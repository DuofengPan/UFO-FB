"""ORCS-aligned LoRA wrap of UFO-FB ``ResidualActor``.

Frozen path (unchanged contract)::

    obs --input_filter--> embed_s / embed_z(obs,z) --cat--> policy --tanh--> mu

Adapter stream (only trainable conditioning)::

    augmentation --> first LoRA (on first policy Linear)
    hidden state  --> subsequent LoRAs (same interleaving as ``MLPWithAdapter``)

Embeddings stay frozen (analogous to SONIC encoder/FSQ not taking aug).
Only ``actor.policy`` Linears receive LoRA (analogous to ``adapt_decoder=True``).
"""

from __future__ import annotations

from typing import Iterable

import torch
import torch.nn as nn

from humanoidverse.adapt_fb.core.base_policy import FrozenUfoFbPolicy
from humanoidverse.adapt_fb.core.lora import Adapter


def _iter_policy_linears(policy: nn.Sequential) -> list[nn.Linear]:
    """Depth-order Linear modules inside ResidualActor.policy blocks."""
    linears: list[nn.Linear] = []
    for block in policy:
        # ResidualBlock / Block both expose ``mlp: Sequential`` containing Linear.
        mlp = getattr(block, "mlp", None)
        if mlp is None:
            raise TypeError(f"Unexpected policy block type: {type(block)}")
        for mod in mlp:
            if isinstance(mod, nn.Linear):
                linears.append(mod)
    if not linears:
        raise RuntimeError("No Linear modules found in actor.policy")
    return linears


class FbWithAdapter(nn.Module):
    """Frozen UFO-FB policy + LoRA on the actor ``policy`` stack."""

    def __init__(
        self,
        frozen: FrozenUfoFbPolicy,
        *,
        augmentation_dim: int,
        rank: int = 16,
        alpha: float = 1.0,
        std: float | None = None,
    ) -> None:
        super().__init__()
        self.frozen = frozen
        self.actor = frozen.actor
        self.augmentation_dim = int(augmentation_dim)
        self.rank = int(rank)
        self.alpha = float(alpha)
        self.std = float(frozen.model.cfg.actor_std if std is None else std)

        # Freeze everything under the UFO model (embeddings + policy weights).
        for p in self.frozen.parameters():
            p.requires_grad_(False)

        linears = _iter_policy_linears(self.actor.policy)
        self._policy_linears = linears
        adapters: list[Adapter] = []
        for i, lin in enumerate(linears):
            in_dim = self.augmentation_dim if i == 0 else int(lin.in_features)
            out_dim = int(lin.out_features)
            adapters.append(Adapter(in_dim, out_dim, rank=self.rank, alpha=self.alpha))
        self.adapters = nn.ModuleList(adapters)

        # Trainable: adapters only.
        for p in self.adapters.parameters():
            p.requires_grad_(True)

    @property
    def z_dim(self) -> int:
        return self.frozen.z_dim

    @property
    def action_dim(self) -> int:
        return self.frozen.action_dim

    def trainable_parameters(self) -> Iterable[nn.Parameter]:
        return self.adapters.parameters()

    def _embedding(self, obs: dict[str, torch.Tensor] | torch.Tensor, z: torch.Tensor) -> torch.Tensor:
        # Match ResidualActor.forward embedding path (frozen).
        obs_f = self.actor.input_filter(obs)
        z_embedding = self.actor.embed_z(torch.cat([obs_f, z], dim=-1))
        s_embedding = self.actor.embed_s(obs_f)
        return torch.cat([s_embedding, z_embedding], dim=-1)

    def _policy_forward(self, embedding: torch.Tensor, augmentation: torch.Tensor) -> torch.Tensor:
        """Run ResidualActor.policy with ORCS-style interleaved LoRA."""
        x = embedding
        linear_idx = 0
        for block in self.actor.policy:
            mlp = block.mlp
            # Expect LN -> Linear -> [Mish?]
            if len(mlp) < 2 or not isinstance(mlp[1], nn.Linear):
                raise RuntimeError(f"Unexpected mlp layout: {mlp}")
            h = mlp[0](x)  # LayerNorm
            lin: nn.Linear = mlp[1]
            assert lin is self._policy_linears[linear_idx]
            adapter = self.adapters[linear_idx]
            cond = augmentation if linear_idx == 0 else h
            y = lin(h) + adapter(cond)
            linear_idx += 1
            # Optional Mish / activations after Linear
            for mod in mlp[2:]:
                y = mod(y)
            # ResidualBlock: x + mlp(x). Block: mlp(x) only.
            # Detect residual by class name to avoid hard import at module import time.
            if block.__class__.__name__ == "ResidualBlock":
                x = x + y
            else:
                x = y
        assert linear_idx == len(self._policy_linears)
        return x

    def forward(
        self,
        obs: dict[str, torch.Tensor] | torch.Tensor,
        z: torch.Tensor,
        augmentation: torch.Tensor,
        *,
        mean: bool = True,
    ) -> torch.Tensor:
        if augmentation.shape[-1] != self.augmentation_dim:
            raise ValueError(
                f"augmentation last dim {augmentation.shape[-1]} != expected {self.augmentation_dim}"
            )
        # Obs normalizer from UFO model (frozen eval path).
        obs_n = self.frozen.model._normalize(obs)
        emb = self._embedding(obs_n, z)
        mu = torch.tanh(self._policy_forward(emb, augmentation))
        if mean:
            return mu
        std = torch.ones_like(mu) * self.std
        return mu + std * torch.randn_like(mu)

    @torch.no_grad()
    def act_base(self, obs: dict[str, torch.Tensor], z: torch.Tensor, *, mean: bool = True) -> torch.Tensor:
        """Frozen UFO act (no adapter) for bit-exact checks."""
        return self.frozen.act(obs, z, mean=mean)
