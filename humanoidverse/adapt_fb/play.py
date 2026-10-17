"""ORCS-style interactive play for AdaptFb (UFO MJLab host + optional ball).

Does **not** overwrite UFO ``goal_inference`` artifacts. Goal ``z`` is read-only
from the existing ``goal_reaching.pkl``.

Examples (cwd = UFO repo root)::

    export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

    # Frozen base, no ball (UFO host only)
    python -m humanoidverse.adapt_fb.play --agent initial --ball none --viewer native

    # Ball present but parked / pinned overhead (inactive threat)
    python -m humanoidverse.adapt_fb.play --agent initial --ball parked --viewer native

    # Ball thrown at the robot (cone threat)
    python -m humanoidverse.adapt_fb.play --agent initial --ball throw --viewer native

Keys: ``n``/``b`` cycle goal (MuJoCo window or terminal); Space pause; Enter reset.
"""

from __future__ import annotations

import argparse
import select
import sys
import termios
import threading
import tty
from pathlib import Path
from typing import Literal

import torch

from humanoidverse.adapt_fb.core.artifacts import resolve_artifacts, resolve_model_folder
from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy
from humanoidverse.adapt_fb.core.fb_adapter import FbWithAdapter
from humanoidverse.adapt_fb.core.goal_bank import GoalBank
from humanoidverse.adapt_fb.core.ufo_host import BallMode, UfoHostPlayEnv, build_ufo_vector_env

AgentMode = Literal["trained", "initial"]


def _load_adapter(adapted: FbWithAdapter, adapter_ckpt: Path | None, device: str) -> None:
    if adapter_ckpt is None or not adapter_ckpt.is_file():
        return
    payload = torch.load(adapter_ckpt, map_location=device, weights_only=False)
    state = payload.get("actor_state_dict", payload)
    adapted_sd = {
        k.replace("adapted.", "", 1): v
        for k, v in state.items()
        if k.startswith("adapted.") or k.startswith("adapters.")
    }
    if not adapted_sd:
        adapted_sd = {k: v for k, v in state.items() if "adapter" in k.lower()}
    missing, unexpected = adapted.load_state_dict(adapted_sd, strict=False)
    print(f"loaded adapter ckpt missing={len(missing)} unexpected={len(unexpected)}")


def _actor_obs_from_td(obs: object) -> dict[str, torch.Tensor]:
    skip = {"goal_z", "augmentation", "critic"}
    out: dict[str, torch.Tensor] = {}
    for key in obs.keys():  # type: ignore[union-attr]
        if key in skip:
            continue
        out[key] = obs[key]
    return out


class _Policy:
    def __init__(
        self,
        adapted: FbWithAdapter,
        *,
        mean: bool = True,
        agent: AgentMode = "trained",
    ) -> None:
        self.adapted = adapted
        self.mean = mean
        self.agent = agent

    def __call__(self, obs: object) -> torch.Tensor:
        with torch.no_grad():
            actor_obs = _actor_obs_from_td(obs)
            z = obs["goal_z"]  # type: ignore[index]
            if self.agent == "initial":
                return self.adapted.act_base(actor_obs, z, mean=self.mean)
            return self.adapted(actor_obs, z, obs["augmentation"], mean=self.mean)  # type: ignore[index]

    def reset(self) -> None:
        pass


class _GoalCycleNativeViewer:
    def __init__(self, env: UfoHostPlayEnv, policy: _Policy, *, cycle_fn) -> None:
        from mjlab.viewer import NativeMujocoViewer
        from mjlab.viewer.base import ViewerAction
        from mjlab.viewer.native.keys import KEY_B, KEY_N

        self._cycle_fn = cycle_fn
        self._stdin_stop = threading.Event()
        self._stdin_thread: threading.Thread | None = None
        self._old_termios: list | None = None

        class _Viewer(NativeMujocoViewer):  # type: ignore[misc, valid-type]
            def _handle_custom_action(self, action: ViewerAction, payload: object | None) -> bool:
                if action == ViewerAction.CUSTOM and isinstance(payload, dict):
                    delta = int(payload.get("goal_delta", 0))
                    if delta != 0:
                        name = cycle_fn(delta)
                        self.log(f"[INFO] goal → {name}")
                        print(f"[play] goal → {name}", flush=True)
                        return True
                return super()._handle_custom_action(action, payload)

        def _on_key(key: int) -> None:
            if key == KEY_N:
                viewer.request_action("CUSTOM", {"goal_delta": 1})
            elif key == KEY_B:
                viewer.request_action("CUSTOM", {"goal_delta": -1})

        viewer = _Viewer(env, policy, key_callback=_on_key)
        self._viewer = viewer

    def run(self) -> None:
        if sys.stdin.isatty():
            self._start_stdin()
        try:
            self._viewer.run()
        finally:
            self._stop_stdin()

    def _start_stdin(self) -> None:
        try:
            fd = sys.stdin.fileno()
            self._old_termios = termios.tcgetattr(fd)
            tty.setcbreak(fd)
        except (termios.error, OSError) as exc:
            print(f"[play] stdin listen disabled: {exc}", flush=True)
            return

        def _loop() -> None:
            while not self._stdin_stop.is_set():
                try:
                    ready, _, _ = select.select([sys.stdin], [], [], 0.2)
                except (ValueError, OSError):
                    break
                if not ready:
                    continue
                ch = sys.stdin.read(1)
                if ch in ("n", "N"):
                    self._viewer.request_action("CUSTOM", {"goal_delta": 1})
                elif ch in ("b", "B"):
                    self._viewer.request_action("CUSTOM", {"goal_delta": -1})

        self._stdin_thread = threading.Thread(target=_loop, name="goal-stdin", daemon=True)
        self._stdin_thread.start()
        print("[play] terminal keys: n/b cycle goal (or MuJoCo window)", flush=True)

    def _stop_stdin(self) -> None:
        self._stdin_stop.set()
        if self._stdin_thread is not None:
            self._stdin_thread.join(timeout=1.0)
        if self._old_termios is not None:
            try:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self._old_termios)
            except (termios.error, OSError):
                pass


