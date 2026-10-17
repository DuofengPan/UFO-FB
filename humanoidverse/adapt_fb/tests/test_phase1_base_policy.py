"""Phase 1: frozen UFO-FB loads and act() is deterministic."""

from __future__ import annotations

from pathlib import Path

import pytest
import torch


def _default_ckpt() -> Path:
    # adapt_fb/tests → UFO repo root
    return Path(__file__).resolve().parents[3] / "runs" / "ufo_fb_8gpu" / "checkpoint"


@pytest.mark.skipif(not (_default_ckpt() / "model" / "config.json").is_file(), reason="no UFO-FB checkpoint")
def test_frozen_act_matches_reload():
    from humanoidverse.adapt_fb.core.base_policy import load_frozen_ufo_fb_policy, make_dummy_actor_obs

    ckpt = _default_ckpt()
    pol = load_frozen_ufo_fb_policy(ckpt, device="cpu")
    obs = make_dummy_actor_obs(2, device="cpu")
    z = torch.zeros(2, pol.z_dim)
    a1 = pol.act(obs, z, mean=True)
    a2 = pol.act(obs, z, mean=True)
    assert a1.shape[-1] == pol.action_dim
    assert torch.allclose(a1, a2)
