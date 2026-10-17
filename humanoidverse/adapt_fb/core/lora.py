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
        # Clamp rank into (0, min(in,out)) so tiny adapter inputs (e.g. aug_dim=6
        # with rank=16) stay low-rank LoRA instead of silently becoming a full
        # Linear(6, 2048) — that path overfit hard in the first AdaptFb run.
        max_rank = min(int(input_dim), int(output_dim))
        eff_rank = int(rank)
        if max_rank <= 1:
            self.low_rank = False
        else:
            eff_rank = max(1, min(eff_rank, max_rank - 1))
            self.low_rank = eff_rank > 0
        if self.low_rank:
            self.down = nn.Linear(input_dim, eff_rank, bias=False)
            self.up = nn.Linear(eff_rank, output_dim, bias=False)
            nn.init.normal_(self.down.weight, std=1.0 / eff_rank**0.5)
            nn.init.zeros_(self.up.weight)
            self.scale = alpha / float(eff_rank)
            self.rank = eff_rank
        else:
            self.delta = nn.Linear(input_dim, output_dim, bias=False)
            nn.init.zeros_(self.delta.weight)
            self.scale = float(alpha)
            self.rank = 0

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.low_rank:
            return self.scale * self.up(self.down(x))
        return self.scale * self.delta(x)
