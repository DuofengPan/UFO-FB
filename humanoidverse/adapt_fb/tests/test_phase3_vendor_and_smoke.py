"""Phase 3: vendored rsl_rl import + registration module + policy play smoke."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]


def test_deps_lock_pins_rsl_rl() -> None:
    lock = json.loads((ROOT / "deps.lock.json").read_text())
    assert lock["rsl_rl"]["sha"] == "215b6f4ceda569d2ca39df64dd679b9af15375cb"
    assert (ROOT / lock["rsl_rl"]["path"] / "rsl_rl").is_dir()


def test_vendored_rsl_rl_import() -> None:
    from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl

    path = ensure_vendored_rsl_rl()
    import rsl_rl
    from rsl_rl.modules.mlp_with_adapter import Adapter
    from rsl_rl.models.sonic_adapter_model import SonicWithAdapterModel  # noqa: F401

    assert Path(rsl_rl.__file__).resolve().is_relative_to(path.resolve()) or str(path) in str(
        Path(rsl_rl.__file__).resolve()
    )
    # Zero-init adapter constructible
    a = Adapter(8, 16, rank=4, alpha=1.0)
    y = a(torch.randn(2, 8))
    assert y.shape == (2, 16)
    assert float(y.abs().max()) == 0.0


def test_registration_module_imports() -> None:
    import humanoidverse.adapt_fb.registration as reg

    assert isinstance(reg.SKIP_REASON, dict)


@pytest.mark.skipif(
    not (ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "checkpoint" / "model" / "config.json").is_file()
    and not os.environ.get("UFO_FB_CHECKPOINT"),
    reason="UFO-FB checkpoint not available",
)
def test_play_smoke_with_offline_z() -> None:
    pytest.importorskip("humanoidverse")
    from humanoidverse.adapt_fb.play_smoke import run_play_smoke

    ckpt = os.environ.get("UFO_FB_CHECKPOINT")
    ckpt_path = Path(ckpt) if ckpt else ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "checkpoint"
    goal = ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "goal_inference" / "goal_reaching.pkl"
    info = run_play_smoke(
        checkpoint_dir=ckpt_path,
        goal_pkl=goal if goal.is_file() else None,
        steps=8,
        augmentation_dim=8,
        device="cpu",
    )
    assert info["steps"] == 8
    assert info["action_shape"] == (8, 29)
    assert "rsl_rl" in info["rsl_rl_file"]
    assert (ROOT / "dependencies" / "rsl_rl").resolve() in Path(info["rsl_rl_file"]).resolve().parents
