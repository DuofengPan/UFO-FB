"""Build UFO actor observation dicts from mjlab G1 robot state.

Matches ``HumanoidVerseMjlabEnv.get_observation`` proprio layout
(``bfm_zero_obs.yaml``):

- ``state`` = cat(dof_pos_rel, dof_vel, projected_gravity, base_ang_vel)  # 64
- ``last_action``  # 29 (UFO-normalized action space, typically ×5)
- ``history_actor`` = 4-step history of sorted keys
  ``[actions, base_ang_vel, dof_pos, dof_vel, projected_gravity]``  # 372

Obs scales follow UFO training (``base_ang_vel`` ×0.25). Noise is off.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch

# Sorted key order must match UFO HistoryHandler (sorted(obs_auxiliary keys)).
HISTORY_KEYS: tuple[str, ...] = (
    "actions",
    "base_ang_vel",
    "dof_pos",
    "dof_vel",
    "projected_gravity",
)
HISTORY_LENGTH = 4
OBS_SCALES: dict[str, float] = {
    "actions": 1.0,
    "base_ang_vel": 0.25,
    "dof_pos": 1.0,
    "dof_vel": 1.0,
    "projected_gravity": 1.0,
    "history_actor": 1.0,
}
# UFO policy action → mjlab JointPositionAction input.
ACTION_NORMALIZE_FROM = 1.0
ACTION_NORMALIZE_TO = 5.0
PRIVILEGED_STATE_DIM = 463


@dataclass
class ProprioSnapshot:
    dof_pos: torch.Tensor  # (B, 29) relative to default
    dof_vel: torch.Tensor
    projected_gravity: torch.Tensor
    base_ang_vel: torch.Tensor
    actions: torch.Tensor  # last policy action (pre-normalize)


class ActorHistoryBuffer:
    """Ring buffer mirroring UFO ``HistoryHandler`` for actor proprio."""

    def __init__(
        self,
        num_envs: int,
        *,
        device: str | torch.device,
        history_length: int = HISTORY_LENGTH,
    ) -> None:
        self.num_envs = int(num_envs)
        self.device = torch.device(device)
        self.history_length = int(history_length)
        self._dims = {
            "actions": 29,
            "base_ang_vel": 3,
            "dof_pos": 29,
            "dof_vel": 29,
            "projected_gravity": 3,
        }
        self._buf: dict[str, torch.Tensor] = {
            k: torch.zeros(self.num_envs, self.history_length, d, device=self.device)
            for k, d in self._dims.items()
        }

    def reset(self, env_ids: torch.Tensor | None = None) -> None:
        if env_ids is None:
            for v in self._buf.values():
                v.zero_()
            return
        if env_ids.numel() == 0:
            return
        for v in self._buf.values():
            v[env_ids] = 0.0

    def query(self) -> torch.Tensor:
        """Flattened history in UFO sorted-key order. Shape (B, 372).

        Layout matches ``HVHistoryHandler``: index 0 is **newest**, then older
        frames. ``reshape(B, -1)`` → ``[t0_dims | t1_dims | …]`` with t0 newest.
        """
        parts = [self._buf[k].reshape(self.num_envs, -1) for k in HISTORY_KEYS]
        return torch.cat(parts, dim=-1)

    def add(self, snap: dict[str, torch.Tensor]) -> None:
        """Push newest at index 0; shift older right (UFO ``HistoryHandler.add``)."""
        for key in HISTORY_KEYS:
            x = snap[key]
            buf = self._buf[key]
            # Must clone before overlapping write (same as UFO env_utils handler).
            val = buf.clone()
            buf[:, 1:] = val[:, :-1]
            buf[:, 0] = x


def proprio_from_robot(
    robot,
    last_action: torch.Tensor,
    *,
    default_joint_pos: torch.Tensor | None = None,
) -> ProprioSnapshot:
    """Read mjlab entity ``robot`` into UFO-scaled proprio (no history)."""
    default = default_joint_pos if default_joint_pos is not None else robot.data.default_joint_pos
    dof_pos = robot.data.joint_pos - default
    dof_vel = robot.data.joint_vel
    grav = robot.data.projected_gravity_b
    ang = robot.data.root_link_ang_vel_b
    return ProprioSnapshot(
        dof_pos=dof_pos,
        dof_vel=dof_vel,
        projected_gravity=grav,
        base_ang_vel=ang,
        actions=last_action,
    )


def _scale(name: str, x: torch.Tensor) -> torch.Tensor:
    return x * float(OBS_SCALES.get(name, 1.0))


def build_actor_obs(
    snap: ProprioSnapshot,
    history: ActorHistoryBuffer,
    *,
    include_privileged_zeros: bool = True,
    advance_history: bool = True,
) -> dict[str, torch.Tensor]:
    """Assemble UFO actor obs dict.

    When ``advance_history`` is True (once per control step), push the current
    frame after querying — same order as UFO ``_raw_actor_obs``. Set False for
    goal-cycle / peek rebuilds that must not corrupt the ring buffer.
    """
    scaled = {
        "actions": _scale("actions", snap.actions),
        "base_ang_vel": _scale("base_ang_vel", snap.base_ang_vel),
        "dof_pos": _scale("dof_pos", snap.dof_pos),
        "dof_vel": _scale("dof_vel", snap.dof_vel),
        "projected_gravity": _scale("projected_gravity", snap.projected_gravity),
    }
    hist = _scale("history_actor", history.query())
    state = torch.cat(
        [
            scaled["dof_pos"],
            scaled["dof_vel"],
            scaled["projected_gravity"],
            scaled["base_ang_vel"],
        ],
        dim=-1,
    )
    obs: dict[str, torch.Tensor] = {
        "state": state,
        "last_action": scaled["actions"],
        "history_actor": hist,
    }
    if include_privileged_zeros:
        b = state.shape[0]
        obs["privileged_state"] = torch.zeros(
            b, PRIVILEGED_STATE_DIM, device=state.device, dtype=state.dtype
        )
    if advance_history:
        history.add(scaled)
    return obs


def policy_to_mjlab_action(action: torch.Tensor) -> torch.Tensor:
    """Map UFO tanh policy output into mjlab JointPositionAction units."""
    return action * (ACTION_NORMALIZE_TO / ACTION_NORMALIZE_FROM)
