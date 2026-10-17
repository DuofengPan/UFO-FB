"""ORCS-style play host on UFO's MJLab env + optional dodge ball.

Default construction matches ``humanoidverse.goal_inference`` (frozen UFO
``HumanoidVerseMjlabVectorEnv``). Ball modes inject a freejoint sphere into that
same mjlab scene — UFO train / goal_inference defaults are untouched.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Literal

import torch
from tensordict import TensorDict

from humanoidverse.adapt_fb.core.goal_bank import GoalBank

BallMode = Literal["none", "parked", "throw"]

_DEFAULT_MOTION_REL = Path("humanoidverse/data/lafan_29dof_10s-clipped.pkl")


def ufo_repo_root() -> Path:
    import humanoidverse

    return Path(humanoidverse.__file__).resolve().parent.parent


def resolve_ufo_motion_pkl(data_path: Path | None = None) -> Path:
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
        "UFO motion pkl not found. "
        f"Tried: {', '.join(str(c) for c in candidates)}. Pass --data-path."
    )


def _inject_ball(mjlab_cfg: Any, ball: BallMode) -> Any:
    """Add ball entity (+ ThrowBall event) onto a UFO ``ManagerBasedRlEnvCfg``."""
    if ball == "none":
        return mjlab_cfg

    from mjlab.managers.event_manager import EventTermCfg

    from humanoidverse.adapt_fb.assets.ball import BALL_BODY_NAME, PARKED_BALL_POS, ball_entity_cfg
    from humanoidverse.adapt_fb.tasks.dodge.mdp.events import ThrowBall

    if ball == "parked":
        ball_cfg = ball_entity_cfg(spawn_pos=PARKED_BALL_POS)
        stand_fraction = 1.0  # all envs anchors → pin forever, never throw
    else:
        # Overhead park between throws; ThrowBall teleports into the frontal cone.
        ball_cfg = ball_entity_cfg(spawn_pos=(0.0, 0.0, 5.0))
        stand_fraction = 0.0

    entities = dict(mjlab_cfg.scene.entities)
    entities[BALL_BODY_NAME] = ball_cfg
    scene = replace(mjlab_cfg.scene, entities=entities)

    events = dict(mjlab_cfg.events)
    events["throw_ball"] = EventTermCfg(
        func=ThrowBall,
        mode="interval",
        interval_range_s=(0.0, 0.0),
        params={
            "ball_name": BALL_BODY_NAME,
            "stand_fraction": stand_fraction,
            # Cone threat (no camera on UFO host scene).
            "interval_range_s": (1.5, 3.5) if ball == "throw" else (1.0, 4.0),
            "dist_range": (2.0, 3.0),
            "flight_time_range": (0.55, 0.70),
        },
    )
    # Extra contacts for the freejoint sphere.
    sim = mjlab_cfg.sim
    sim = replace(sim, nconmax=max(int(sim.nconmax), 128), njmax=max(int(sim.njmax), 512))
    return replace(mjlab_cfg, scene=scene, events=events, sim=sim)


def build_ufo_vector_env(
    model_folder: Path,
    *,
    device: str,
    num_envs: int = 1,
    data_path: Path | None = None,
    max_episode_length_s: float = 20.0,
    headless: bool = True,
    ball: BallMode = "none",
) -> Any:
    """Build UFO VectorEnv; optionally inject AdaptFb ball into the mjlab scene."""
    from mjlab.envs import ManagerBasedRlEnv

    from humanoidverse.agents.envs.humanoidverse_mjlab import (
        HumanoidVerseMjlabCore,
        HumanoidVerseMjlabVectorEnv,
        make_mjlab_ufo_env_cfg,
        _compose_humanoidverse_config,
    )
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

    hv_config, unresolved_conf = _compose_humanoidverse_config(
        num_envs=num_envs,
        relative_config_path=env_cfg.relative_config_path,
        hydra_overrides=list(env_cfg.hydra_overrides),
        lafan_tail_path=env_cfg.lafan_tail_path,
        data_mix_weights=env_cfg.data_mix_weights,
        disable_obs_noise=env_cfg.disable_obs_noise,
        disable_domain_randomization=env_cfg.disable_domain_randomization,
        max_episode_length_s=env_cfg.max_episode_length_s,
        root_height_obs=env_cfg.root_height_obs,
        robot_training=env_cfg.robot_training,
    )
    mjlab_cfg = make_mjlab_ufo_env_cfg(
        hv_config,
        num_envs=num_envs,
        seed=env_cfg.seed,
        mjcf_path=env_cfg.mjcf_path,
        auto_reset=env_cfg.auto_reset,
        robot_training=env_cfg.robot_training,
    )
    mjlab_cfg = _inject_ball(mjlab_cfg, ball)
    mjlab_env = ManagerBasedRlEnv(mjlab_cfg, device=device)
    core = HumanoidVerseMjlabCore(hv_config, mjlab_env, creation_config=env_cfg)
    wrapped = HumanoidVerseMjlabVectorEnv(
        core,
        include_last_action=env_cfg.include_last_action,
        context_length=env_cfg.context_length,
        include_history_actor=env_cfg.include_history_actor,
        include_history_noaction=env_cfg.include_history_noaction,
    )
    wrapped._creation_config = env_cfg
    wrapped._adapt_fb_ball = ball  # type: ignore[attr-defined]
    wrapped._adapt_fb_unresolved = unresolved_conf  # type: ignore[attr-defined]
    return wrapped


def _ball_augmentation(mjlab_env: Any, *, ball: BallMode, device: torch.device) -> torch.Tensor:
    """Privileged (pos_b, vel_b) in robot yaw frame; zeros if no ball."""
    n = int(mjlab_env.num_envs)
    if ball == "none":
        return torch.zeros(n, 6, device=device, dtype=torch.float32)
    from humanoidverse.adapt_fb.assets.ball import BALL_BODY_NAME
    from humanoidverse.adapt_fb.tasks.dodge.mdp.observations import ball_pos_b, ball_vel_b

    pos = ball_pos_b(mjlab_env, ball_name=BALL_BODY_NAME)
    vel = ball_vel_b(mjlab_env, ball_name=BALL_BODY_NAME)
    return torch.cat([pos, vel], dim=-1)


class UfoHostPlayEnv:
    """Viewer-compatible adapter: UFO VectorEnv + GoalBank ``z`` + ball aug.

    Exposes ``cfg`` / ``num_envs`` / ``unwrapped`` for ``NativeMujocoViewer``.
    """

    def __init__(
        self,
        vector_env: Any,
        goal_bank: GoalBank,
        *,
        ball: BallMode = "none",
        augmentation_dim: int = 6,
        multi_z: bool = False,
        fixed_goal_name: str | None = None,
    ) -> None:
        self.vector = vector_env
        self.core = vector_env._env
        self.unwrapped = self.core.mjlab_env
        self.cfg = self.unwrapped.cfg  # required by mjlab BaseViewer
        self.goal_bank = goal_bank
        self.ball: BallMode = ball
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

    def _refresh_aug(self) -> None:
        self._aug = _ball_augmentation(self.unwrapped, ball=self.ball, device=self.device)

    def _pack_obs(self, ufo_obs: dict[str, torch.Tensor]) -> TensorDict:
        self._refresh_aug()
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
        if bool(dones_bool.any()):
            ufo_obs, _info = self.vector.reset(to_numpy=False)
            self._resample_goals(dones_bool.nonzero(as_tuple=False).flatten())
        self._cached_obs = self._pack_obs(ufo_obs)
        return self._cached_obs, rew, dones, dict(info) if info is not None else {}

    def close(self) -> None:
        return self.vector.close()
