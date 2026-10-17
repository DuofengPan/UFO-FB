"""AdaptFb agent zoo — ORCS-shaped, UFO-FB base (no ``orcs`` import).

Every AdaptFb task trains the same way: adaptive-KL PPO over an asymmetric
actor-critic. The actor is frozen UFO-FB + LoRA; the critic is a fresh MLP.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from humanoidverse.adapt_fb.core.artifacts import resolve_checkpoint_dir

__all__ = [
    "CRITIC_HIDDEN",
    "DIST_BASE_BAND",
    "NUM_STEPS_PER_ENV",
    "MAX_ITERATIONS",
    "SAVE_INTERVAL",
    "fb_adapter_actor",
    "adapt_fb_agent_cfg",
]

CRITIC_HIDDEN = (512, 256, 128)
NUM_STEPS_PER_ENV = 24
MAX_ITERATIONS = 60_000
SAVE_INTERVAL = 500

DIST_BASE_BAND = {
    "class_name": "GaussianDistribution",
    "init_std": 0.05,  # UFO actor_std default; overwritten if cfg differs
    "std_type": "scalar",
    "learn_std": False,
}


def fb_adapter_actor(
    *,
    rank: int = 16,
    alpha: float = 1.0,
    base_checkpoint: str | Path | None = None,
    adapter_obs_group: str = "augmentation",
    goal_obs_group: str = "goal_z",
    init_std: float | None = None,
) -> dict[str, Any]:
    """Frozen UFO-FB + zero-init LoRA on ResidualActor.policy Linears."""
    ckpt = str(resolve_checkpoint_dir(base_checkpoint))
    dist = dict(DIST_BASE_BAND)
    if init_std is not None:
        dist["init_std"] = float(init_std)
    return {
        "class_name": "humanoidverse.adapt_fb.core.fb_adapter_model.FbWithAdapterModel",
        "distribution_cfg": dist,
        "adapter_obs_group": adapter_obs_group,
        "goal_obs_group": goal_obs_group,
        "rank": rank,
        "alpha": alpha,
        "base_checkpoint": ckpt,
        "obs_normalization": True,
    }


def adapt_fb_agent_cfg(
    experiment_name: str = "adapt_fb_dodge",
    *,
    rank: int = 16,
    alpha: float = 1.0,
    base_checkpoint: str | Path | None = None,
    max_iterations: int = MAX_ITERATIONS,
    num_steps_per_env: int = NUM_STEPS_PER_ENV,
    save_interval: int = SAVE_INTERVAL,
    logger: str = "tensorboard",
) -> dict[str, Any]:
    """Full OnPolicyRunner train_cfg for AdaptFb dodge."""
    return {
        "seed": 42,
        "device": "cuda:0",
        "num_steps_per_env": num_steps_per_env,
        "max_iterations": max_iterations,
        "save_interval": save_interval,
        "experiment_name": experiment_name,
        "run_name": "",
        "logger": logger,
        "obs_groups": {
            "actor": ["state", "last_action", "history_actor", "goal_z"],
            "critic": ["critic"],
        },
        "actor": fb_adapter_actor(
            rank=rank, alpha=alpha, base_checkpoint=base_checkpoint
        ),
        "critic": {
            "class_name": "MLPModel",
            "hidden_dims": list(CRITIC_HIDDEN),
            "activation": "elu",
            "obs_normalization": True,
        },
        "algorithm": {
            "class_name": "PPO",
            "clip_param": 0.2,
            "entropy_coef": 0.005,
            "learning_rate": 1e-3,
            "schedule": "adaptive",
            "gamma": 0.99,
            "lam": 0.95,
            "desired_kl": 0.01,
            "max_grad_norm": 1.0,
            "value_loss_coef": 1.0,
            "use_clipped_value_loss": True,
            "num_learning_epochs": 5,
            "num_mini_batches": 4,
            "normalize_advantage_per_mini_batch": False,
            "optimizer": "adam",
            "rnd_cfg": None,
            "symmetry_cfg": None,
        },
    }