def run_play(
    *,
    steps: int,
    num_envs: int,
    device: str,
    adapter_ckpt: Path | None,
    checkpoint_dir: Path | None,
    goal_pkl: Path | None,
    multi_z: bool,
    mean: bool = True,
    viewer: str = "none",
    agent: AgentMode = "initial",
    data_path: Path | None = None,
    ball: BallMode = "none",
) -> dict[str, float]:
    arts = resolve_artifacts(checkpoint_dir, goal_pkl)
    model_folder = resolve_model_folder(arts.checkpoint_dir)
    bank = GoalBank.from_goal_pkl(arts.goal_pkl, device=device)
    frozen = load_frozen_ufo_fb_policy(arts.checkpoint_dir, device=device)
    adapted = FbWithAdapter(frozen, augmentation_dim=6, rank=16, alpha=1.0).to(device)

    if agent == "initial":
        print(f"[INFO]: agent=initial ball={ball} — frozen UFO-FB on UFO host", flush=True)
        if adapter_ckpt is not None:
            print(f"[INFO]: ignoring --adapter-ckpt {adapter_ckpt}", flush=True)
    else:
        _load_adapter(adapted, adapter_ckpt, device)
        print(f"[INFO]: agent=trained ball={ball} — LoRA on UFO host", flush=True)

    print(f"[INFO]: UFO model_folder={model_folder}", flush=True)
    n_env = 1 if viewer != "none" else num_envs
    vector = build_ufo_vector_env(
        model_folder,
        device=device,
        num_envs=n_env,
        data_path=data_path,
        headless=(viewer == "none"),
        ball=ball,
    )
    env = UfoHostPlayEnv(
        vector,
        bank,
        ball=ball,
        multi_z=multi_z and viewer == "none",
        fixed_goal_name=None if multi_z else bank.names[0],
    )
    policy = _Policy(adapted, mean=mean, agent=agent)

    if viewer == "none":
        obs = env.get_observations()
        reward_sum = 0.0
        height_sum = 0.0
        done_events = 0
        aug_abs = 0.0
        robot = env.unwrapped.scene["robot"]
        for _ in range(steps):
            action = policy(obs)
            obs, rew, dones, _ = env.step(action)
            reward_sum += float(rew.mean().cpu())
            height_sum += float(robot.data.root_link_pos_w[:, 2].mean().cpu())
            aug_abs += float(obs["augmentation"].abs().mean().cpu())
            if bool(dones.any()):
                done_events += 1
        env.close()
        return {
            "steps": float(steps),
            "reward_mean": reward_sum / max(steps, 1),
            "height_mean": height_sum / max(steps, 1),
            "aug_abs_mean": aug_abs / max(steps, 1),
            "done_events": float(done_events),
        }

    print(
        f"[play] ball={ball} agent={agent} goals={len(bank)} current={env._goal_names[0]!r}\n"
        "  keys: n/b goal, Space pause, Enter reset, +/- speed",
        flush=True,
    )
    if viewer == "native":
        _GoalCycleNativeViewer(env, policy, cycle_fn=lambda d: env.cycle_goals(step=d)).run()
    elif viewer == "viser":
        from mjlab.viewer import ViserPlayViewer

        ViserPlayViewer(env, policy, checkpoint_manager=None).run()
    else:
        raise ValueError(viewer)
    env.close()
    return {"steps": 0.0, "reward_mean": 0.0}


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--steps", type=int, default=200)
    p.add_argument("--num-envs", type=int, default=1)
    p.add_argument("--device", type=str, default="cuda:0")
    p.add_argument("--adapter-ckpt", type=Path, default=None)
    p.add_argument("--checkpoint-dir", type=Path, default=None)
    p.add_argument("--goal-pkl", type=Path, default=None)
    p.add_argument("--data-path", type=Path, default=None)
    p.add_argument("--single-z", action="store_true")
    p.add_argument("--agent", type=str, default="initial", choices=("trained", "initial"))
    p.add_argument(
        "--ball",
        type=str,
        default="none",
        choices=("none", "parked", "throw"),
        help="none=UFO host only; parked=ball pinned overhead; throw=cone throws at robot",
    )
    p.add_argument("--viewer", type=str, default="none", choices=("none", "native", "viser"))
    args = p.parse_args(argv)
    if args.device.startswith("cuda") and not torch.cuda.is_available():
        args.device = "cpu"
    if args.viewer != "none":
        args.num_envs = 1
    info = run_play(
        steps=args.steps,
        num_envs=args.num_envs,
        device=args.device,
        adapter_ckpt=args.adapter_ckpt,
        checkpoint_dir=args.checkpoint_dir,
        goal_pkl=args.goal_pkl,
        multi_z=not args.single_z,
        viewer=args.viewer,
        agent=args.agent,  # type: ignore[arg-type]
        data_path=args.data_path,
        ball=args.ball,  # type: ignore[arg-type]
    )
    for k, v in info.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
