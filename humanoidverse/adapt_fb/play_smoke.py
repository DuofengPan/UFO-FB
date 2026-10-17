"""Phase 3 policy play smoke: frozen UFO-FB + LoRA, offline goal ``z``, no physics.

This validates the adaptation stack end-to-end without MJLab scenes. Full
``play`` with dodge physics arrives in Phase 4.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import torch

from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy, make_dummy_actor_obs
from humanoidverse.adapt_fb.core.fb_adapter import FbWithAdapter
from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl


def _load_goal_z(goal_pkl: Path, device: str) -> tuple[str, torch.Tensor]:
    import joblib

    z_dict: dict[str, Any] = joblib.load(goal_pkl)
    if not z_dict:
        raise RuntimeError(f"Empty goal pkl: {goal_pkl}")
    name = sorted(z_dict.keys())[0]
    z = torch.as_tensor(z_dict[name], device=device, dtype=torch.float32)
    if z.ndim == 1:
        z = z.unsqueeze(0)
    return name, z


def run_play_smoke(
    *,
    checkpoint_dir: Path | None,
    goal_pkl: Path | None,
    steps: int,
    augmentation_dim: int,
    device: str,
) -> dict[str, Any]:
    ensure_vendored_rsl_rl()
    # Sanity: vendored package importable
    import rsl_rl  # noqa: F401
    from rsl_rl.modules.mlp_with_adapter import Adapter as RslAdapter  # noqa: F401

    frozen = load_frozen_ufo_fb_policy(checkpoint_dir, device=device)
    adapted = FbWithAdapter(frozen, augmentation_dim=augmentation_dim, rank=16, alpha=1.0)
    adapted.to(device)

    if goal_pkl is not None and goal_pkl.is_file():
        goal_name, z = _load_goal_z(goal_pkl, device)
    else:
        goal_name = "random_projected_z"
        z = frozen.model.project_z(torch.randn(1, frozen.z_dim, device=device))

    obs = make_dummy_actor_obs(1, device=device)
    # Mild non-zero proprio so the stack is exercised.
    obs = {k: torch.randn_like(v) * 0.01 for k, v in obs.items()}
    aug = torch.zeros(1, augmentation_dim, device=device)

    actions = []
    with torch.no_grad():
        for _ in range(steps):
            a = adapted(obs, z, aug, mean=True)
            actions.append(a.detach().cpu())
            # Fake closed loop: last_action feeds next obs
            if "last_action" in obs:
                obs["last_action"] = a

    stacked = torch.cat(actions, dim=0)
    return {
        "goal_name": goal_name,
        "steps": steps,
        "action_shape": tuple(stacked.shape),
        "action_mean_abs": float(stacked.abs().mean()),
        "rsl_rl_file": str(Path(rsl_rl.__file__).resolve()),
        "z_dim": frozen.z_dim,
        "action_dim": frozen.action_dim,
    }


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint-dir", type=Path, default=None)
    p.add_argument("--goal-pkl", type=Path, default=None)
    p.add_argument("--steps", type=int, default=16)
    p.add_argument("--augmentation-dim", type=int, default=8)
    p.add_argument("--device", type=str, default="cpu")
    args = p.parse_args(argv)

    # play_smoke.py -> humanoidverse.adapt_fb -> src -> UFO-FB-adapt -> code/
    default_goal = (
        Path(__file__).resolve().parents[3]
        / "UFO"
        / "runs"
        / "ufo_fb_8gpu"
        / "goal_inference"
        / "goal_reaching.pkl"
    )
    goal = args.goal_pkl if args.goal_pkl is not None else default_goal

    info = run_play_smoke(
        checkpoint_dir=args.checkpoint_dir,
        goal_pkl=goal if goal.is_file() else None,
        steps=args.steps,
        augmentation_dim=args.augmentation_dim,
        device=args.device,
    )
    for k, v in info.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
