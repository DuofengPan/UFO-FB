"""Phase 5: GoalBank sampling + single-z vs multi-z smoke protocol."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]
GOAL_PKL = ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "goal_inference" / "goal_reaching.pkl"


def test_goal_bank_from_synthetic() -> None:
    from humanoidverse.adapt_fb.core.goal_bank import GoalBank, GoalEntry

    entries = [
        GoalEntry("a", torch.randn(256)),
        GoalEntry("b", torch.randn(256)),
        GoalEntry("c", torch.randn(256)),
    ]
    bank = GoalBank(entries, device="cpu")
    assert len(bank) == 3
    gen = torch.Generator().manual_seed(0)
    names, z = bank.sample(8, generator=gen)
    assert len(names) == 8
    assert z.shape == (8, 256)
    assert bank.get("a").shape == (256,)


@pytest.mark.skipif(not GOAL_PKL.is_file(), reason="goal_reaching.pkl not available")
def test_goal_bank_from_ufo_pkl() -> None:
    from humanoidverse.adapt_fb.core.goal_bank import GoalBank

    bank = GoalBank.from_goal_pkl(GOAL_PKL, device="cpu")
    assert len(bank) >= 2
    assert bank.z_dim == 256
    names, z = bank.sample(4)
    assert z.shape == (4, 256)
    assert all(n in bank.names for n in names)


@pytest.mark.skipif(
    (not GOAL_PKL.is_file())
    or (
        not (ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "checkpoint" / "model" / "config.json").is_file()
        and not os.environ.get("UFO_FB_CHECKPOINT")
    ),
    reason="checkpoint or goal pkl missing",
)
def test_multiz_smoke_sees_multiple_goals() -> None:
    pytest.importorskip("humanoidverse")
    pytest.importorskip("mjlab")
    from humanoidverse.adapt_fb.multiz_smoke import run_multiz_smoke

    ckpt = os.environ.get("UFO_FB_CHECKPOINT")
    ckpt_path = Path(ckpt) if ckpt else ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "checkpoint"
    info = run_multiz_smoke(
        checkpoint_dir=ckpt_path,
        goal_pkl=GOAL_PKL,
        steps=16,
        episodes_hint=8,
        num_envs=2,
        device="cpu",
        seed=1,
    )
    assert info["bank_size"] >= 2
    assert info["single_z"]["n_unique_goals"] == 1
    assert info["multi_z"]["n_unique_goals"] >= 2
    assert "protocol" in info


def test_eval_protocol_doc_exists() -> None:
    doc = ROOT / "docs" / "multiz_eval.md"
    assert doc.is_file()
    text = doc.read_text(encoding="utf-8")
    assert "single_z" in text and "multi_z" in text
