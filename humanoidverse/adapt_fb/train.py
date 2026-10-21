"""Train AdaptFb dodge: frozen UFO-FB + LoRA via vendored rsl_rl PPO.

Uses the **same UFO MJLab host** as play (``build_ufo_vector_env`` + ball inject),
so train/play share proprio, action scaling, and motion-reset plant.

Multi-GPU (rsl_rl DDP)::

    torchrun --standalone --nproc_per_node=8 -m humanoidverse.adapt_fb.train \\
      --num-envs 4096 --max-iterations 8000 --log-dir runs/adapt_fb_dodge_8gpu

Each rank owns ``num_envs`` sims on ``cuda:{LOCAL_RANK}``. Effective samples/iter
scale with ``WORLD_SIZE``; shorten ``--max-iterations`` ≈ linearly for similar
total experience and much lower wall time.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import torch

from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl

# Bind vendored rsl_rl before any other AdaptFb import that may pull it in.
ensure_vendored_rsl_rl()

from humanoidverse.adapt_fb.core.artifacts import resolve_artifacts, resolve_model_folder
from humanoidverse.adapt_fb.core.goal_bank import GoalBank
from humanoidverse.adapt_fb.core.rl import adapt_fb_agent_cfg
from humanoidverse.adapt_fb.core.ufo_host import UfoHostTrainEnv, build_ufo_vector_env
from humanoidverse.adapt_fb.tasks.dodge.env_cfg import EPISODE_LENGTH_S


def _resolve_device(cli_device: str) -> str:
    """Resolve train device.

    - ``train_ddp`` / ``UFO_FB_DDP_ISOLATED=1``: one visible GPU → always ``cuda:0``.
    - Plain torchrun without isolation: ``cuda:{LOCAL_RANK}`` (legacy; prefer train_ddp).
    - Single-process: honor CLI.
    """
    if os.environ.get("UFO_FB_DDP_ISOLATED") == "1":
        if torch.cuda.is_available():
            torch.cuda.set_device(0)
        return "cuda:0"
    if "LOCAL_RANK" in os.environ:
        local_rank = int(os.environ["LOCAL_RANK"])
        os.environ.setdefault("MUJOCO_EGL_DEVICE_ID", str(local_rank))
        if torch.cuda.is_available():
            torch.cuda.set_device(local_rank)
        return f"cuda:{local_rank}"
    if cli_device.startswith("cuda") and not torch.cuda.is_available():
        print("CUDA unavailable; falling back to cpu")
        return "cpu"
    if cli_device.startswith("cuda:") and torch.cuda.is_available():
        torch.cuda.set_device(int(cli_device.split(":")[1]))
    return cli_device


def run_train(
    *,
    num_envs: int,
    max_iterations: int,
    device: str,
    log_dir: Path | None,
    multi_z: bool,
    checkpoint_dir: Path | None,
    goal_pkl: Path | None,
    data_path: Path | None = None,
    max_episode_length_s: float = EPISODE_LENGTH_S,
    seed: int = 42,
    resume: Path | None = None,
) -> Path:
    ensure_vendored_rsl_rl()
    import rsl_rl

    vendor_root = Path(ensure_vendored_rsl_rl()).resolve()
    if not Path(rsl_rl.__file__).resolve().is_relative_to(vendor_root):
        raise ImportError(
            f"rsl_rl resolved to {rsl_rl.__file__}, expected under {vendor_root}. "
            "Unload site-packages rsl_rl or check PYTHONPATH."
        )
    from rsl_rl.runners import OnPolicyRunner

    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    world_size = int(os.environ.get("WORLD_SIZE", "1"))
    rank_seed = seed + local_rank

    arts = resolve_artifacts(checkpoint_dir, goal_pkl)
    model_folder = resolve_model_folder(arts.checkpoint_dir)
    bank = GoalBank.from_goal_pkl(arts.goal_pkl, device=device)

    vector = build_ufo_vector_env(
        model_folder,
        device=device,
        num_envs=num_envs,
        data_path=data_path,
        max_episode_length_s=max_episode_length_s,
        headless=True,
        ball="throw",
        train=True,
    )
    # Seed the underlying mjlab env for rank diversity.
    if hasattr(vector._env.mjlab_env, "seed"):
        vector._env.mjlab_env.seed(rank_seed)
    vec = UfoHostTrainEnv(vector, bank, ball="throw", multi_z=multi_z)

    train_cfg = adapt_fb_agent_cfg(
        "adapt_fb_dodge",
        base_checkpoint=arts.checkpoint_dir,
        max_iterations=max_iterations,
    )
    train_cfg["seed"] = rank_seed
    train_cfg["device"] = device

    if log_dir is None:
        log_dir = Path("runs") / "adapt_fb_dodge"
    if local_rank == 0:
        log_dir.mkdir(parents=True, exist_ok=True)

    if world_size > 1 and local_rank == 0:
        print(
            f"[INFO] multi-GPU world_size={world_size}, envs/rank={num_envs}, "
            f"samples/iter≈{num_envs * 24 * world_size} (UFO host + ThrowBall)"
        )
    if local_rank == 0:
        print(
            f"[INFO] AdaptFb train plant=UFO host model_folder={model_folder} "
            f"episode_length_s={max_episode_length_s} multi_z={multi_z}",
            flush=True,
        )

    runner = OnPolicyRunner(vec, train_cfg, log_dir=str(log_dir), device=device)
    if resume is not None:
        resume = Path(resume).expanduser().resolve()
        if not resume.is_file():
            raise FileNotFoundError(f"--resume not found: {resume}")
        runner.load(str(resume), map_location=device)
        if local_rank == 0:
            print(
                f"[INFO] resumed from {resume} at iter={runner.current_learning_iteration}; "
                f"will run +{max_iterations} iters "
                f"(→ {runner.current_learning_iteration + max_iterations})",
                flush=True,
            )
    runner.learn(num_learning_iterations=max_iterations, init_at_random_ep_len=True)
    out = log_dir / f"model_{runner.current_learning_iteration}.pt"
    vec.close()
    return out


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--num-envs", type=int, default=64, help="Environments per GPU/rank")
    p.add_argument("--max-iterations", type=int, default=500)
    p.add_argument("--device", type=str, default="cuda:0", help="Ignored under torchrun (uses LOCAL_RANK)")
    p.add_argument("--log-dir", type=Path, default=None)
    p.add_argument(
        "--single-z",
        action="store_true",
        help="Fix z to the first GoalBank entry for all envs (default: sample a "
        "new goal each episode reset — multi-z dodge).",
    )
    p.add_argument("--checkpoint-dir", type=Path, default=None)
    p.add_argument("--goal-pkl", type=Path, default=None)
    p.add_argument("--data-path", type=Path, default=None, help="UFO motion pkl (default: lafan clip)")
    p.add_argument(
        "--max-episode-length-s",
        type=float,
        default=EPISODE_LENGTH_S,
        help=f"Episode length in seconds (default {EPISODE_LENGTH_S}, same as legacy dodge)",
    )
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--resume",
        type=Path,
        default=None,
        help="rsl_rl model_*.pt to resume (loads actor/critic/optimizer + iter). "
        "--max-iterations is ADDITIONAL iters after the resumed iter.",
    )
    args = p.parse_args(argv)

    device = _resolve_device(args.device)
    out = run_train(
        num_envs=args.num_envs,
        max_iterations=args.max_iterations,
        device=device,
        log_dir=args.log_dir,
        multi_z=not args.single_z,
        checkpoint_dir=args.checkpoint_dir,
        goal_pkl=args.goal_pkl,
        data_path=args.data_path,
        max_episode_length_s=args.max_episode_length_s,
        seed=args.seed,
        resume=args.resume,
    )
    if int(os.environ.get("LOCAL_RANK", "0")) == 0:
        print(f"saved: {out}")


if __name__ == "__main__":
    main()
