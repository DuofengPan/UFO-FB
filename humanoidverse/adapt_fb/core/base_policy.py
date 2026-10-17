"""Load and freeze a UFO-FB checkpoint for ORCS-style adaptation.

Phase 1: expose a frozen ``act(obs, z)`` that delegates to UFO's
``FBcprAuxModel`` (or sibling FB models). F / B / actor weights are not trained
here; later phases only strap LoRA onto the actor decoder path.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn


DEFAULT_CHECKPOINT_ENV = "UFO_FB_CHECKPOINT"


@dataclass(frozen=True)
class BasePolicyInfo:
    z_dim: int
    action_dim: int
    checkpoint_dir: Path
    model_name: str


class FrozenUfoFbPolicy(nn.Module):
    """Thin wrapper: UFO FB model with all parameters frozen."""

    def __init__(self, model: nn.Module, checkpoint_dir: Path):
        super().__init__()
        self.model = model
        self.checkpoint_dir = Path(checkpoint_dir)
        self._freeze_all()
        self.eval()

    def _freeze_all(self) -> None:
        for p in self.model.parameters():
            p.requires_grad_(False)

    @property
    def z_dim(self) -> int:
        return int(self.model.cfg.archi.z_dim)

    @property
    def action_dim(self) -> int:
        # Prefer actor output; fall back to cfg / stored action_dim on model.
        actor = self.model._actor
        # ResidualActor / Actor end with Linear(action_dim)
        last = None
        for m in actor.policy.modules():
            if isinstance(m, nn.Linear):
                last = m
        if last is not None:
            return int(last.out_features)
        return int(getattr(self.model, "action_dim", 29))

    @property
    def actor(self) -> nn.Module:
        return self.model._actor

    @property
    def info(self) -> BasePolicyInfo:
        return BasePolicyInfo(
            z_dim=self.z_dim,
            action_dim=self.action_dim,
            checkpoint_dir=self.checkpoint_dir,
            model_name=type(self.model).__name__,
        )

    @torch.no_grad()
    def act(
        self,
        obs: torch.Tensor | dict[str, torch.Tensor],
        z: torch.Tensor,
        *,
        mean: bool = True,
    ) -> torch.Tensor:
        return self.model.act(obs, z, mean=mean)

    def train(self, mode: bool = True):  # type: ignore[override]
        # Keep UFO modules in eval for BN/dropout stability during adaptation
        # scaffolding; adapter modules in Phase 2 will set their own train mode.
        return super().train(False)


def resolve_checkpoint_dir(checkpoint_dir: str | Path | None = None) -> Path:
    """Resolve UFO-FB checkpoint; delegates to :mod:`humanoidverse.adapt_fb.core.artifacts`."""
    from humanoidverse.adapt_fb.core.artifacts import resolve_checkpoint_dir as _resolve

    return _resolve(checkpoint_dir)


def _ufo_load_device(device: str | torch.device) -> tuple[str, torch.device]:
    """Map ``cuda:N`` → UFO config literal ``cuda`` + concrete torch device."""
    d = torch.device(device)
    load = "cuda" if d.type == "cuda" else "cpu"
    return load, d


def load_frozen_ufo_fb_policy(
    checkpoint_dir: str | Path | None = None,
    *,
    device: str = "cpu",
) -> FrozenUfoFbPolicy:
    """Load UFO FB model from a training checkpoint directory and freeze it.

    Under multi-GPU, ``device`` must be ``cuda:{LOCAL_RANK}``. UFO's loader only
    accepts the literal ``\"cuda\"``, which would otherwise land every rank's
    ~3GB frozen weights on GPU 0 — bind the current device first.
    """
    try:
        from humanoidverse.agents.load_utils import load_model_from_checkpoint_dir
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "humanoidverse is required for Phase 1+. Install / PYTHONPATH the UFO repo."
        ) from exc

    ckpt = resolve_checkpoint_dir(checkpoint_dir)
    _, torch_dev = _ufo_load_device(device)
    if torch_dev.type == "cuda":
        torch.cuda.set_device(torch_dev)
    # UFO/safetensors treats bare "cuda" as cuda:0 always — under torchrun every
    # rank would pin ~3GB on GPU 0 and OOM. Load on CPU, then move once.
    model = load_model_from_checkpoint_dir(str(ckpt), device="cpu")
    model.to(torch_dev)
    model.eval()
    return FrozenUfoFbPolicy(model, ckpt)


def make_dummy_actor_obs(
    batch: int = 1,
    *,
    device: str | torch.device = "cpu",
    dtype: torch.dtype = torch.float32,
) -> dict[str, torch.Tensor]:
    """Minimal obs dict matching the ufo_fb_8gpu actor input_filter keys."""
    return {
        "state": torch.zeros(batch, 64, device=device, dtype=dtype),
        "last_action": torch.zeros(batch, 29, device=device, dtype=dtype),
        "history_actor": torch.zeros(batch, 372, device=device, dtype=dtype),
        # Present in obs_space; unused by actor filter but kept for normalizer safety.
        "privileged_state": torch.zeros(batch, 463, device=device, dtype=dtype),
    }
