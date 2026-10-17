"""Reward terms — dodge task (+ optional stand-station helpers).

``ball_clearance`` is the SMP/MimicKit dodge signal and is what ``dodge_env_cfg``
wires. Episode goal behaviour is **not** spelled as a stand station: frozen
UFO-FB + per-episode ``goal_z`` is the prior; LoRA only adds the dodge residual.

``station_*`` helpers approximate ORCS's MultiClip nominal-stand pull. They are
**unused by default** — rewarding default stand fights dance/fight/jump goals.
"""

from __future__ import annotations

import torch
from mjlab.envs import ManagerBasedRlEnv

__all__ = [
    "ball_clearance",
    "station_height",
    "station_upright",
    "station_default_pose",
]


def ball_clearance(
    env: ManagerBasedRlEnv,
    robot_name: str = "robot",
    ball_name: str = "ball",
    pos_w: float = 0.9,
    vel_w: float = 0.1,
    pos_scale: float = 0.3,
    vel_scale: float = 1.0,
) -> torch.Tensor:
    """SMP/MimicKit's dodgeball reward (arXiv:2512.03028 ``compute_dodge_reward``).

        r = pos_w (1 - exp(-pos_scale d)) + vel_w exp(-vel_scale ||v_xy||^2)

    `d` is the root->ball distance. The distance term SATURATES, so once the ball
    is clear there is no gradient pulling the robot to keep fleeing — it settles;
    the stillness term makes it move only when it must.
    """
    robot, ball = env.scene[robot_name], env.scene[ball_name]
    d = torch.linalg.norm(
        ball.data.root_link_pos_w - robot.data.root_link_pos_w, dim=-1)
    v = torch.sum(torch.square(robot.data.root_link_lin_vel_w[:, :2]), dim=-1)
    return pos_w * (1.0 - torch.exp(-pos_scale * d)) + vel_w * torch.exp(-vel_scale * v)


def station_height(
    env: ManagerBasedRlEnv,
    robot_name: str = "robot",
    target_height: float = 0.78,
    std: float = 0.12,
) -> torch.Tensor:
    """Keep pelvis near the nominal standing height (ORCS station surrogate)."""
    h = env.scene[robot_name].data.root_link_pos_w[:, 2]
    return torch.exp(-torch.square(h - target_height) / (std * std))


def station_upright(
    env: ManagerBasedRlEnv,
    robot_name: str = "robot",
    std: float = 0.25,
) -> torch.Tensor:
    """Keep projected gravity ≈ (0, 0, -1) in the base frame."""
    grav_z = env.scene[robot_name].data.projected_gravity_b[:, 2]
    return torch.exp(-torch.square(grav_z + 1.0) / (std * std))


def station_default_pose(
    env: ManagerBasedRlEnv,
    robot_name: str = "robot",
    std: float = 0.8,
) -> torch.Tensor:
    """Soft pull of joints toward the entity default (action=0 target)."""
    robot = env.scene[robot_name]
    err = robot.data.joint_pos - robot.data.default_joint_pos
    return torch.exp(-torch.sum(torch.square(err), dim=-1) / (std * std))
