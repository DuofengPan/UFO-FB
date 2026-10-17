"""Resolve UFO-FB checkpoint + goal-bank paths.

Prefer env overrides, then this UFO checkout's ``runs/ufo_fb_8gpu``, then
optional ``artifacts/`` under the UFO repo root (HF sync layout).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CHECKPOINT_ENV = "UFO_FB_CHECKPOINT"
DEFAULT_GOAL_PKL_ENV = "UFO_FB_GOAL_PKL"
DEFAULT_GOAL_BANK_ENV = "UFO_FB_GOAL_BANK"

# humanoidverse/adapt_fb/core → UFO repo root
_UFO_ROOT = Path(__file__).resolve().parents[3]
_ARTIFACTS_DIR = _UFO_ROOT / "artifacts"
_DEFAULT_RUN = _UFO_ROOT / "runs" / "ufo_fb_8gpu"


@dataclass(frozen=True)
class ArtifactPaths:
    checkpoint_dir: Path
    goal_pkl: Path
    artifacts_dir: Path = _ARTIFACTS_DIR
    goal_bank_id: str | None = None


def artifacts_dir() -> Path:
    return _ARTIFACTS_DIR


def ufo_repo_root() -> Path:
    return _UFO_ROOT


def _load_manifest(art: Path | None = None) -> dict | None:
    path = (art or _ARTIFACTS_DIR) / "manifest.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def active_goal_bank_id() -> str | None:
    env = os.environ.get(DEFAULT_GOAL_BANK_ENV)
    if env:
        return env.strip() or None
    manifest = _load_manifest()
    if not manifest:
        return None
    return manifest.get("default_goal_bank")


def default_checkpoint_candidates() -> list[Path]:
    return [
        _DEFAULT_RUN / "checkpoint",
        _ARTIFACTS_DIR / "checkpoint",
    ]


def default_goal_pkl_candidates() -> list[Path]:
    paths: list[Path] = [
        _DEFAULT_RUN / "goal_inference" / "goal_reaching.pkl",
    ]
    bank = active_goal_bank_id()
    if bank:
        paths.append(_ARTIFACTS_DIR / "goals" / bank / "goal_reaching.pkl")
    paths.append(_ARTIFACTS_DIR / "goal_reaching.pkl")
    goals_root = _ARTIFACTS_DIR / "goals"
    if goals_root.is_dir():
        for p in sorted(goals_root.glob("*/goal_reaching.pkl")):
            if p not in paths:
                paths.append(p)
    return paths


def _first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.is_dir() or p.is_file():
            return p.resolve()
    return None


def resolve_checkpoint_dir(checkpoint_dir: str | Path | None = None) -> Path:
    if checkpoint_dir is not None:
        path = Path(checkpoint_dir).expanduser().resolve()
    else:
        env = os.environ.get(DEFAULT_CHECKPOINT_ENV)
        if env:
            path = Path(env).expanduser().resolve()
        else:
            found = _first_existing(default_checkpoint_candidates())
            if found is None:
                raise FileNotFoundError(
                    "UFO-FB checkpoint not found. Train / place a run at "
                    f"runs/ufo_fb_8gpu/checkpoint, or set {DEFAULT_CHECKPOINT_ENV}. Tried: "
                    + ", ".join(str(p) for p in default_checkpoint_candidates())
                )
            path = found
    if not path.is_dir():
        raise FileNotFoundError(f"UFO-FB checkpoint not a directory: {path}")
    if not (path / "model" / "config.json").is_file():
        raise FileNotFoundError(f"Missing model/config.json under {path}")
    return path


def resolve_goal_pkl(goal_pkl: str | Path | None = None) -> Path:
    if goal_pkl is not None:
        path = Path(goal_pkl).expanduser().resolve()
    else:
        env = os.environ.get(DEFAULT_GOAL_PKL_ENV)
        if env:
            path = Path(env).expanduser().resolve()
        else:
            found = _first_existing(default_goal_pkl_candidates())
            if found is None:
                raise FileNotFoundError(
                    "goal_reaching.pkl not found. Run goal_inference on the FB run, "
                    f"or set {DEFAULT_GOAL_PKL_ENV}."
                )
            path = found
    if not path.is_file():
        raise FileNotFoundError(f"goal pkl not a file: {path}")
    return path


def resolve_artifacts(
    checkpoint_dir: str | Path | None = None,
    goal_pkl: str | Path | None = None,
) -> ArtifactPaths:
    goal = resolve_goal_pkl(goal_pkl)
    bank_id = active_goal_bank_id()
    if bank_id is None:
        parts = goal.parts
        if "goals" in parts:
            i = parts.index("goals")
            if i + 1 < len(parts):
                bank_id = parts[i + 1]
    return ArtifactPaths(
        checkpoint_dir=resolve_checkpoint_dir(checkpoint_dir),
        goal_pkl=goal,
        artifacts_dir=_ARTIFACTS_DIR,
        goal_bank_id=bank_id,
    )


def resolve_model_folder(checkpoint_dir: str | Path | None = None) -> Path:
    """UFO train run folder: ``config.json`` + ``checkpoint/`` (goal_inference layout)."""
    ckpt = resolve_checkpoint_dir(checkpoint_dir)
    if ckpt.name == "checkpoint" and (ckpt.parent / "config.json").is_file():
        return ckpt.parent.resolve()
    if (ckpt / "config.json").is_file() and (ckpt / "checkpoint").is_dir():
        return ckpt.resolve()
    if (_DEFAULT_RUN / "config.json").is_file() and (_DEFAULT_RUN / "checkpoint").is_dir():
        return _DEFAULT_RUN.resolve()
    raise FileNotFoundError(
        f"Cannot resolve UFO model folder (need config.json next to checkpoint/). "
        f"checkpoint_dir={ckpt}. Tried {_DEFAULT_RUN}."
    )
