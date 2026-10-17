"""Phase 2 acceptance: full LoRA on ResidualActor.policy; zero-init ≈ base."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import torch

pytest.importorskip("humanoidverse")

from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy, make_dummy_actor_obs
from humanoidverse.adapt_fb.core.fb_adapter import FbWithAdapter, _iter_policy_linears


def _ckpt() -> Path:
    env = os.environ.get("UFO_FB_CHECKPOINT")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2] / "UFO" / "runs" / "ufo_fb_8gpu" / "checkpoint"


@pytest.fixture(scope="module")
def adapted() -> FbWithAdapter:
    ckpt = _ckpt()
    if not (ckpt / "model" / "config.json").is_file():
        pytest.skip(f"checkpoint missing: {ckpt}")
    frozen = load_frozen_ufo_fb_policy(ckpt, device="cpu")
    return FbWithAdapter(frozen, augmentation_dim=8, rank=16, alpha=1.0)


def test_policy_linear_count(adapted: FbWithAdapter) -> None:
    # hidden_layers=6 ResidualBlocks + 1 final Block => 7 Linears
    assert len(_iter_policy_linears(adapted.actor.policy)) == 7
    assert len(adapted.adapters) == 7


def test_only_adapters_trainable(adapted: FbWithAdapter) -> None:
    trainable = [n for n, p in adapted.named_parameters() if p.requires_grad]
    assert trainable
    assert all(n.startswith("adapters.") for n in trainable)
    frozen_params = [p for n, p in adapted.named_parameters() if not p.requires_grad]
    assert frozen_params


def test_zero_init_matches_frozen_base(adapted: FbWithAdapter) -> None:
    torch.manual_seed(1)
    obs = {k: torch.randn_like(v) for k, v in make_dummy_actor_obs(4).items()}
    z = adapted.frozen.model.project_z(torch.randn(4, adapted.z_dim))
    aug = torch.randn(4, adapted.augmentation_dim)
    with torch.no_grad():
        a_base = adapted.act_base(obs, z, mean=True)
        a_ad = adapted(obs, z, aug, mean=True)
    max_abs = (a_base - a_ad).abs().max().item()
    assert max_abs < 1e-6, f"zero-init LoRA drifted from base: max_abs={max_abs}"


def test_adapter_grad_flows(adapted: FbWithAdapter) -> None:
    obs = make_dummy_actor_obs(2)
    z = adapted.frozen.model.project_z(torch.randn(2, adapted.z_dim))
    aug = torch.randn(2, adapted.augmentation_dim, requires_grad=False)
    a = adapted(obs, z, aug, mean=True)
    loss = a.pow(2).mean()
    loss.backward()
    grads = [p.grad for p in adapted.adapters.parameters() if p.requires_grad]
    assert grads and any(g is not None and g.abs().sum() > 0 for g in grads)
    # Base actor weights must not get grads
    for p in adapted.actor.parameters():
        assert p.grad is None
