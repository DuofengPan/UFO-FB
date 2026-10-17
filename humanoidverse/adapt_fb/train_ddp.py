"""Multi-GPU entry for AdaptFb train (use with torchrun).

Isolates each rank onto one physical GPU **before** importing torch / warp::

    torchrun --standalone --nproc_per_node=8 -m humanoidverse.adapt_fb.train_ddp \\
      --num-envs 4096 --max-iterations 8000 \\
      --log-dir runs/adapt_fb_dodge_8gpu

Each process only sees ``cuda:0`` (its assigned card). rsl_rl still keys off
``LOCAL_RANK`` for NCCL; device checks are relaxed in vendored runner.
"""

from __future__ import annotations

import os
import sys


def _isolate_gpu() -> None:
    if "LOCAL_RANK" not in os.environ:
        return
    local_rank = int(os.environ["LOCAL_RANK"])
    # Must run before torch / warp CUDA init.
    os.environ["CUDA_VISIBLE_DEVICES"] = str(local_rank)
    os.environ["MUJOCO_EGL_DEVICE_ID"] = "0"
    # Tell train.py to use the only visible device.
    os.environ["UFO_FB_DDP_ISOLATED"] = "1"


_isolate_gpu()

from humanoidverse.adapt_fb.train import main  # noqa: E402


if __name__ == "__main__":
    # Drop any --device from CLI; isolated workers always use cuda:0.
    argv = [a for a in (sys.argv[1:] if len(sys.argv) > 1 else []) if not a.startswith("--device")]
    # Ensure device flag
    filtered: list[str] = []
    skip = False
    for a in argv:
        if skip:
            skip = False
            continue
        if a == "--device":
            skip = True
            continue
        if a.startswith("--device="):
            continue
        filtered.append(a)
    filtered.extend(["--device", "cuda:0"])
    main(filtered)
