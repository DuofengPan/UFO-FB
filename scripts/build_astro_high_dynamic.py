#!/usr/bin/env python3
"""Rebuild the versioned Astro kungfu + four-backflip UFO datasets on CPU."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pickle
import sys
from pathlib import Path

import joblib
import numpy as np
from scipy.spatial.transform import Rotation, Slerp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ufo.motion.formats import RobotStateMotion, clip_ufo_motion_dict, dump_ufo_pkl, load_motion_data_by_format, robot_state_to_ufo_motion
from ufo.tools.robot_config import load_robot_spec


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resample(raw: dict, name: str, joint_names: list[str]) -> RobotStateMotion:
    fps = float(raw['fps'])
    root = np.asarray(raw['root_pos'], dtype=np.float64)
    quat = np.asarray(raw['root_rot'], dtype=np.float64)
    dof = np.asarray(raw['dof_pos'], dtype=np.float64)
    n = len(root)
    if n < 2 or root.shape != (n, 3) or quat.shape != (n, 4) or dof.shape != (n, 29):
        raise ValueError(f'{name}: invalid array shapes')
    if not np.isfinite(fps) or fps <= 0 or not all(np.isfinite(x).all() for x in (root, quat, dof)):
        raise ValueError(f'{name}: invalid fps or nonfinite data')
    if np.max(np.abs(np.linalg.norm(quat, axis=1) - 1)) > 1e-3:
        raise ValueError(f'{name}: non-unit quaternion')
    t = np.arange(n) / fps
    target = np.arange(int(np.floor(t[-1] * 50)) + 1) / 50
    interp = lambda a: np.column_stack([np.interp(target, t, a[:, i]) for i in range(a.shape[1])])
    return RobotStateMotion(
        motion_key=f'kungfu_{name}', root_pos=interp(root),
        root_quat=Slerp(t, Rotation.from_quat(quat))(target).as_quat(),
        dof_pos=interp(dof), fps=50.0, joint_names=joint_names, source='astro_high_dynamic',
        metadata={'category': 'kungfu', 'original_fps': fps, 'original_frames': n},
    )


def validate_roundtrip(motion: dict, spec) -> None:
    """Check that pose_aa actually reconstructs the declared root/joint rotations."""
    aa = np.asarray(motion['pose_aa'])
    body_idx = {name: i for i, name in enumerate(spec.body_names)}
    actual = Rotation.from_rotvec(aa[:, body_idx[spec.base_body]])
    expected = Rotation.from_quat(motion['root_quat'])
    if np.max((actual.inv() * expected).magnitude()) > 2e-5:
        raise ValueError(f"{motion['motion_key']}: root rotation roundtrip failed")
    for i, name in enumerate(spec.control_joint_names):
        expected_aa = motion['dof_pos'][:, i, None] * np.asarray(spec.joint_axes[name])[None, :]
        if not np.allclose(aa[:, body_idx[spec.joint_body_names[name]]], expected_aa, atol=2e-6):
            raise ValueError(f"{motion['motion_key']}: joint mapping failed: {name}")
    for field in ('pose_aa', 'root_trans_offset', 'root_quat', 'dof_pos'):
        if not np.isfinite(motion[field]).all():
            raise ValueError(f"{motion['motion_key']}: nonfinite {field}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true', help='Rebuild existing generated datasets')
    args = parser.parse_args()
    spec_path = ROOT / 'configs/robots/astro_p2_29dof.yaml'
    spec = load_robot_spec(spec_path)
    folder = ROOT / 'ufo/data/robots/astro_p2/motions/high_dynamic'
    outputs = [folder / 'astro_high_dynamic_50hz.pkl', folder / 'astro_high_dynamic_50hz_10s-clipped.pkl']
    if any(p.exists() for p in outputs) and not args.force:
        raise FileExistsError('Output exists; use --force to rebuild explicitly')
    layout = json.loads((folder / 'raw/provenance/joint_layout.json').read_text())
    if layout['joint_names'] != list(spec.control_joint_names) or layout['root_quat_order'] != 'xyzw':
        raise ValueError('Retarget XML joint order differs from the training robot')
    if sorted(spec.control_joint_names, key=lambda n: spec.joint_qpos_addr[n]) != list(spec.control_joint_names):
        raise ValueError('Training qpos/control joint order mismatch')
    full = {}
    sources = []
    kungfu = sorted((folder / 'raw/kungfu').glob('*.pkl'))
    flips = sorted((folder / 'raw/qingtong').glob('*.qpos.csv'))
    if len(kungfu) != 20 or len(flips) != 4:
        raise ValueError(f'Expected 20 kungfu and four flip sources, got {len(kungfu)}, {len(flips)}')
    for path in kungfu:
        provenance = json.loads((folder / f'raw/provenance/{path.name}.json').read_text())
        if provenance['output']['sha256'] != sha256(path):
            raise ValueError(f'Source checksum mismatch: {path.name}')
        if provenance['dependencies']['robot_model']['sha256'] != layout['source_xml_sha256']:
            raise ValueError(f'Retarget XML mismatch: {path.name}')
        with path.open('rb') as stream:
            raw = pickle.load(stream)
        state = resample(raw, path.stem, layout['joint_names'])
        state.metadata.update(source_file=str(path.relative_to(ROOT)), source_sha256=sha256(path))
        motion = robot_state_to_ufo_motion(state, spec, 'astro_high_dynamic')
        full[state.motion_key] = motion
        sources.append({'path': str(path.relative_to(ROOT)), 'sha256': sha256(path),
                        'motion_key': state.motion_key, 'category': 'kungfu',
                        'source_fps': float(raw['fps']), 'source_frames': len(raw['root_pos']),
                        'frames_50hz': len(state.root_pos)})
    columns = {'root_pos': [f'root_pos_{c}_m' for c in 'xyz'],
               'root_quat': [f'root_quat_{c}' for c in 'xyzw'],
               'dof_pos': [f'dof_pos_{i}_rad' for i in range(29)]}
    for path in flips:
        with path.open() as stream:
            rows = list(csv.DictReader(stream))
        if [int(r['Frame']) for r in rows] != list(range(len(rows))) or any(float(r['fps']) != 50 for r in rows):
            raise ValueError(f'Expected contiguous 50 Hz flip CSV: {path}')
        data = load_motion_data_by_format('robot_state_csv', str(path), source_name='qingtong_backflip',
                                         fps=50, robot_spec=spec, columns=columns)
        if len(data) != 1:
            raise ValueError('One flip motion per CSV required')
        motion = next(iter(data.values()))
        key = 'qingtong_' + path.name.removesuffix('.qpos.csv')
        motion.update(motion_key=key, source='astro_high_dynamic')
        motion['metadata'].update(category='backflip', source_file=str(path.relative_to(ROOT)),
                                  source_sha256=sha256(path))
        full[key] = motion
        sources.append({'path': str(path.relative_to(ROOT)), 'sha256': sha256(path),
                        'motion_key': key, 'category': 'backflip', 'source_fps': 50,
                        'source_frames': len(rows), 'frames_50hz': len(rows)})
    for motion in full.values():
        validate_roundtrip(motion, spec)
    clipped = clip_ufo_motion_dict(full, clip_seconds=10, stride_seconds=10,
                                   keep_short=True, min_clip_seconds=1, source_name='astro_high_dynamic')
    if {m['metadata']['source_motion_key'] for m in clipped.values()} != set(full):
        raise ValueError('Clipping dropped a source motion')
    for motion in clipped.values():
        validate_roundtrip(motion, spec)
    for data, path in zip((full, clipped), outputs):
        dump_ufo_pkl(data, path, 'astro_high_dynamic')
        reloaded = joblib.load(path)
        if set(reloaded) != set(data):
            raise ValueError('Serialized dataset keys changed')
    report = {'schema': 'astro_high_dynamic.v1', 'robot': spec.name, 'fps': 50,
              'root_quat_order': 'xyzw', 'joint_names': layout['joint_names'],
              'source_counts': {'kungfu': len(kungfu), 'backflip': len(flips)},
              'full_motions': len(full), 'training_clips': len(clipped),
              'full_duration_seconds': sum((len(m['pose_aa'])-1)/50 for m in full.values()),
              'training_frames': sum(len(m['pose_aa']) for m in clipped.values()),
              'sources': sources,
              'artifacts': [{'path': str(p.relative_to(ROOT)), 'sha256': sha256(p), 'bytes': p.stat().st_size} for p in outputs]}
    (folder / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sources','joint_names')}, indent=2))


if __name__ == '__main__':
    main()
