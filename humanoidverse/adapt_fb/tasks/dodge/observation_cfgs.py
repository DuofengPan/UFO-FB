"""Observation groups for AdaptFb dodge — ORCS-style augmentation seam.

Actor proprio for the frozen UFO-FB policy is assembled outside this env (UFO
obs contract). The env exposes:

- ``augmentation`` — privileged ball kinematics (LoRA condition; vision swap target)
- ``critic`` — ball + root (privileged value features; never deployed)
"""

from __future__ import annotations

from dataclasses import dataclass

from mjlab.managers.observation_manager import ObservationGroupCfg, ObservationTermCfg

from humanoidverse.adapt_fb.tasks.dodge import mdp


@dataclass(frozen=True)
class ObsCtx:
    robot_name: str = "robot"
    ball_name: str = "ball"


def _T(func, params: dict | None = None) -> ObservationTermCfg:
    return ObservationTermCfg(func=func, params=params or {})


def _grp(terms: dict) -> ObservationGroupCfg:
    return ObservationGroupCfg(terms=terms, concatenate_terms=True, enable_corruption=False)


def ball_state_terms(c: ObsCtx | None = None) -> dict[str, ObservationTermCfg]:
    c = c or ObsCtx()
    p = {"robot_name": c.robot_name, "ball_name": c.ball_name}
    return {
        "ball_pos_b": _T(mdp.ball_pos_b, p),
        "ball_vel_b": _T(mdp.ball_vel_b, p),
    }


def augmentation_group(c: ObsCtx | None = None) -> ObservationGroupCfg:
    """THE extension seam — privileged ball state for the LoRA adapter."""
    return _grp(ball_state_terms(c))


def critic_group(c: ObsCtx | None = None) -> ObservationGroupCfg:
    """Privileged critic: ball + coarse proprio (never deployed)."""
    c = c or ObsCtx()
    import mjlab.envs.mdp as mjlab_mdp

    terms = {
        **ball_state_terms(c),
        "joint_pos": _T(mjlab_mdp.joint_pos_rel),
        "joint_vel": _T(mjlab_mdp.joint_vel_rel),
        "projected_gravity": _T(mjlab_mdp.projected_gravity),
        "base_lin_vel": _T(mjlab_mdp.base_lin_vel),
        "base_ang_vel": _T(mjlab_mdp.base_ang_vel),
    }
    return _grp(terms)


def fb_dodge_obs(c: ObsCtx | None = None) -> dict[str, ObservationGroupCfg]:
    return {
        "augmentation": augmentation_group(c),
        "critic": critic_group(c),
    }
