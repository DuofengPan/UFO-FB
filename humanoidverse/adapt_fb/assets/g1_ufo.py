"""G1 robot cfg aligned to UFO ``g1_29dof_hard_waist`` PD / action / defaults.

Stock ``mjlab`` Unitree G1 uses different Kp/Kd (especially waist ~40 vs UFO
300) and different effort grouping. The frozen UFO-FB actor was trained under
the UFO numbers; AdaptFb must replay that plant or the base cannot stand.
"""

from __future__ import annotations

from dataclasses import replace

from mjlab.asset_zoo.robots.unitree_g1.g1_constants import get_g1_robot_cfg
from mjlab.entity import EntityCfg

# UFO ``init_state.default_joint_angles`` (action=0 target).
UFO_DEFAULT_JOINT_POS: dict[str, float] = {
    "left_hip_pitch_joint": -0.1,
    "left_hip_roll_joint": 0.0,
    "left_hip_yaw_joint": 0.0,
    "left_knee_joint": 0.3,
    "left_ankle_pitch_joint": -0.2,
    "left_ankle_roll_joint": 0.0,
    "right_hip_pitch_joint": -0.1,
    "right_hip_roll_joint": 0.0,
    "right_hip_yaw_joint": 0.0,
    "right_knee_joint": 0.3,
    "right_ankle_pitch_joint": -0.2,
    "right_ankle_roll_joint": 0.0,
    "waist_yaw_joint": 0.0,
    "waist_roll_joint": 0.0,
    "waist_pitch_joint": 0.0,
    "left_shoulder_pitch_joint": 0.0,
    "left_shoulder_roll_joint": 0.0,
    "left_shoulder_yaw_joint": 0.0,
    "left_elbow_joint": 0.0,
    "left_wrist_roll_joint": 0.0,
    "left_wrist_pitch_joint": 0.0,
    "left_wrist_yaw_joint": 0.0,
    "right_shoulder_pitch_joint": 0.0,
    "right_shoulder_roll_joint": 0.0,
    "right_shoulder_yaw_joint": 0.0,
    "right_elbow_joint": 0.0,
    "right_wrist_roll_joint": 0.0,
    "right_wrist_pitch_joint": 0.0,
    "right_wrist_yaw_joint": 0.0,
}

# Substring tables — same matching rule as UFO ``_match_joint_value``.
UFO_STIFFNESS: dict[str, float] = {
    "hip_yaw": 40.17924,
    "hip_roll": 99.09843,
    "hip_pitch": 99.09843,
    "knee": 99.09843,
    "ankle_pitch": 28.50125,
    "ankle_roll": 28.50125,
    "waist_yaw": 300.0,
    "waist_roll": 300.0,
    "waist_pitch": 300.0,
    "shoulder_pitch": 14.25062,
    "shoulder_roll": 14.25062,
    "shoulder_yaw": 14.25062,
    "elbow": 14.25062,
    "wrist_roll": 14.25062,
    "wrist_pitch": 8.61103,
    "wrist_yaw": 8.61103,
}

UFO_DAMPING: dict[str, float] = {
    "hip_yaw": 2.55789,
    "hip_roll": 6.30880,
    "hip_pitch": 6.30880,
    "knee": 6.30880,
    "ankle_pitch": 1.81445,
    "ankle_roll": 1.81445,
    "waist_yaw": 5.0,
    "waist_roll": 5.0,
    "waist_pitch": 5.0,
    "shoulder_pitch": 0.90722,
    "shoulder_roll": 0.90722,
    "shoulder_yaw": 0.90722,
    "elbow": 0.90722,
    "wrist_roll": 0.90722,
    "wrist_pitch": 0.54820,
    "wrist_yaw": 0.54820,
}

# Ordered as UFO ``dof_names`` / ``dof_effort_limit_list``.
UFO_DOF_NAMES: tuple[str, ...] = tuple(UFO_DEFAULT_JOINT_POS.keys())
UFO_EFFORT_LIMITS: tuple[float, ...] = (
    139.0,
    139.0,
    88.0,
    139.0,
    50.0,
    50.0,
    139.0,
    139.0,
    88.0,
    139.0,
    50.0,
    50.0,
    88.0,
    50.0,
    50.0,
    25.0,
    25.0,
    25.0,
    25.0,
    25.0,
    13.4,
    13.4,
    25.0,
    25.0,
    25.0,
    25.0,
    25.0,
    13.4,
    13.4,
)

ACTION_SCALE_BASE = 0.25  # UFO ``robot.control.action_scale`` with action_rescale


def _match(joint_name: str, table: dict[str, float]) -> float:
    for key, value in table.items():
        if key in joint_name:
            return float(value)
    raise KeyError(f"No UFO control entry for joint {joint_name}")


def ufo_action_scales() -> dict[str, float]:
    """Per-joint JointPositionAction scale = 0.25 * effort / Kp (UFO formula)."""
    scales: dict[str, float] = {}
    for name, effort in zip(UFO_DOF_NAMES, UFO_EFFORT_LIMITS, strict=True):
        kp = _match(name, UFO_STIFFNESS)
        scales[name] = ACTION_SCALE_BASE * effort / kp
    return scales


def get_ufo_aligned_g1_robot_cfg() -> EntityCfg:
    """Stock mjlab G1 mesh/XML with UFO PD gains, efforts, and default pose."""
    robot = get_g1_robot_cfg()
    # Replace stock regex defaults (e.g. ``.*_hip_pitch_joint``) entirely —
    # leaving them would override named UFO angles at entity build time.
    robot.init_state.joint_pos = dict(UFO_DEFAULT_JOINT_POS)
    pos = list(robot.init_state.pos)
    pos[2] = 0.8
    robot.init_state.pos = tuple(pos)

    # One BuiltinPositionActuatorCfg per joint so waist can use Kp=300.
    actuators = []
    for name, effort in zip(UFO_DOF_NAMES, UFO_EFFORT_LIMITS, strict=True):
        kp = _match(name, UFO_STIFFNESS)
        kd = _match(name, UFO_DAMPING)
        # Reuse armature/friction from a stock actuator when possible.
        template = robot.articulation.actuators[0]
        actuators.append(
            replace(
                template,
                target_names_expr=(name,),
                stiffness=kp,
                damping=kd,
                effort_limit=effort,
            )
        )
    robot.articulation.actuators = tuple(actuators)
    return robot
