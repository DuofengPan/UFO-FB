"""Play AdaptFb: default host is UFO's MJLab env (goal_inference path).

Run from the **UFO repo root** (this package is ``humanoidverse.adapt_fb``).

Why UFO host (default)
----------------------
The former standalone Adapt ``dodge`` + ``obs_bridge`` rebuilt proprio by hand
and drifted from UFO training. Play reuses ``load_mjlab_env_cfg`` +
``HumanoidVerseMjlabVectorEnv`` so obs/action match the FB checkpoint.

Legacy Adapt dodge remains as ``--backend dodge`` (A/B only).

Examples (cwd = UFO repo)::

    export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
    python -m humanoidverse.adapt_fb.play --agent initial --viewer native --device cuda:0
    python -m humanoidverse.adapt_fb.play --agent initial --steps 300 --device cuda:0
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
from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl

AgentMode = Literal["trained", "initial"]
Backend = Literal["ufo", "dodge"]


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
    """Strip play-only keys; keep UFO actor / normalizer fields."""
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
            aug = obs["augmentation"]  # type: ignore[index]
            return self.adapted(actor_obs, z, aug, mean=self.mean)

    def reset(self) -> None:
        pass


class _GoalCycleNativeViewer:
    def __init__(self, env: object, policy: _Policy, *, cycle_fn) -> None:
        from mjlab.viewer import NativeMujocoViewer
        from mjlab.viewer.base import ViewerAction
        from mjlab.viewer.native.keys import KEY_B, KEY_N

        self._cycle_fn = cycle_fn
        self._stdin_stop = threading.Event()
        self._stdin_thread: threading.Thread | None = None
        self._old_termios: list | None = None
        outer = self

        class _Viewer(NativeMujocoViewer):  # type: ignore[misc, valid-type]
            def _handle_custom_action(self, action: ViewerAction, payload: object | None) -> bool:
                if action == ViewerAction.CUSTOM and isinstance(payload, dict):
                    delta = int(payload.get("goal_delta", 0))
                    if delta != 0:
                        name = outer._cycle_fn(delta)
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


def _run_ufo_play(
    *,
    steps: int,
    num_envs: int,
    device: str,
    adapter_ckpt: Path | None,
    checkpoint_dir: Path | None,
    goal_pkl: Path | None,
    multi_z: bool,
    mean: bool,
    viewer: str,
    agent: AgentMode,
    data_path: Path | None,
) -> dict[str, float]:
    from humanoidverse.adapt_fb.core.ufo_host import UfoHostPlayEnv, build_ufo_vector_env

    arts = resolve_artifacts(checkpoint_dir, goal_pkl)
    model_folder = resolve_model_folder(arts.checkpoint_dir)
    bank = GoalBank.from_goal_pkl(arts.goal_pkl, device=device)
    frozen = load_frozen_ufo_fb_policy(arts.checkpoint_dir, device=device)
    adapted = FbWithAdapter(frozen, augmentation_dim=6, rank=16, alpha=1.0).to(device)

    if agent == "initial":
        print("[INFO]: agent=initial — frozen UFO-FB via UFO host env", flush=True)
        if adapter_ckpt is not None:
            print(f"[INFO]: ignoring --adapter-ckpt {adapter_ckpt}", flush=True)
    else:
        _load_adapter(adapted, adapter_ckpt, device)
        print("[INFO]: agent=trained — LoRA on UFO host (aug=zeros until ball port)", flush=True)

    print(f"[INFO]: UFO model_folder={model_folder}", flush=True)
    vector = build_ufo_vector_env(
        model_folder,
        device=device,
        num_envs=1 if viewer != "none" else num_envs,
        data_path=data_path,
        headless=(viewer == "none"),
    )
    env = UfoHostPlayEnv(
        vector,
        bank,
        multi_z=multi_z and viewer == "none",
        fixed_goal_name=None if multi_z else bank.names[0],
    )
    policy = _Policy(adapted, mean=mean, agent=agent)

    if viewer == "none":
        obs = env.get_observations()
        reward_sum = 0.0
        height_sum = 0.0
        done_events = 0
        robot = env.unwrapped.scene["robot"]
        for _ in range(steps):
            action = policy(obs)
            obs, rew, dones, _ = env.step(action)
            reward_sum += float(rew.mean().cpu())
            height_sum += float(robot.data.root_link_pos_w[:, 2].mean().cpu())
            if bool(dones.any()):
                done_events += 1
        env.close()
        return {
            "steps": float(steps),
            "reward_mean": reward_sum / max(steps, 1),
            "height_mean": height_sum / max(steps, 1),
            "done_events": float(done_events),
        }

    print(
        f"[play] backend=ufo agent={agent} goals={len(bank)} "
        f"current={env._goal_names[0]!r}\n"
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


def _run_dodge_play(
    *,
    steps: int,
    num_envs: int,
    device: str,
    adapter_ckpt: Path | None,
    checkpoint_dir: Path | None,
    goal_pkl: Path | None,
    multi_z: bool,
    mean: bool,
    viewer: str,
    agent: AgentMode,
    no_ball: bool,
) -> dict[str, float]:
    """Legacy Adapt dodge + obs_bridge (kept for A/B; known to diverge from UFO)."""
    ensure_vendored_rsl_rl()
    from mjlab.envs import ManagerBasedRlEnv

    from humanoidverse.adapt_fb.core.dodge_vec_env import DodgeFbVecEnv
    from humanoidverse.adapt_fb.tasks.dodge.env_cfg import dodge_env_cfg

    print(
        "[WARN]: --backend dodge uses Adapt obs_bridge (history / last_action may "
        "diverge from UFO). Prefer --backend ufo.",
        flush=True,
    )
    arts = resolve_artifacts(checkpoint_dir, goal_pkl)
    bank = GoalBank.from_goal_pkl(arts.goal_pkl, device=device)
    frozen = load_frozen_ufo_fb_policy(arts.checkpoint_dir, device=device)
    adapted = FbWithAdapter(frozen, augmentation_dim=6, rank=16, alpha=1.0).to(device)
    if agent == "initial":
        print("[INFO]: agent=initial — frozen base on dodge bridge", flush=True)
    else:
        _load_adapter(adapted, adapter_ckpt, device)

    cfg = dodge_env_cfg(play=True, throw_ball=not no_ball)
    cfg.scene.num_envs = 1 if viewer != "none" else num_envs
    mj_env = ManagerBasedRlEnv(cfg=cfg, device=device)
    vec = DodgeFbVecEnv(mj_env, bank, multi_z=multi_z)
    policy = _Policy(adapted, mean=mean, agent=agent)

    if viewer == "none":
        obs = vec.get_observations().to(device)
        reward_sum = 0.0
        for _ in range(steps):
            action = policy(obs)
            obs, rew, _d, _e = vec.step(action)
            reward_sum += float(rew.mean().cpu())
        vec.close()
        return {"steps": float(steps), "reward_mean": reward_sum / max(steps, 1)}

    print(
        f"[play] backend=dodge agent={agent} no_ball={no_ball} "
        f"goals={len(bank)} current={vec._goal_names[0]!r}",
        flush=True,
    )
    if viewer == "native":
        _GoalCycleNativeViewer(vec, policy, cycle_fn=lambda d: vec.cycle_goals(step=d)).run()
    else:
        from mjlab.viewer import ViserPlayViewer

        ViserPlayViewer(vec, policy, checkpoint_manager=None).run()
    vec.close()
    return {"steps": 0.0, "reward_mean": 0.0}


def run_play(**kwargs) -> dict[str, float]:
    backend: Backend = kwargs.pop("backend", "ufo")
    if backend == "ufo":
        kwargs.pop("no_ball", None)
        return _run_ufo_play(**kwargs)
    return _run_dodge_play(**kwargs)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--backend",
        type=str,
        default="ufo",
        choices=("ufo", "dodge"),
        help="ufo=UFO goal_inference env (default); dodge=legacy Adapt bridge",
    )
    p.add_argument("--steps", type=int, default=200)
    p.add_argument("--num-envs", type=int, default=1)
    p.add_argument("--device", type=str, default="cuda:0")
    p.add_argument("--adapter-ckpt", type=Path, default=None)
    p.add_argument("--checkpoint-dir", type=Path, default=None)
    p.add_argument("--goal-pkl", type=Path, default=None)
    p.add_argument("--data-path", type=Path, default=None, help="UFO motion pkl override")
    p.add_argument("--single-z", action="store_true")
    p.add_argument("--agent", type=str, default="initial", choices=("trained", "initial"))
    p.add_argument("--no-ball", action="store_true", help="dodge backend only: park ball far away")
    p.add_argument("--viewer", type=str, default="none", choices=("none", "native", "viser"))
    args = p.parse_args(argv)
    if args.device.startswith("cuda") and not torch.cuda.is_available():
        args.device = "cpu"
    if args.viewer != "none":
        args.num_envs = 1
    info = run_play(
        backend=args.backend,  # type: ignore[arg-type]
        steps=args.steps,
        num_envs=args.num_envs,
        device=args.device,
        adapter_ckpt=args.adapter_ckpt,
        checkpoint_dir=args.checkpoint_dir,
        goal_pkl=args.goal_pkl,
        multi_z=not args.single_z,
        mean=True,
        viewer=args.viewer,
        agent=args.agent,  # type: ignore[arg-type]
        no_ball=args.no_ball,
        data_path=args.data_path,
    )
    for k, v in info.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
