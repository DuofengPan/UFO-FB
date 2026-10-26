#!/usr/bin/env python
"""Minimal 2-GPU NCCL smoke without MuJoCo/Warp."""
from __future__ import annotations

import os
import torch
import torch.distributed as dist


def main() -> None:
    local_rank = int(os.environ["LOCAL_RANK"])
    rank = int(os.environ["RANK"])
    world = int(os.environ["WORLD_SIZE"])
    torch.cuda.set_device(local_rank)
    dist.init_process_group(backend="nccl")
    print(f"[rank {rank}] init ok device={torch.cuda.current_device()}", flush=True)

    x = torch.randn(8 * 1024 * 1024, device=f"cuda:{local_rank}")  # 32MB
    dist.broadcast(x, src=0)
    torch.cuda.synchronize()
    print(f"[rank {rank}] broadcast 32MB ok sum={x.sum().item():.4f}", flush=True)

    dist.all_reduce(x)
    torch.cuda.synchronize()
    print(f"[rank {rank}] all_reduce ok sum={x.sum().item():.4f}", flush=True)

    # mimic many small broadcasts like broadcast_module_state
    for i in range(200):
        t = torch.randn(4096, device=f"cuda:{local_rank}")
        dist.broadcast(t, src=0)
    torch.cuda.synchronize()
    print(f"[rank {rank}] 200x small broadcast ok", flush=True)

    dist.destroy_process_group()
    print(f"[rank {rank}] DONE", flush=True)


if __name__ == "__main__":
    main()
