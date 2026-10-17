"""Play / rollout host built on UFO's own MJLab env (not the Adapt dodge bridge).

Uses the same construction path as ``humanoidverse.goal_inference``:

  load_mjlab_env_cfg(model_folder) → HumanoidVerseMjlabConfig.build()
  → HumanoidVerseMjlabVectorEnv.reset / step / get_observation

Obs, history, ×5 action normalize, and PD targets all stay inside UFO — this
module only wraps that VectorEnv for mjlab's ``NativeMujocoViewer`` and attaches
an offline ``GoalBank`` ``z``.

Part of ``humanoidverse.adapt_fb`` inside the UFO repo. Motion/mjcf paths are
resolved from the UFO package root so cwd does not matter.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import torch
from tensordict import TensorDict

from humanoidverse.adapt_fb.core.goal_bank import GoalBank

# Default motion clip UFO goal_inference uses (resolved under the UFO package root).
_DEFAULT_MOTION_REL = Path("humanoidverse/data/lafan_29dof_10s-clipped.pkl")


def ufo_repo_root() -> Path:
    """Absolute root of the UFO checkout that provides ``humanoidverse``."""
    import humanoidverse

    return Path(humanoidverse.__file__).resolve().parent.parent


def resolve_ufo_motion_pkl(data_path: Path | None = None) -> Path:
    """Motion library path independent of process cwd."""
    if data_path is not None:
        path = Path(data_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"UFO motion pkl not found: {path}")
        return path
    root = ufo_repo_root()
    candidates = [
        root / _DEFAULT_MOTION_REL,
        root / "humanoidverse" / "data" / "lafan_29dof.pkl",
    ]
    for cand in candidates:
        if cand.is_file():
            return cand.resolve()
    raise FileNotFoundError(
        "UFO motion pkl not found under the humanoidverse install. "
        f"Tried: {', '.join(str(c) for c in candidates)}. Pass --data-path."
    )


def build_ufo_vector_env(
    model_folder: Path,
    *,
    device: str,
    num_envs: int = 1,
    data_path: Path | None = None,
    max_episode_length_s: float = 20.0,
    headless: bool = True,
) -> Any:
    """Build UFO ``HumanoidVerseMjlabVectorEnv`` (same as goal_inference).

    Always passes an **absolute** motion path so play works from any cwd.
    """
    from humanoidverse.mjlab_inference_utils import load_mjlab_env_cfg

    model_folder = Path(model_folder).expanduser().resolve()
    motion = resolve_ufo_motion_pkl(data_path)
    env_cfg, _root_h = load_mjlab_env_cfg(
        model_folder,
        data_path=motion,
        robot_config=None,
        device=device,
        headless=headless,
        disable_dr=True,
        disable_obs_noise=True,
        max_episode_length_s=max_episode_length_s,
    )
    # HumanoidVerseMjlabConfig is frozen — motion must be absolute via data_path above.
    # Training config already sets include_history_actor / include_last_action.
    wrapped, _meta = env_cfg.build(num_envs=num_envs)
    return wrapped


class UfoHostPlayEnv:
    """Viewer-compatible adapter: UFO VectorEnv + GoalBank ``z`` + zero ball aug.

    ``unwrapped`` is the underlying mjlab ``ManagerBasedRlEnv`` so
    ``NativeMujocoViewer`` can sync sim state. Policy obs come from UFO
    ``get_observation`` (not Adapt ``obs_bridge``).
    """

    def __init__(
        self,
        vector_env: Any,
        goal_bank: GoalBank,
        *,
        augmentation_dim: int = 6,
        multi_z: bool = False,
        fixed_goal_name: str | None = None,
    ) -> None:
        self.vector = vector_env
        self.core = vector_env._env
        self.unwrapped = self.core.mjlab_env
        self.goal_bank = goal_bank
        self.augmentation_dim = int(augmentation_dim)
        self.multi_z = bool(multi_z)
        self.fixed_goal_name = fixed_goal_name

        self.num_envs = int(self.unwrapped.num_envs)
        self.device = torch.device(self.core.device)
        self._goal_z = torch.zeros(self.num_envs, goal_bank.z_dim, device=self.device)
        self._goal_names: list[str] = [""] * self.num_envs
        self._aug = torch.zeros(self.num_envs, self.augmentation_dim, device=self.device)
        self._cached_obs: TensorDict | None = None
        self.reset()

    def _pack_obs(self, ufo_obs: dict[str, torch.Tensor]) -> TensorDict:
        payload: dict[str, torch.Tensor] = {}
        for key, value in ufo_obs.items():
            if torch.is_tensor(value):
                payload[key] = value
            else:
                payload[key] = torch.as_tensor(value, device=self.device, dtype=torch.float32)
        payload["goal_z"] = self._goal_z.clone()
        payload["augmentation"] = self._aug.clone()
        return TensorDict(payload, batch_size=[self.num_envs])

    def _resample_goals(self, env_ids: torch.Tensor | None = None) -> None:
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        n = int(env_ids.numel())
        if n == 0:
            return
        if self.multi_z and self.fixed_goal_name is None:
            names, z = self.goal_bank.sample(n)
        else:
            name = self.fixed_goal_name or self.goal_bank.names[0]
            names = [name] * n
            z = self.goal_bank.get(name).unsqueeze(0).expand(n, -1).contiguous()
        self._goal_z[env_ids] = z.to(self.device)
        for i, eid in enumerate(env_ids.tolist()):
            self._goal_names[int(eid)] = names[i]

    def set_goal_index(self, index: int, env_ids: torch.Tensor | None = None) -> str:
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)
        name, z = self.goal_bank.get_index(index)
        z = z.to(self.device).unsqueeze(0).expand(int(env_ids.numel()), -1).contiguous()
        self._goal_z[env_ids] = z
        for eid in env_ids.tolist():
            self._goal_names[int(eid)] = name
        if self._cached_obs is not None:
            self._cached_obs = self._cached_obs.clone()
            self._cached_obs["goal_z"] = self._goal_z.clone()
        return name

    def cycle_goals(self, *, step: int = 1) -> str:
        if not self._goal_names or not self._goal_names[0]:
            cur = 0
        else:
            try:
                cur = self.goal_bank.names.index(self._goal_names[0])
            except ValueError:
                cur = 0
        return self.set_goal_index(cur + int(step))

    def get_observations(self) -> TensorDict:
        assert self._cached_obs is not None
        return self._cached_obs

    def reset(self) -> TensorDict:
        ufo_obs, _info = self.vector.reset(to_numpy=False)
        self._resample_goals()
        self._cached_obs = self._pack_obs(ufo_obs)
        return self._cached_obs

    def step(self, actions: torch.Tensor) -> tuple[TensorDict, torch.Tensor, torch.Tensor, dict]:
        ufo_obs, rew, terminated, truncated, info = self.vector.step(actions, to_numpy=False)
        dones_bool = terminated.bool() | truncated.bool()
        dones = dones_bool.to(dtype=torch.long)
        # Inference sets auto_reset=False; keep play continuous.
        if bool(dones_bool.any()):
            ufo_obs, _info = self.vector.reset(to_numpy=False)
            self._resample_goals(dones_bool.nonzero(as_tuple=False).flatten())
        self._cached_obs = self._pack_obs(ufo_obs)
        return self._cached_obs, rew, dones, dict(info) if info is not None else {}

    def close(self) -> None:
        return self.vector.close()
