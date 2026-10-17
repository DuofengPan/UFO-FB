"""VecEnv wrapper: mjlab dodge + UFO actor obs + offline goal ``z``."""

from __future__ import annotations

from typing import Any

import torch
from tensordict import TensorDict

from rsl_rl.env import VecEnv

from humanoidverse.adapt_fb.core.goal_bank import GoalBank
from humanoidverse.adapt_fb.core.obs_bridge import (
    ActorHistoryBuffer,
    build_actor_obs,
    policy_to_mjlab_action,
    proprio_from_robot,
)


class DodgeFbVecEnv(VecEnv):
    """Wraps a mjlab ``ManagerBasedRlEnv`` for AdaptFb PPO.

    Exposes TensorDict groups consumed by :class:`FbWithAdapterModel`::

        state, last_action, history_actor, goal_z, augmentation, critic

    Policy actions are UFO-space (≈tanh); they are ×5-normalized before the
    underlying JointPositionAction term (same as UFO ``normalize_action``).
    """

    def __init__(
        self,
        env: Any,
        goal_bank: GoalBank,
        *,
        clip_actions: float | None = 5.0,
        multi_z: bool = True,
        fixed_goal_name: str | None = None,
    ) -> None:
        self.env = env
        self.unwrapped = getattr(env, "unwrapped", env)
        self.goal_bank = goal_bank
        self.clip_actions = clip_actions
        self.multi_z = bool(multi_z)
        self.fixed_goal_name = fixed_goal_name

        self.num_envs = int(self.unwrapped.num_envs)
        self.device = torch.device(self.unwrapped.device)
        self.max_episode_length = self.unwrapped.max_episode_length
        self.num_actions = int(self.unwrapped.action_manager.total_action_dim)
        self.cfg = self.unwrapped.cfg

        self._history = ActorHistoryBuffer(self.num_envs, device=self.device)
        self._last_action = torch.zeros(self.num_envs, self.num_actions, device=self.device)
        self._goal_z = torch.zeros(self.num_envs, goal_bank.z_dim, device=self.device)
        self._goal_names: list[str] = [""] * self.num_envs

        # rsl_rl does not call reset — seed obs now.
        self.env.reset()
        self._resample_goals(torch.arange(self.num_envs, device=self.device))
        self._history.reset()
        self._last_action.zero_()
        self._cached_obs = self._build_obs()

    @property
    def episode_length_buf(self) -> torch.Tensor:
        return self.unwrapped.episode_length_buf

    @episode_length_buf.setter
    def episode_length_buf(self, value: torch.Tensor) -> None:
        self.unwrapped.episode_length_buf = value

    def get_observations(self) -> TensorDict:
        return self._cached_obs

    def _resample_goals(self, env_ids: torch.Tensor) -> None:
        if env_ids.numel() == 0:
            return
        n = int(env_ids.numel())
        if self.multi_z and self.fixed_goal_name is None:
            names, z = self.goal_bank.sample(n)
        else:
            name = self.fixed_goal_name or self.goal_bank.names[0]
            names = [name] * n
            z = self.goal_bank.get(name).unsqueeze(0).expand(n, -1).contiguous()
        z = z.to(self.device)
        self._goal_z[env_ids] = z
        for i, eid in enumerate(env_ids.tolist()):
            self._goal_names[eid] = names[i]

    def set_goal_index(self, index: int, env_ids: torch.Tensor | None = None) -> str:
        """Assign goal ``index`` (mod bank size) to selected envs; return goal name."""
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        name, z = self.goal_bank.get_index(index)
        z = z.to(self.device).unsqueeze(0).expand(int(env_ids.numel()), -1).contiguous()
        self._goal_z[env_ids] = z
        for eid in env_ids.tolist():
            self._goal_names[int(eid)] = name
        # Peek only — do not advance history when cycling goals mid-episode.
        self._cached_obs = self._build_obs(advance_history=False)
        return name

    def cycle_goals(self, *, step: int = 1) -> str:
        """Advance all envs to the next (or prev) goal in the bank; return new name."""
        if not self._goal_names or not self._goal_names[0]:
            cur = 0
        else:
            try:
                cur = self.goal_bank.names.index(self._goal_names[0])
            except ValueError:
                cur = 0
        return self.set_goal_index(cur + int(step))

    def reset(self) -> "TensorDict":
        """Reset underlying mjlab env and UFO-side buffers (viewer EnvProtocol)."""
        self.env.reset()
        self._history.reset()
        self._last_action.zero_()
        self._resample_goals(torch.arange(self.num_envs, device=self.device))
        self._cached_obs = self._build_obs(advance_history=True)
        return self._cached_obs

    def _build_obs(self, *, advance_history: bool = True) -> TensorDict:
        robot = self.unwrapped.scene["robot"]
        snap = proprio_from_robot(robot, self._last_action)
        actor = build_actor_obs(
            snap,
            self._history,
            include_privileged_zeros=False,
            advance_history=advance_history,
        )

        raw = self.unwrapped.observation_manager.compute()
        aug = raw["augmentation"]
        critic = raw["critic"]
        if not torch.is_tensor(aug):
            aug = torch.as_tensor(aug, device=self.device, dtype=torch.float32)
        if not torch.is_tensor(critic):
            critic = torch.as_tensor(critic, device=self.device, dtype=torch.float32)

        return TensorDict(
            {
                "state": actor["state"],
                "last_action": actor["last_action"],
                "history_actor": actor["history_actor"],
                "goal_z": self._goal_z.clone(),
                "augmentation": aug,
                "critic": critic,
            },
            batch_size=[self.num_envs],
        )

    def step(self, actions: torch.Tensor) -> tuple[TensorDict, torch.Tensor, torch.Tensor, dict]:
        # UFO stores *normalized* actions (×5) in obs last_action / history.
        mj_actions = policy_to_mjlab_action(actions)
        if self.clip_actions is not None:
            mj_actions = torch.clamp(mj_actions, -self.clip_actions, self.clip_actions)
        self._last_action = mj_actions.detach()
        obs_dict, rew, terminated, truncated, extras = self.env.step(mj_actions)
        del obs_dict  # rebuilt below with UFO proprio
        dones_bool = terminated | truncated
        dones = dones_bool.to(dtype=torch.long)

        done_ids = dones_bool.nonzero(as_tuple=False).flatten()
        if done_ids.numel() > 0:
            self._history.reset(done_ids)
            self._last_action[done_ids] = 0.0
            self._resample_goals(done_ids)

        self._cached_obs = self._build_obs(advance_history=True)
        if not self.cfg.is_finite_horizon:
            extras = dict(extras)
            extras["time_outs"] = truncated
        return self._cached_obs, rew, dones, extras

    def close(self) -> None:
        return self.env.close()
