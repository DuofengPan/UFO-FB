"""BONES unit/rotation conventions and corrupt-input rejection."""

import csv
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from scipy.spatial.transform import Rotation

from ufo.tools.bones_motion_import import ROOT_COLUMNS, read_bones_csv
from ufo.tools.robot_config import load_robot_spec


@pytest.fixture
def spec():
    return load_robot_spec(Path(__file__).resolve().parents[1] / "configs/robots/g1_29dof.yaml")


def write_csv(path, spec, *, corrupt=None, reverse=True):
    header = ["Frame", *ROOT_COLUMNS, *(n + "_dof" for n in spec.control_joint_names)]
    row = np.array([42, 100, -200, 80, 30, 40, 50, *np.linspace(-30, 40, 29)])
    data = np.repeat(row[None], 3, axis=0)
    data[:, 0] = [42, 43, 44]
    if corrupt == "gap":
        data[-1, 0] = 45
    if corrupt == "nan":
        data[1, 7] = np.nan
    if corrupt == "fractional":
        data[:, 0] += 0.1
    if reverse:
        header = header[::-1]
        data = data[:, ::-1]
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    return path


@pytest.mark.parametrize("order", ["xyzw", "wxyz"])
def test_named_columns_units_and_extrinsic_rotation(tmp_path, spec, order):
    spec = replace(spec, root_quat_order=order)
    state = read_bones_csv(write_csv(tmp_path / "test.csv", spec), spec)
    np.testing.assert_allclose(state.root_pos[0], [1, -2, 0.8])
    np.testing.assert_allclose(state.dof_pos[0], np.deg2rad(np.linspace(-30, 40, 29)), atol=1e-7)
    q = state.root_quat[0] if order == "xyzw" else state.root_quat[0, [1, 2, 3, 0]]
    expected = Rotation.from_euler("xyz", [30, 40, 50], degrees=True)
    assert (expected.inv() * Rotation.from_quat(q)).magnitude() < 1e-6
    assert (Rotation.from_euler("XYZ", [30, 40, 50], degrees=True).inv() * Rotation.from_quat(q)).magnitude() > 0.1
    assert state.fps == 120 and state.metadata["source_frame_start"] == 42


@pytest.mark.parametrize("corrupt", ["gap", "nan", "fractional"])
def test_rejects_bad_frames_or_values(tmp_path, spec, corrupt):
    with pytest.raises(ValueError):
        read_bones_csv(write_csv(tmp_path / "bad.csv", spec, corrupt=corrupt), spec)


def test_rejects_unrecognized_joint_schema(tmp_path, spec):
    path = write_csv(tmp_path / "bad.csv", spec)
    path.write_text(path.read_text().replace("left_hip_pitch_joint_dof", "wrong_joint_dof"))
    with pytest.raises(ValueError, match="schema"):
        read_bones_csv(path, spec)
