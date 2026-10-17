"""Dodge env — frozen UFO-FB + LoRA over a standing G1, privileged ball threat.

Adapted from ORCS ``orcs.tasks.dodge.env_cfg`` (BSD-3-Clause). Differences:

- robot PD / action / defaults aligned to UFO ``g1_29dof_hard_waist`` (not stock mjlab G1);
- observation streams are FB-oriented (``augmentation`` / ``critic`` = ball);
- Goal behaviour is carried by frozen UFO-FB + per-episode ``goal_z`` (not a
  stand-only station clip). Optional stand-surrogate rewards live in
  ``mdp/rewards.py`` but are **not** wired by default — they fight non-stand goals.
"""

from __future__ import annotations

from typing import Callable

from mjlab.entity import EntityCfg
from mjlab.envs import ManagerBasedRlEnvCfg
import mjlab.envs.mdp as mjlab_mdp
from mjlab.envs.mdp import actions as mdp_actions
from mjlab.envs.mdp import terminations as mdp_terminations
from mjlab.envs.mdp.rewards import action_rate_l2, joint_pos_limits
from mjlab.managers.event_manager import EventTermCfg
from mjlab.managers.observation_manager import ObservationGroupCfg, ObservationTermCfg
from mjlab.managers.reward_manager import RewardTermCfg
from mjlab.managers.termination_manager import TerminationTermCfg
from mjlab.scene import SceneCfg
from mjlab.sim import MujocoCfg, SimulationCfg
from mjlab.tasks.manipulation.mdp.terminations import illegal_contact
from mjlab.terrains import TerrainEntityCfg
from mjlab.viewer import ViewerConfig

from humanoidverse.adapt_fb.assets import BALL_BODY_NAME, ball_entity_cfg
from humanoidverse.adapt_fb.assets.ball import PARKED_BALL_POS
from humanoidverse.adapt_fb.assets.g1_ufo import (
    UFO_DEFAULT_JOINT_POS,
    get_ufo_aligned_g1_robot_cfg,
    ufo_action_scales,
)
from humanoidverse.adapt_fb.tasks.dodge import mdp
from humanoidverse.adapt_fb.tasks.dodge.observation_cfgs import ObsCtx, fb_dodge_obs
from humanoidverse.adapt_fb.tasks.dodge.sensors import (
    BALL_CONTACT_SENSOR_NAME,
    DODGE_KILL_BODIES,
    GROUND_CONTACT_SENSOR_NAME,
    ball_contact_sensor,
    ground_contact_sensor,
)

__all__ = ["dodge_env_cfg", "EPISODE_LENGTH_S", "UFO_G1_DEFAULT_JOINT_POS"]

EPISODE_LENGTH_S = 10.0
UFO_G1_DEFAULT_JOINT_POS = UFO_DEFAULT_JOINT_POS


def _g1_action_cfg() -> mdp_actions.JointPositionActionCfg:
    """UFO action_rescale scales on named joints (preserve_order)."""
    scales = ufo_action_scales()
    return mdp_actions.JointPositionActionCfg(
        entity_name="robot",
        actuator_names=tuple(scales.keys()),
        preserve_order=True,
        scale=scales,
        use_default_offset=True,
    )


def _policy_obs_group() -> ObservationGroupCfg:
    """Minimal proprio for the MJLab runner (UFO actor obs is built separately)."""
    return ObservationGroupCfg(
        terms={
            "joint_pos": ObservationTermCfg(func=mjlab_mdp.joint_pos_rel),
            "joint_vel": ObservationTermCfg(func=mjlab_mdp.joint_vel_rel),
            "projected_gravity": ObservationTermCfg(func=mjlab_mdp.projected_gravity),
        },
        concatenate_terms=True,
        enable_corruption=False,
    )


def dodge_env_cfg(
    *,
    play: bool = False,
    num_steps_per_env: int = 24,
    robot_cfg: Callable[[], EntityCfg] | None = None,
    ball_radius: float = 0.127,
    ball_mass: float = 0.62,
    kill_bodies: tuple[str, ...] = DODGE_KILL_BODIES,
    kill_exclude: tuple[str, ...] = (),
    throw_ball: bool = True,
    **throw_kw,
) -> ManagerBasedRlEnvCfg:
    """Standing G1 dodging a thrown ball; LoRA reads privileged ball ``augmentation``."""
    robot = (robot_cfg or get_ufo_aligned_g1_robot_cfg)()

    events: dict = {
        "reset_default": EventTermCfg(func=mjlab_mdp.reset_scene_to_default, mode="reset"),
        "policy_update_counter": EventTermCfg(
            func=mdp.PolicyUpdateCounter,
            mode="interval",
            interval_range_s=(0.0, 0.0),
            is_global_time=True,
            params={"num_steps_per_env": num_steps_per_env},
        ),
    }
    if throw_ball:
        events["throw_ball"] = EventTermCfg(
            func=mdp.ThrowBall,
            mode="interval",
            interval_range_s=(0.0, 0.0),
            params={"ball_name": BALL_BODY_NAME, **throw_kw},
        )

    # Keep the ball entity (obs/sensors stay consistent) but park it far away
    # when throws are disabled so gravity cannot drop it onto the robot.
    ball_cfg = ball_entity_cfg(
        radius=ball_radius,
        mass=ball_mass,
        spawn_pos=None if throw_ball else PARKED_BALL_POS,
    )

    cfg = ManagerBasedRlEnvCfg(
        scene=SceneCfg(
            terrain=TerrainEntityCfg(terrain_type="plane"),
            entities={
                "robot": robot,
                BALL_BODY_NAME: ball_cfg,
            },
            sensors=(
                ground_contact_sensor(kill_bodies, kill_exclude),
                ball_contact_sensor(),
            ),
            num_envs=1 if not play else 16,
            env_spacing=2.5,
        ),
        observations={
            "policy": _policy_obs_group(),
            **fb_dodge_obs(ObsCtx()),
        },
        actions={"joint_pos": _g1_action_cfg()},
        commands={},
        events=events,
        rewards={
            # Task: dodge. Between throws clearance saturates; recovery to the
            # episode's goal_z is the frozen UFO-FB's job (not a stand station).
            "ball_clearance": RewardTermCfg(
                func=mdp.ball_clearance,
                weight=1.0,
                params={"ball_name": BALL_BODY_NAME},
            ),
            "action_rate_l2": RewardTermCfg(func=action_rate_l2, weight=-0.1),
            "joint_pos_limits": RewardTermCfg(func=joint_pos_limits, weight=-1.0),
        },
        terminations={
            "time_out": TerminationTermCfg(func=mdp_terminations.time_out, time_out=True),
            "ball_hit": TerminationTermCfg(
                func=illegal_contact,
                params={"sensor_name": BALL_CONTACT_SENSOR_NAME},
            ),
            "fell": TerminationTermCfg(
                func=illegal_contact,
                params={"sensor_name": GROUND_CONTACT_SENSOR_NAME},
            ),
        },
        viewer=ViewerConfig(
            origin_type=ViewerConfig.OriginType.WORLD,
            distance=4.0,
            elevation=-15.0,
            azimuth=135.0,
        ),
        sim=SimulationCfg(
            nconmax=100,
            njmax=300,
            mujoco=MujocoCfg(timestep=0.005, iterations=10, ls_iterations=20),
        ),
        decimation=4,
        episode_length_s=EPISODE_LENGTH_S,
    )

    if play:
        cfg.scene.num_envs = 16
        if throw_ball and "throw_ball" in cfg.events:
            cfg.events["throw_ball"].params["stand_fraction"] = 0.0
    return cfg
