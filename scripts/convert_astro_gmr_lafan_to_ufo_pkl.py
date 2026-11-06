#!/usr/bin/env python3
"""Convert Astro GMR LaFAN1 per-motion PKLs into UFO full + near-10s PKLs.

GMR pack layout (lafan1_gmr/*.pkl) stores:
  root_pos [T,3], root_rot [T,4] (xyzw), dof_pos [T,30], fps, ...

DOF order (verified by MuJoCo FK against local_body_pos):
  waist_yaw/pitch/roll, head, left arm x7, right arm x7, left leg x6, right leg x6

For UFO Astro P2 29-DoF (fixed head) we drop head_joint and reorder into
RobotSpec.control_joint_names, then emit the same two artifacts as G1 LaFAN:
  ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof.pkl
  ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof_10s-clipped.pkl
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from omegaconf import OmegaConf

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from ufo.motion.formats import RobotStateMotion, clip_ufo_motion_dict, dump_ufo_pkl, robot_state_to_ufo_motion
from ufo.tools.robot_config import load_robot_spec


def _gmr_astro_30_joint_names() -> list[str]:
    """Verified against MuJoCo FK (pairwise body error ~0.008m on shared links)."""

    return [
        "waist_yaw_joint",
        "waist_pitch_joint",
        "waist_roll_joint",
        "head_joint",
        "left_shoulder_pitch_joint",
        "left_shoulder_roll_joint",
        "left_shoulder_yaw_joint",
        "left_elbow_joint",
        "left_wrist_roll_joint",
        "left_wrist_pitch_joint",
        "left_wrist_yaw_joint",
        "right_shoulder_pitch_joint",
        "right_shoulder_roll_joint",
        "right_shoulder_yaw_joint",
        "right_elbow_joint",
        "right_wrist_roll_joint",
        "right_wrist_pitch_joint",
        "right_wrist_yaw_joint",
        "left_hip_pitch_joint",
        "left_hip_roll_joint",
        "left_hip_yaw_joint",
        "left_knee_joint",
        "left_ankle_pitch_joint",
        "left_ankle_roll_joint",
        "right_hip_pitch_joint",
        "right_hip_roll_joint",
        "right_hip_yaw_joint",
        "right_knee_joint",
        "right_ankle_pitch_joint",
        "right_ankle_roll_joint",
    ]


def _iter_gmr_pkls(source: Path) -> list[Path]:
    source = source.expanduser().resolve()
    if source.is_file() and source.suffix.lower() == ".zip":
        extract_dir = source.parent / f".{source.stem}_extracted"
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(source) as zf:
            zf.extractall(extract_dir)
        source = extract_dir
    if source.is_dir():
        # Prefer nested lafan1_gmr/ if present.
        nested = source / "lafan1_gmr"
        root = nested if nested.is_dir() else source
        files = sorted(root.glob("*.pkl"))
        if not files:
            files = sorted(root.rglob("*.pkl"))
        if not files:
            raise FileNotFoundError(f"No .pkl files under {source}")
        return files
    raise FileNotFoundError(f"Source must be a zip or directory: {source}")


def _gmr_to_robot_state(path: Path, *, robot_spec) -> RobotStateMotion:
    raw = joblib.load(path)
    required = ("root_pos", "root_rot", "dof_pos", "fps")
    missing = [k for k in required if k not in raw]
    if missing:
        raise ValueError(f"{path} missing fields {missing}")
    dof = np.asarray(raw["dof_pos"], dtype=np.float32)
    if dof.ndim != 2 or dof.shape[1] != 30:
        raise ValueError(f"{path} expected dof_pos [T,30], got {dof.shape}")
    joint_names_30 = _gmr_astro_30_joint_names()
    # Drop fixed head (always ~0 in this pack) for Astro 29-DoF training robot.
    keep = [i for i, name in enumerate(joint_names_30) if name != "head_joint"]
    dof29 = dof[:, keep]
    joint_names_29 = [joint_names_30[i] for i in keep]
    expected = set(robot_spec.control_joint_names)
    if set(joint_names_29) != expected:
        raise ValueError(
            f"{path} joint set mismatch after dropping head: "
            f"extra={set(joint_names_29) - expected} missing={expected - set(joint_names_29)}"
        )
    return RobotStateMotion(
        motion_key=path.stem,
        root_pos=np.asarray(raw["root_pos"], dtype=np.float32),
        root_quat=np.asarray(raw["root_rot"], dtype=np.float32),  # xyzw
        dof_pos=dof29,
        fps=float(np.asarray(raw["fps"]).reshape(-1)[0]),
        joint_names=joint_names_29,
        source="astro_gmr_lafan1",
        metadata={
            "path": str(path),
            "reader": "astro_gmr_lafan_pkl",
            "gmr_dof_dim": 30,
            "dropped_joints": ["head_joint"],
        },
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("/data/atom9/code/lafan1_gmr.zip"),
        help="Zip or directory of GMR per-motion PKLs",
    )
    parser.add_argument("--robot", default="configs/robots/astro_p2_29dof.yaml")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("ufo/data/robots/astro_p2/motions/lafan"),
        help="Directory for astro_lafan_29dof.pkl and clipped twin",
    )
    parser.add_argument("--clip-seconds", type=float, default=10.0)
    parser.add_argument("--stride-seconds", type=float, default=10.0)
    parser.add_argument("--min-clip-seconds", type=float, default=1.0)
    parser.add_argument(
        "--manifest-out",
        type=Path,
        default=Path("configs/data/astro_lafan.yaml"),
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    robot_spec = load_robot_spec(args.robot)
    files = _iter_gmr_pkls(args.source)
    print(f"found {len(files)} GMR motions from {args.source}")

    full: dict[str, Any] = {}
    for idx, path in enumerate(files, start=1):
        motion = _gmr_to_robot_state(path, robot_spec=robot_spec)
        ufo = robot_state_to_ufo_motion(motion, robot_spec, "astro_gmr_lafan1")
        key = ufo["motion_key"]
        if key in full:
            raise ValueError(f"Duplicate motion_key={key}")
        full[key] = ufo
        if idx % 10 == 0 or idx == len(files):
            print(f"converted {idx}/{len(files)}")

    out_dir = args.out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    full_path = out_dir / "astro_lafan_29dof.pkl"
    clip_path = out_dir / "astro_lafan_29dof_10s-clipped.pkl"
    for path in (full_path, clip_path):
        if path.exists() and not args.force:
            raise FileExistsError(f"{path} exists; pass --force to overwrite")

    dump_ufo_pkl(full, full_path, "astro_gmr_lafan1:full")
    clipped = clip_ufo_motion_dict(
        full,
        clip_seconds=args.clip_seconds,
        stride_seconds=args.stride_seconds,
        keep_short=True,
        min_clip_seconds=args.min_clip_seconds,
        source_name="astro_gmr_lafan1:clip",
    )
    dump_ufo_pkl(clipped, clip_path, "astro_gmr_lafan1:clip")

    def _rel(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(_REPO_ROOT))
        except ValueError:
            return str(path.resolve())

    manifest = {
        "robot_config": args.robot,
        "datasets": [
            {
                "name": "astro_lafan",
                "format": "ufo_pkl",
                "train_path": _rel(clip_path),
                "inference_path": _rel(full_path),
                "weight": 1.0,
            }
        ],
    }
    manifest_path = args.manifest_out.expanduser().resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    OmegaConf.save(OmegaConf.create(manifest), manifest_path)

    print(f"full motions: {len(full)} -> {full_path} ({full_path.stat().st_size / 1e6:.1f} MB)")
    print(f"clipped motions: {len(clipped)} -> {clip_path} ({clip_path.stat().st_size / 1e6:.1f} MB)")
    print(f"manifest: {manifest_path}")


if __name__ == "__main__":
    main()
