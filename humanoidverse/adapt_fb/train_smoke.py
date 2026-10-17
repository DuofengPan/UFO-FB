"""Phase 4 train smoke: MJLab dodge env + frozen UFO-FB LoRA, one Adam step.

Uses privileged ball ``augmentation`` from the env and an offline goal ``z``.
Does **not** update F/B/actor base weights.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import torch

from humanoidverse.adapt_fb.core.artifacts import resolve_artifacts
from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy
from humanoidverse.adapt_fb.core.fb_adapter import FbWithAdapter
from humanoidverse.adapt_fb.core.obs_bridge import (
    ActorHistoryBuffer,
    build_actor_obs,
    policy_to_mjlab_action,
    proprio_from_robot,
)
from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl


def _load_z(goal_pkl: Path | None, z_dim: int, device: str) -> tuple[str, torch.Tensor]:
    if goal_pkl is not None and goal_pkl.is_file():
        import joblib

        z_dict = joblib.load(goal_pkl)
        name = sorted(z_dict.keys())[0]
        z = torch.as_tensor(z_dict[name], device=device, dtype=torch.float32)
        if z.ndim == 1:
            z = z.unsqueeze(0)
        return name, z
    return "random", torch.nn.functional.normalize(torch.randn(1, z_dim, device=device), dim=-1) * (z_dim**0.5)


def run_train_smoke(
    *,
    checkpoint_dir: Path | None,
    goal_pkl: Path | None,
    steps: int,
    device: str,
    num_envs: int = 2,
) -> dict[str, Any]:
    ensure_vendored_rsl_rl()

    from mjlab.envs import ManagerBasedRlEnv

    from humanoidverse.adapt_fb.tasks.dodge.env_cfg import dodge_env_cfg

    arts = resolve_artifacts(checkpoint_dir, goal_pkl)
    frozen = load_frozen_ufo_fb_policy(arts.checkpoint_dir, device=device)
    goal_name, z = _load_z(arts.goal_pkl, frozen.z_dim, device)
    # ball_pos_b (3) + ball_vel_b (3)
    aug_dim = 6
    adapted = FbWithAdapter(frozen, augmentation_dim=aug_dim, rank=16, alpha=1.0).to(device)
    opt = torch.optim.Adam(adapted.trainable_parameters(), lr=1e-3)

    cfg = dodge_env_cfg(play=False)
    cfg.scene.num_envs = num_envs
    env = ManagerBasedRlEnv(cfg=cfg, device=device)

    obs, _info = env.reset()
    z_b = z.expand(num_envs, -1).contiguous()
    history = ActorHistoryBuffer(num_envs, device=device)
    last_action = torch.zeros(num_envs, frozen.action_dim, device=device)

    reward_hist: list[float] = []
    for step in range(steps):
        aug = obs["augmentation"]
        if not torch.is_tensor(aug):
            aug = torch.as_tensor(aug, device=device, dtype=torch.float32)
        robot = env.scene["robot"]
        snap = proprio_from_robot(robot, last_action)
        actor_obs = build_actor_obs(snap, history)

        action = adapted(actor_obs, z_b, aug, mean=True)
        act_dim = env.action_manager.action.shape[-1]
        if action.shape[-1] != act_dim:
            raise RuntimeError(f"action dim mismatch: adapter={action.shape[-1]} env={act_dim}")

        last_action = action.detach()
        obs, reward, terminated, truncated, _info = env.step(policy_to_mjlab_action(last_action))
        reward_hist.append(float(reward.mean().detach().cpu()))

        if step == steps - 1:
            opt.zero_grad(set_to_none=True)
            actor_obs_g = {k: v.detach() for k, v in actor_obs.items()}
            a = adapted(actor_obs_g, z_b.detach(), aug.detach(), mean=True)
            loss = 1e-4 * a.pow(2).mean()
            loss.backward()
            opt.step()

        if bool(terminated.any()) or bool(truncated.any()):
            obs, _info = env.reset()
            history.reset()
            last_action.zero_()

    env.close()
    return {
        "goal_name": goal_name,
        "steps": steps,
        "num_envs": num_envs,
        "reward_mean": sum(reward_hist) / max(len(reward_hist), 1),
        "aug_dim": aug_dim,
        "action_dim": int(adapted.action_dim),
        "adapter_grad_ok": True,
    }


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint-dir", type=Path, default=None)
    p.add_argument("--goal-pkl", type=Path, default=None)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--num-envs", type=int, default=2)
    p.add_argument("--device", type=str, default="cpu")
    args = p.parse_args(argv)
    info = run_train_smoke(
        checkpoint_dir=args.checkpoint_dir,
        goal_pkl=args.goal_pkl,
        steps=args.steps,
        device=args.device,
        num_envs=args.num_envs,
    )
    for k, v in info.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
