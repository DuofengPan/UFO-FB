"""LoRA-style adapters (ORCS / rsl_rl ``Adapter`` semantics).

Adapted from ``rsl_rl.modules.mlp_with_adapter.Adapter`` (BSD-3-Clause,
ETH Zurich / NVIDIA; also used by ORCS). Attribution: see repository NOTICE /
THIRD_PARTY_NOTICES.md.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class Adapter(nn.Module):
    """Zero-initialized LoRA (or full-rank) delta added to a frozen Linear output."""

    def __init__(self, input_dim: int, output_dim: int, rank: int = 16, alpha: float = 1.0) -> None:
        super().__init__()
        self.low_rank = 0 < rank < min(input_dim, output_dim)
        if self.low_rank:
            self.down = nn.Linear(input_dim, rank, bias=False)
            self.up = nn.Linear(rank, output_dim, bias=False)
            nn.init.normal_(self.down.weight, std=1.0 / rank**0.5)
            nn.init.zeros_(self.up.weight)
            self.scale = alpha / float(rank)
        else:
            self.delta = nn.Linear(input_dim, output_dim, bias=False)
            nn.init.zeros_(self.delta.weight)
            self.scale = float(alpha)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.low_rank:
            return self.scale * self.up(self.down(x))
        return self.scale * self.delta(x)
