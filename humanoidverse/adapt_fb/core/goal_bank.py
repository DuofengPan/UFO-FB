"""Offline goal-``z`` bank for multi-pose AdaptFb training / eval.

Phase 5: sample embeddings from a ``goal_reaching.pkl`` produced by UFO
``goal_inference`` (keys ``{motion_name}_{frame}``). F/B stay frozen; only the
LoRA adapter is trained while ``z`` switches across the bank.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import torch


@dataclass(frozen=True)
class GoalEntry:
    name: str
    z: torch.Tensor  # (z_dim,)


class GoalBank:
    """In-memory goal embedding table with sampling helpers."""

    def __init__(self, entries: Sequence[GoalEntry], *, device: str | torch.device = "cpu"):
        if not entries:
            raise ValueError("GoalBank requires at least one entry")
        self.device = torch.device(device)
        self.names: list[str] = [e.name for e in entries]
        zs = [e.z.detach().to(self.device, dtype=torch.float32).reshape(-1) for e in entries]
        z_dim = zs[0].numel()
        if any(z.numel() != z_dim for z in zs):
            raise ValueError("All goal embeddings must share the same z_dim")
        self._z = torch.stack(zs, dim=0)  # (N, z_dim)
        self.z_dim = int(z_dim)

    def __len__(self) -> int:
        return len(self.names)

    @classmethod
    def from_goal_pkl(
        cls,
        path: str | Path,
        *,
        device: str | torch.device = "cpu",
        names: Sequence[str] | None = None,
    ) -> GoalBank:
        import joblib

        path = Path(path)
        raw: dict[str, Any] = joblib.load(path)
        if not isinstance(raw, dict) or not raw:
            raise ValueError(f"Expected non-empty dict in {path}")
        keys = list(names) if names is not None else sorted(raw.keys())
        missing = [k for k in keys if k not in raw]
        if missing:
            raise KeyError(f"Goals not in pkl: {missing[:5]}{'...' if len(missing) > 5 else ''}")
        entries = [
            GoalEntry(name=k, z=torch.as_tensor(raw[k], dtype=torch.float32).reshape(-1)) for k in keys
        ]
        return cls(entries, device=device)

    def sample(
        self,
        batch: int,
        *,
        generator: torch.Generator | None = None,
    ) -> tuple[list[str], torch.Tensor]:
        """Sample ``batch`` goals with replacement; return names and ``(B, z_dim)``."""
        idx = torch.randint(0, len(self), (batch,), generator=generator, device="cpu")
        names = [self.names[int(i)] for i in idx.tolist()]
        z = self._z[idx.to(self._z.device)]
        return names, z

    def get(self, name: str) -> torch.Tensor:
        try:
            i = self.names.index(name)
        except ValueError as exc:
            raise KeyError(name) from exc
        return self._z[i]

    def get_index(self, index: int) -> tuple[str, torch.Tensor]:
        i = int(index) % len(self)
        return self.names[i], self._z[i]

    def as_dict(self) -> dict[str, torch.Tensor]:
        return {n: self._z[i].clone() for i, n in enumerate(self.names)}
