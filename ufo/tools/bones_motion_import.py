"""Import already-retargeted BONES-SEED G1 CSVs; no retargeting or time resampling.

BONES uses centimetres, degrees and extrinsic XYZ root Euler angles at 120 Hz.
See docs/BONES_SEED.md. This adapter feeds the existing RobotState converter.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import joblib
import mujoco
import numpy as np
import torch
from easydict import EasyDict
from scipy.spatial.transform import Rotation

from ufo.motion.formats import RobotStateMotion, clip_ufo_motion_dict, robot_state_to_ufo_motion, validate_ufo_motion_dict
from ufo.motion.kinematics import HumanoidKinematics
from ufo.tools.robot_config import load_robot_spec

ROOT_COLUMNS = ["root_translateX", "root_translateY", "root_translateZ", "root_rotateX", "root_rotateY", "root_rotateZ"]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_bones_csv(path, spec, *, motion_key=None, fps=120.0):
    """Read named columns, reject nonfinite/gapped data, return canonical RobotState.

    Frames can start at any integer but must be contiguous. Joint columns may be
    reordered. XYZ rotations are extrinsic (scipy lowercase 'xyz'), never intrinsic.
    """
    path = Path(path)
    if not np.isfinite(fps) or fps <= 0:
        raise ValueError("Source fps must be finite and positive")
    if spec.coordinate_system != "z_up" or spec.dof_unit != "rad":
        raise ValueError("BONES import requires a Z-up robot configured in radians")
    with path.open(newline="", encoding="utf-8-sig") as stream:
        header = next(csv.reader(stream))
    expected = ["Frame", *ROOT_COLUMNS, *(name + "_dof" for name in spec.control_joint_names)]
    if len(set(header)) != len(header) or set(header) != set(expected):
        raise ValueError(f"{path}: unexpected CSV schema; missing={set(expected) - set(header)}, extra={set(header) - set(expected)}")
    values = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.float64, ndmin=2)
    if values.shape[1] != len(header) or len(values) < 3 or not np.isfinite(values).all():
        raise ValueError(f"{path}: at least three finite, full-width frames required")
    frames = values[:, header.index("Frame")]
    if not np.all(frames == np.rint(frames)) or not np.all(np.diff(frames) == 1):
        raise ValueError(f"{path}: Frame must contain contiguous integer indices")
    root = values[:, [header.index(c) for c in ROOT_COLUMNS]]
    quat = Rotation.from_euler("xyz", root[:, 3:], degrees=True).as_quat()
    if spec.root_quat_order == "wxyz":
        quat = quat[:, [3, 0, 1, 2]]
    elif spec.root_quat_order != "xyzw":
        raise ValueError(f"Unsupported quaternion order: {spec.root_quat_order}")
    dofs = np.deg2rad(values[:, [header.index(name + "_dof") for name in spec.control_joint_names]])
    return RobotStateMotion(
        motion_key or path.stem,
        (root[:, :3] / 100).astype(np.float32),
        quat.astype(np.float32),
        dofs.astype(np.float32),
        float(fps),
        joint_names=list(spec.control_joint_names),
        source="BONES-SEED G1",
        metadata=dict(
            source_csv=str(path),
            source_csv_sha256=sha256(path),
            source_frame_start=int(frames[0]),
            source_frame_end=int(frames[-1]),
            source_fps=float(fps),
            source_position_unit="cm",
            source_angle_unit="deg",
            root_rotation="extrinsic XYZ",
            resampling="none",
            retargeting="none",
        ),
    )


def audit_fk(state, motion, spec, model, parser, *, samples=128):
    """Compare original CSV robot state in MuJoCo with UFO pose_aa FK."""
    if samples < 2:
        raise ValueError("At least two FK samples required")
    frame_ids = np.unique(np.linspace(0, len(state.root_pos) - 1, min(samples, len(state.root_pos)), dtype=int))
    data = mujoco.MjData(model)
    body_ids = [model.body(name).id for name in spec.body_names]
    root_addr = spec.joint_qpos_addr[spec.free_joint]
    joint_addrs = [spec.joint_qpos_addr[name] for name in spec.control_joint_names]
    positions, rotations = [], []
    for frame in frame_ids:
        data.qpos[root_addr : root_addr + 3] = state.root_pos[frame]
        q = state.root_quat[frame]
        data.qpos[root_addr + 3 : root_addr + 7] = q[[3, 0, 1, 2]] if spec.root_quat_order == "xyzw" else q
        data.qpos[joint_addrs] = state.dof_pos[frame]
        mujoco.mj_forward(model, data)
        positions.append(data.xpos[body_ids].copy())
        rotations.append(data.xquat[body_ids][:, [1, 2, 3, 0]].copy())
    with torch.no_grad():
        result = parser.fk_batch(
            torch.from_numpy(motion["pose_aa"][frame_ids][None]),
            torch.from_numpy(motion["root_trans_offset"][frame_ids][None]),
            dt=1 / state.fps,
        )
    pos_error = float(np.max(np.linalg.norm(result.global_translation[0].numpy() - positions, axis=-1)))
    actual = result.global_rotation[0].numpy().reshape(-1, 4)
    expected = np.asarray(rotations).reshape(-1, 4)
    rot_error = float(np.max((Rotation.from_quat(actual).inv() * Rotation.from_quat(expected)).magnitude()))
    if pos_error > 2e-5 or rot_error > 2e-5:
        raise ValueError(f"{state.motion_key}: FK mismatch {pos_error}m / {rot_error}rad")
    if not np.array_equal(state.dof_pos, motion["dof_pos"]):
        raise ValueError(f"{state.motion_key}: joint positions changed during conversion")
    limits = np.array([spec.joint_ranges[n] if spec.joint_ranges[n] is not None else [-np.inf, np.inf] for n in spec.control_joint_names])
    overshoot = np.maximum(np.maximum(limits[:, 0] - state.dof_pos, state.dof_pos - limits[:, 1]), 0)
    return dict(
        sampled_frames=len(frame_ids),
        body_position_max_m=pos_error,
        body_rotation_max_rad=rot_error,
        joint_limit_max_overshoot_rad=float(overshoot.max()),
        joint_limit_frame_fraction=float((overshoot > 0.08).any(axis=1).mean()),
    )


def convert(manifest_path, root, robot_config, output, report_path, *, fps=120.0, train_output=None, clip_seconds=10.0, fk_samples=128):
    paths = [Path(p).resolve() for p in [output, report_path, *([train_output] if train_output else [])]]
    if len(set(paths)) != len(paths) or any(p.exists() for p in paths):
        raise ValueError("Outputs must be distinct new paths; refusing to overwrite existing files")
    root = Path(root).resolve()
    manifest_path = Path(manifest_path).resolve()
    records = json.loads(manifest_path.read_text())
    if not isinstance(records, list) or not records:
        raise ValueError("Selection manifest must be a nonempty list of records")
    spec = load_robot_spec(robot_config)
    if spec.name != "g1_29dof" or len(spec.control_joint_names) != 29 or spec.free_joint is None:
        raise ValueError("This CLI imports already-retargeted 29-DoF G1 data only")
    model = mujoco.MjModel.from_xml_path(spec.xml_path)
    parser = HumanoidKinematics(
        EasyDict(asset=EasyDict(assetRoot=str(spec.xml_file.parent), assetFileName=spec.xml_file.name), extend_config=[])
    )
    if parser.body_names != spec.body_names:
        raise ValueError("UFO FK body order differs from RobotSpec")
    motions, audits, hashes = {}, [], set()
    torch.set_num_threads(1)
    for record in records:
        source = (root / record["selected_path"]).resolve()
        if not source.is_relative_to(root):
            raise ValueError(f"Source escapes dataset root: {source}")
        digest = sha256(source)
        if digest != record["source_sha256"]:
            raise ValueError(f"{source}: manifest SHA-256 mismatch")
        if digest in hashes or record["id"] in motions:
            raise ValueError(f"Duplicate motion ID or source contents: {record['id']}")
        state = read_bones_csv(source, spec, motion_key=record["id"], fps=fps)
        if "frames" in record and len(state.root_pos) != record["frames"]:
            raise ValueError(f"{source}: frame count disagrees with selection manifest")
        motion = robot_state_to_ufo_motion(state, spec)
        motion["metadata"].update(selection=record, source_manifest_sha256=sha256(manifest_path))
        audit = audit_fk(state, motion, spec, model, parser, samples=fk_samples)
        audit.update(id=state.motion_key, frames=len(state.root_pos), fps=fps, source_sha256=digest)
        motions[state.motion_key] = motion
        hashes.add(digest)
        audits.append(audit)
        print(json.dumps(audit), flush=True)
    validate_ufo_motion_dict(motions, str(manifest_path))
    clips = (
        clip_ufo_motion_dict(motions, clip_seconds=clip_seconds, stride_seconds=clip_seconds, min_clip_seconds=1.0)
        if train_output
        else None
    )
    report = dict(
        status="conversion_and_fk_verified",
        physical_tracking_status="NOT_RUN",
        motion_count=len(motions),
        total_frames=sum(a["frames"] for a in audits),
        source_fps=fps,
        output_fps=fps,
        total_duration_s=sum((a["frames"] - 1) / fps for a in audits),
        training_clip_count=len(clips) if clips else None,
        source_manifest_sha256=sha256(manifest_path),
        robot_config=str(Path(robot_config).resolve()),
        robot_xml_sha256=sha256(spec.xml_file),
        resampling="none",
        retargeting="none",
        outputs={"full": str(Path(output).resolve()), "train": str(Path(train_output).resolve()) if train_output else None},
        motions=audits,
    )
    # Do not publish partial PKL files if serialization is interrupted.
    for path, payload in [(Path(output), motions), *([(Path(train_output), clips)] if train_output else [])]:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        joblib.dump(payload, temporary)
        temporary.replace(path)
        report.setdefault("output_sha256", {})[str(path.resolve())] = sha256(path)
    Path(report_path).parent.mkdir(parents=True, exist_ok=True)
    Path(report_path).write_text(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path, required=True, help="Selected JSON records: id, selected_path, source_sha256, optional frames"
    )
    parser.add_argument("--root", type=Path, required=True, help="Dataset root resolving selected_path")
    parser.add_argument("--robot-config", type=Path, default=Path("configs/robots/g1_29dof.yaml"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--train-output", type=Path)
    parser.add_argument("--source-fps", type=float, default=120.0, help="Explicit source rate, preserved without resampling")
    parser.add_argument("--clip-seconds", type=float, default=10.0)
    parser.add_argument("--fk-samples", type=int, default=128)
    args = parser.parse_args()
    result = convert(
        args.manifest,
        args.root,
        args.robot_config,
        args.output,
        args.report,
        fps=args.source_fps,
        train_output=args.train_output,
        clip_seconds=args.clip_seconds,
        fk_samples=args.fk_samples,
    )
    print(json.dumps({k: v for k, v in result.items() if k != "motions"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
