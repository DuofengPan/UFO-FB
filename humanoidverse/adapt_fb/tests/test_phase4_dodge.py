"""Phase 4: dodge MDP units + env build + train smoke."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
import torch

ROOT = Path(__file__).resolve().parents[1]


def test_ball_asset_and_reward_import() -> None:
    from humanoidverse.adapt_fb.assets import BALL_BODY_NAME, ball_entity_cfg
    from humanoidverse.adapt_fb.tasks.dodge.mdp import ThrowBall, ball_clearance, ball_pos_b

    assert BALL_BODY_NAME == "ball"
    cfg = ball_entity_cfg()
    assert cfg is not None
    assert callable(ball_clearance)
    assert callable(ball_pos_b)
    assert ThrowBall is not None


def test_dodge_skip_reason_documented() -> None:
    import humanoidverse.adapt_fb.registration as reg

    assert "UfoFbAdapt-Dodge-AdaptFb" in reg.SKIP_REASON


def test_nominal_motions_vendored() -> None:
    motion = ROOT / "data" / "nominal_motions" / "nominal" / "stand" / "sample1" / "motion.npz"
    assert motion.is_file(), "expected vendored nominal stand clip"


@pytest.mark.skipif(
    not (ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "checkpoint" / "model" / "config.json").is_file()
    and not os.environ.get("UFO_FB_CHECKPOINT"),
    reason="UFO-FB checkpoint not available",
)
def test_train_smoke_short() -> None:
    pytest.importorskip("humanoidverse")
    pytest.importorskip("mjlab")
    from humanoidverse.adapt_fb.train_smoke import run_train_smoke

    ckpt = os.environ.get("UFO_FB_CHECKPOINT")
    ckpt_path = Path(ckpt) if ckpt else ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "checkpoint"
    goal = ROOT.parent / "UFO" / "runs" / "ufo_fb_8gpu" / "goal_inference" / "goal_reaching.pkl"
    info = run_train_smoke(
        checkpoint_dir=ckpt_path,
        goal_pkl=goal if goal.is_file() else None,
        steps=4,
        device="cpu",
        num_envs=2,
    )
    assert info["steps"] == 4
    assert info["aug_dim"] == 6
    assert info["adapter_grad_ok"] is True


def test_env_cfg_builds() -> None:
    pytest.importorskip("mjlab")
    from humanoidverse.adapt_fb.tasks.dodge.env_cfg import dodge_env_cfg

    cfg = dodge_env_cfg(play=False)
    assert "augmentation" in cfg.observations
    assert "ball_clearance" in cfg.rewards
    assert "station_height" not in cfg.rewards
    assert "station_default_pose" not in cfg.rewards
    robot = cfg.scene.entities["robot"]
    assert robot is not None
    waist = next(a for a in robot.articulation.actuators if a.target_names_expr == ("waist_yaw_joint",))
    assert abs(float(waist.stiffness) - 300.0) < 1e-3
