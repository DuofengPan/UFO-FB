"""Phase 5 multi-``z`` smoke: resample goal embeddings across episodes.

Compares a **multi-z** AdaptFb loop (sample from GoalBank each reset) against a
**single-z** baseline (fixed first goal). Same LoRA path; F/B frozen.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import torch

from humanoidverse.adapt_fb.core.artifacts import resolve_artifacts
from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy
from humanoidverse.adapt_fb.core.fb_adapter import FbWithAdapter
from humanoidverse.adapt_fb.core.goal_bank import GoalBank
from humanoidverse.adapt_fb.core.obs_bridge import (
    ActorHistoryBuffer,
    build_actor_obs,
    policy_to_mjlab_action,
    proprio_from_robot,
)
from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl


def _rollout(
    *,
    adapted: FbWithAdapter,
    env: Any,
    z_provider,
    steps: int,
    num_envs: int,
    device: str,
) -> dict[str, Any]:
    obs, _ = env.reset()
    names, z = z_provider(num_envs)
    history = ActorHistoryBuffer(num_envs, device=device)
    last_action = torch.zeros(num_envs, adapted.action_dim, device=device)
    reward_hist: list[float] = []
    used_names: set[str] = set(names)

    for _step in range(steps):
        aug = obs["augmentation"]
        if not torch.is_tensor(aug):
            aug = torch.as_tensor(aug, device=device, dtype=torch.float32)
        robot = env.scene["robot"]
        snap = proprio_from_robot(robot, last_action)
        actor_obs = build_actor_obs(snap, history)
        with torch.no_grad():
            action = adapted(actor_obs, z, aug, mean=True)
        last_action = action.detach()
        obs, reward, terminated, truncated, _info = env.step(policy_to_mjlab_action(last_action))
        reward_hist.append(float(reward.mean().detach().cpu()))
        done = terminated | truncated
        if bool(done.any()):
            obs, _ = env.reset()
            history.reset()
            last_action.zero_()
            names, z = z_provider(num_envs)
            used_names.update(names)

    return {
        "reward_mean": sum(reward_hist) / max(len(reward_hist), 1),
        "unique_goals": sorted(used_names),
        "n_unique_goals": len(used_names),
        "steps": steps,
    }


def run_multiz_smoke(
    *,
    checkpoint_dir: Path | None,
    goal_pkl: Path,
    steps: int,
    episodes_hint: int,
    num_envs: int,
    device: str,
    seed: int = 0,
) -> dict[str, Any]:
    """Run single-z vs multi-z short env rollouts; return comparison metrics."""
    ensure_vendored_rsl_rl()
    from mjlab.envs import ManagerBasedRlEnv

    from humanoidverse.adapt_fb.tasks.dodge.env_cfg import dodge_env_cfg

    arts = resolve_artifacts(checkpoint_dir, goal_pkl)
    bank = GoalBank.from_goal_pkl(arts.goal_pkl, device=device)
    frozen = load_frozen_ufo_fb_policy(arts.checkpoint_dir, device=device)
    if bank.z_dim != frozen.z_dim:
        raise ValueError(f"z_dim mismatch bank={bank.z_dim} model={frozen.z_dim}")

    adapted = FbWithAdapter(frozen, augmentation_dim=6, rank=16, alpha=1.0).to(device)
    cfg = dodge_env_cfg(play=False)
    cfg.scene.num_envs = num_envs
    env = ManagerBasedRlEnv(cfg=cfg, device=device)

    gen = torch.Generator(device="cpu")
    gen.manual_seed(seed)
    fixed_name = bank.names[0]
    fixed_z = bank.get(fixed_name).unsqueeze(0).expand(num_envs, -1).contiguous()

    def single_provider(_b: int) -> tuple[list[str], torch.Tensor]:
        return [fixed_name] * num_envs, fixed_z

    def multi_provider(b: int) -> tuple[list[str], torch.Tensor]:
        return bank.sample(b, generator=gen)

    # steps ≈ episodes_hint * short horizon chunks
    total_steps = max(steps, episodes_hint)
    single = _rollout(
        adapted=adapted, env=env, z_provider=single_provider, steps=total_steps, num_envs=num_envs, device=device
    )
    multi = _rollout(
        adapted=adapted, env=env, z_provider=multi_provider, steps=total_steps, num_envs=num_envs, device=device
    )
    env.close()

    return {
        "bank_size": len(bank),
        "bank_names": bank.names,
        "single_z": single,
        "multi_z": multi,
        "protocol": (
            "Eval: same FbWithAdapter weights; single_z fixes goal[0]; "
            "multi_z resamples GoalBank on each env reset. Compare reward_mean "
            "and n_unique_goals (multi should be >1 when bank_size>1)."
        ),
    }


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint-dir", type=Path, default=None)
    p.add_argument("--goal-pkl", type=Path, default=None)
    p.add_argument("--steps", type=int, default=12)
    p.add_argument("--episodes-hint", type=int, default=4)
    p.add_argument("--num-envs", type=int, default=2)
    p.add_argument("--device", type=str, default="cpu")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args(argv)
    info = run_multiz_smoke(
        checkpoint_dir=args.checkpoint_dir,
        goal_pkl=args.goal_pkl,
        steps=args.steps,
        episodes_hint=args.episodes_hint,
        num_envs=args.num_envs,
        device=args.device,
        seed=args.seed,
    )
    print("bank_size:", info["bank_size"])
    print("protocol:", info["protocol"])
    print("single_z.n_unique_goals:", info["single_z"]["n_unique_goals"], "reward_mean:", info["single_z"]["reward_mean"])
    print("multi_z.n_unique_goals:", info["multi_z"]["n_unique_goals"], "reward_mean:", info["multi_z"]["reward_mean"])
    print("multi_z.unique_goals:", info["multi_z"]["unique_goals"][:8], "...")


if __name__ == "__main__":
    main()
