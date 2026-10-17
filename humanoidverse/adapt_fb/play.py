"""ORCS-style interactive play for AdaptFb (UFO MJLab host + optional ball).

Does **not** overwrite UFO ``goal_inference`` artifacts. Goal ``z`` is read-only
from the existing ``goal_reaching.pkl``.

``--agent`` modes (A/B/C contrasts)::

    base           original UFO-FB (ignore AdaptFb ckpt)
    adapted-base   frozen stem from AdaptFb ckpt, LoRA off  (vs base)
    adapted        full post-train policy (stem + LoRA)     (vs adapted-base)

Examples (cwd = UFO repo root)::

    export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"

    python -m humanoidverse.adapt_fb.play --agent base --ball none --viewer native
    python -m humanoidverse.adapt_fb.play --agent base --ball parked --viewer native
    python -m humanoidverse.adapt_fb.play --agent base --ball throw --viewer native

    python -m humanoidverse.adapt_fb.play --agent adapted-base \\
      --adapter-ckpt runs/adapt_fb_ufo_host_300/model_299.pt --ball throw --viewer native

    python -m humanoidverse.adapt_fb.play --agent adapted \\
      --adapter-ckpt runs/adapt_fb_ufo_host_300/model_299.pt --ball throw --viewer native

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

from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl

ensure_vendored_rsl_rl()

from humanoidverse.adapt_fb.core.artifacts import resolve_artifacts, resolve_model_folder
from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy
from humanoidverse.adapt_fb.core.fb_adapter import FbWithAdapter
from humanoidverse.adapt_fb.core.goal_bank import GoalBank
from humanoidverse.adapt_fb.core.ufo_host import BallMode, UfoHostPlayEnv, build_ufo_vector_env

AgentMode = Literal["base", "adapted-base", "adapted"]

# Legacy CLI aliases → canonical modes.
_AGENT_ALIASES: dict[str, AgentMode] = {
    "initial": "base",
    "trained": "adapted",
}


def resolve_agent_mode(raw: str) -> AgentMode:
    key = raw.strip().lower()
    if key in _AGENT_ALIASES:
        print(f"[INFO]: --agent {raw!r} → {_AGENT_ALIASES[key]!r} (legacy alias)", flush=True)
        return _AGENT_ALIASES[key]
    if key in ("base", "adapted-base", "adapted"):
        return key  # type: ignore[return-value]
    raise ValueError(
        f"Unknown --agent {raw!r}. Expected base | adapted-base | adapted "
        f"(aliases: initial→base, trained→adapted)."
    )


def _load_adapt_ckpt(
    adapted: FbWithAdapter, adapter_ckpt: Path, device: str, *, need_normalizer: bool
) -> torch.nn.Module:
    """Load ``adapted.*`` (frozen stem + adapters) from an rsl_rl actor ckpt.

    When ``need_normalizer`` is True, also load ``adapter_normalizer`` (or warn and
    return Identity). Returns the aug→condition module for the LoRA path.
    """
    from rsl_rl.modules.normalization import EmpiricalNormalization

    if not adapter_ckpt.is_file():
        raise FileNotFoundError(f"AdaptFb checkpoint not found: {adapter_ckpt}")

    payload = torch.load(adapter_ckpt, map_location=device, weights_only=False)
    state = payload.get("actor_state_dict", payload)
    adapted_sd = {
        k.replace("adapted.", "", 1): v
        for k, v in state.items()
        if k.startswith("adapted.")
    }
    if not adapted_sd:
        # Older / partial dumps may only store adapters.*
        adapted_sd = {
            k: v for k, v in state.items() if k.startswith("adapters.")
        }
    missing, unexpected = adapted.load_state_dict(adapted_sd, strict=False)
    print(
        f"loaded adapt ckpt {adapter_ckpt} "
        f"adapted_keys={len(adapted_sd)} missing={len(missing)} unexpected={len(unexpected)}",
        flush=True,
    )

    if not need_normalizer:
        return torch.nn.Identity()

    norm_sd = {
        k.replace("adapter_normalizer.", "", 1): v
        for k, v in state.items()
        if k.startswith("adapter_normalizer.")
    }
    if not norm_sd:
        print("[WARN]: ckpt has no adapter_normalizer; feeding raw augmentation", flush=True)
        return torch.nn.Identity()
    normalizer = EmpiricalNormalization(adapted.augmentation_dim).to(device)
    normalizer.load_state_dict(norm_sd)
    normalizer.eval()
    print(
        f"loaded adapter_normalizer mean={normalizer._mean.flatten().tolist()} "
        f"std={normalizer._std.flatten().tolist()}",
        flush=True,
    )
    return normalizer


class _Policy:
    def __init__(
        self,
        adapted: FbWithAdapter,
        *,
        mean: bool = True,
        agent: AgentMode = "adapted",
        aug_normalizer: torch.nn.Module | None = None,
    ) -> None:
        self.adapted = adapted
        self.mean = mean
        self.agent = agent
        self.aug_normalizer = aug_normalizer if aug_normalizer is not None else torch.nn.Identity()

    def __call__(self, obs: object) -> torch.Tensor:
        with torch.no_grad():
            # Match FbWithAdapterModel training obs groups (ignore host extras).
            actor_obs = {
                "state": obs["state"],  # type: ignore[index]
                "last_action": obs["last_action"],  # type: ignore[index]
                "history_actor": obs["history_actor"],  # type: ignore[index]
            }
            z = obs["goal_z"]  # type: ignore[index]
            # base / adapted-base: frozen stem only (no LoRA), different weight sources.
            if self.agent in ("base", "adapted-base"):
                return self.adapted.act_base(actor_obs, z, mean=self.mean)
            aug = self.aug_normalizer(obs["augmentation"])  # type: ignore[index]
            return self.adapted(actor_obs, z, aug, mean=self.mean)

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
    agent: AgentMode | str = "base",
    data_path: Path | None = None,
    ball: BallMode = "none",
) -> dict[str, float]:
    ensure_vendored_rsl_rl()
    if agent not in ("base", "adapted-base", "adapted"):
        agent = resolve_agent_mode(str(agent))

    arts = resolve_artifacts(checkpoint_dir, goal_pkl)
    model_folder = resolve_model_folder(arts.checkpoint_dir)
    bank = GoalBank.from_goal_pkl(arts.goal_pkl, device=device)

    # Scaffold module graph from the original UFO run; adapted-* then overwrite
    # ``adapted.*`` from the AdaptFb checkpoint (including frozen stem).
    frozen = load_frozen_ufo_fb_policy(arts.checkpoint_dir, device=device)
    adapted = FbWithAdapter(frozen, augmentation_dim=6, rank=16, alpha=1.0).to(device)

    aug_normalizer: torch.nn.Module = torch.nn.Identity()
    if agent == "base":
        print(
            f"[INFO]: agent=base ball={ball} — original UFO-FB (ignore AdaptFb ckpt)",
            flush=True,
        )
        if adapter_ckpt is not None:
            print(f"[INFO]: ignoring --adapter-ckpt {adapter_ckpt}", flush=True)
    else:
        if adapter_ckpt is None:
            raise ValueError(f"--agent {agent} requires --adapter-ckpt")
        aug_normalizer = _load_adapt_ckpt(
            adapted, adapter_ckpt, device, need_normalizer=(agent == "adapted")
        )
        if agent == "adapted-base":
            print(
                f"[INFO]: agent=adapted-base ball={ball} — "
                "AdaptFb ckpt frozen stem, LoRA off (act_base)",
                flush=True,
            )
        else:
            print(
                f"[INFO]: agent=adapted ball={ball} — "
                "AdaptFb ckpt full policy (stem + LoRA)",
                flush=True,
            )

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
    policy = _Policy(adapted, mean=mean, agent=agent, aug_normalizer=aug_normalizer)

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

    hint = ""
    if ball == "throw":
        hint = "\n  throw: ball parks overhead, then flies at the robot every ~0.6–1.2s"
    elif ball == "parked":
        hint = "\n  parked: ball stays far away (no throws)"
    print(
        f"[play] ball={ball} agent={agent} goals={len(bank)} current={env._goal_names[0]!r}\n"
        "  keys: n/b goal, Space pause, Enter reset, +/- speed"
        f"{hint}",
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
    p.add_argument("--adapter-ckpt", type=Path, default=None, help="AdaptFb rsl_rl model_*.pt (required for adapted*)")
    p.add_argument("--checkpoint-dir", type=Path, default=None, help="Original UFO-FB checkpoint dir")
    p.add_argument("--goal-pkl", type=Path, default=None)
    p.add_argument("--data-path", type=Path, default=None)
    p.add_argument("--single-z", action="store_true")
    p.add_argument(
        "--agent",
        type=str,
        default="base",
        help="base | adapted-base | adapted  (aliases: initial→base, trained→adapted)",
    )
    p.add_argument(
        "--ball",
        type=str,
        default="none",
        choices=("none", "parked", "throw"),
        help="none=UFO host only; parked=ball pinned overhead; throw=cone throws at robot",
    )
    p.add_argument("--viewer", type=str, default="none", choices=("none", "native", "viser"))
    args = p.parse_args(argv)
    agent = resolve_agent_mode(args.agent)
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
        agent=agent,
        data_path=args.data_path,
        ball=args.ball,  # type: ignore[arg-type]
    )
    for k, v in info.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
