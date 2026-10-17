"""rsl_rl-compatible actor: frozen UFO-FB + LoRA (``FbWithAdapter``).

Observation contract (TensorDict groups)::

    state, last_action, history_actor  — UFO proprio (obs bridge)
    goal_z                             — offline goal embedding
    augmentation                       — privileged ball (LoRA condition)

Only adapter (+ optional distribution std) parameters are trainable.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
from tensordict import TensorDict

from rsl_rl.modules import AmpMixin, EmpiricalNormalization, HiddenState
from rsl_rl.modules.distribution import Distribution
from rsl_rl.utils import resolve_callable

from humanoidverse.adapt_fb.core.artifacts import resolve_checkpoint_dir
from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy
from humanoidverse.adapt_fb.core.fb_adapter import FbWithAdapter


class FbWithAdapterModel(AmpMixin, nn.Module):
    """PPO actor wrapping :class:`FbWithAdapter`."""

    is_recurrent: bool = False

    def __init__(
        self,
        obs: TensorDict,
        obs_groups: dict[str, list[str]],
        obs_set: str,
        output_dim: int,
        *,
        adapter_obs_group: str = "augmentation",
        goal_obs_group: str = "goal_z",
        rank: int = 16,
        alpha: float = 1.0,
        base_checkpoint: str | Path | None = None,
        distribution_cfg: dict | None = None,
        obs_normalization: bool = True,
        **_unused: Any,
    ) -> None:
        super().__init__()
        self.obs_groups = list(obs_groups[obs_set])
        self.adapter_obs_group = adapter_obs_group
        self.goal_obs_group = goal_obs_group
        self.output_dim = int(output_dim)

        ckpt = resolve_checkpoint_dir(base_checkpoint)
        # Bind load to the env's GPU (cuda:N). Passing bare "cuda" piles all ranks onto GPU 0.
        obs_device = obs[adapter_obs_group].device
        device = str(obs_device)
        frozen = load_frozen_ufo_fb_policy(ckpt, device=device)
        if frozen.action_dim != output_dim:
            raise ValueError(f"action dim mismatch: UFO={frozen.action_dim} env={output_dim}")

        aug_dim = int(obs[adapter_obs_group].shape[-1])
        self.adapted = FbWithAdapter(frozen, augmentation_dim=aug_dim, rank=rank, alpha=alpha)
        self.adapted.to(device)

        self.adapter_normalizer: nn.Module
        if obs_normalization:
            self.adapter_normalizer = EmpiricalNormalization(aug_dim)
        else:
            self.adapter_normalizer = nn.Identity()

        if distribution_cfg is None:
            distribution_cfg = {
                "class_name": "GaussianDistribution",
                "init_std": float(frozen.model.cfg.actor_std),
                "std_type": "scalar",
                "learn_std": False,
            }
        else:
            distribution_cfg = dict(distribution_cfg)
        dist_cls: type[Distribution] = resolve_callable(distribution_cfg.pop("class_name"))  # type: ignore
        self.distribution: Distribution = dist_cls(output_dim, **distribution_cfg)

        self._print_param_summary()

    def _print_param_summary(self) -> None:
        def _count(m: nn.Module) -> tuple[int, int]:
            tot = sum(p.numel() for p in m.parameters())
            tr = sum(p.numel() for p in m.parameters() if p.requires_grad)
            return tr, tot

        sep = "─" * 62
        print(f"\n{sep}")
        print("  FbWithAdapterModel  (UFO-FB base frozen)")
        print(sep)
        for name, mod in [
            ("adapters", self.adapted.adapters),
            ("adapter normalizer", self.adapter_normalizer),
            ("distribution", self.distribution),
            ("frozen UFO model", self.adapted.frozen),
        ]:
            tr, tot = _count(mod)
            print(f"  {name:<28} {tr:>12,} {tot:>12,}")
        print(f"{sep}\n")

    def _actor_obs_dict(self, obs: TensorDict) -> dict[str, torch.Tensor]:
        return {
            "state": obs["state"],
            "last_action": obs["last_action"],
            "history_actor": obs["history_actor"],
        }

    def _adapter_latent(self, obs: TensorDict) -> torch.Tensor:
        return self.adapter_normalizer(obs[self.adapter_obs_group])

    def _mean_action(self, obs: TensorDict) -> torch.Tensor:
        z = obs[self.goal_obs_group]
        aug = self._adapter_latent(obs)
        return self.adapted(self._actor_obs_dict(obs), z, aug, mean=True)

    def forward(
        self,
        obs: TensorDict,
        masks: torch.Tensor | None = None,
        hidden_state: HiddenState = None,
        stochastic_output: bool = False,
    ) -> torch.Tensor:
        del masks, hidden_state
        with self._amp_body():
            mu = self._mean_action(obs)
        mu = self._head_input(mu)
        self.distribution.update(mu)
        if stochastic_output:
            return self.distribution.sample()
        return self.distribution.deterministic_output(mu)

    def reset(self, dones: torch.Tensor | None = None, hidden_state: HiddenState = None) -> None:
        del dones, hidden_state

    def get_hidden_state(self) -> HiddenState:
        return None

    def detach_hidden_state(self, dones: torch.Tensor | None = None) -> None:
        del dones

    @property
    def output_mean(self) -> torch.Tensor:
        return self.distribution.mean

    @property
    def output_std(self) -> torch.Tensor:
        return self.distribution.std

    @property
    def output_entropy(self) -> torch.Tensor:
        return self.distribution.entropy

    @property
    def output_distribution_params(self) -> tuple[torch.Tensor, ...]:
        return self.distribution.params

    def get_output_log_prob(self, outputs: torch.Tensor) -> torch.Tensor:
        return self.distribution.log_prob(outputs)

    def get_kl_divergence(
        self, old_params: tuple[torch.Tensor, ...], new_params: tuple[torch.Tensor, ...]
    ) -> torch.Tensor:
        return self.distribution.kl_divergence(old_params, new_params)

    def update_normalization(self, obs: TensorDict) -> None:
        if isinstance(self.adapter_normalizer, EmpiricalNormalization):
            self.adapter_normalizer.update(obs[self.adapter_obs_group])
