"""ORCS-style play/train host on UFO's MJLab env + optional dodge ball.

Default construction matches ``humanoidverse.goal_inference`` (frozen UFO
``HumanoidVerseMjlabVectorEnv``). Ball modes inject a freejoint sphere into that
same mjlab scene — UFO train / goal_inference defaults are untouched.

Train and play share this plant so LoRA sees the same proprio / action / reset
path as the frozen UFO-FB prior.
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

# Play: denser throws, no stand anchors (viewer should see the threat).
_THROW_PARAMS_PLAY: dict[str, Any] = {
    "stand_fraction": 0.0,
    "interval_range_s": (0.6, 1.2),
    "dist_range": (2.0, 3.0),
    "flight_time_range": (0.55, 0.70),
    "flight_window_s": 1.5,
}

# Train: ORCS-like cadence + stand anchors so the batch keeps ball-free goals.
_THROW_PARAMS_TRAIN: dict[str, Any] = {
    "stand_fraction": 0.2,
    "interval_range_s": (1.5, 3.5),
    "dist_range": (2.0, 3.0),
    "flight_time_range": (0.55, 0.70),
    "flight_window_s": 1.5,
}


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


def _inject_ball(mjlab_cfg: Any, ball: BallMode, *, train: bool = False) -> Any:
    """Add ball entity (+ ThrowBall event) onto a UFO ``ManagerBasedRlEnvCfg``."""
    if ball == "none":
        return mjlab_cfg

    from mjlab.managers.event_manager import EventTermCfg

    from humanoidverse.adapt_fb.assets.ball import BALL_BODY_NAME, PARKED_BALL_POS, ball_entity_cfg
    from humanoidverse.adapt_fb.tasks.dodge.mdp.events import ThrowBall

    entities = dict(mjlab_cfg.scene.entities)
    events = dict(mjlab_cfg.events)

    if ball == "parked":
        # Far lateral park only — no ThrowBall, so it never hops to overhead.
        entities[BALL_BODY_NAME] = ball_entity_cfg(spawn_pos=PARKED_BALL_POS)
    else:
        # Overhead park between throws; ThrowBall teleports into the frontal cone.
        entities[BALL_BODY_NAME] = ball_entity_cfg(spawn_pos=(0.0, 0.0, 5.0))
        throw_params = dict(_THROW_PARAMS_TRAIN if train else _THROW_PARAMS_PLAY)
        throw_params["ball_name"] = BALL_BODY_NAME
        events["throw_ball"] = EventTermCfg(
            func=ThrowBall,
            mode="interval",
            interval_range_s=(0.0, 0.0),  # tick every env step; ThrowBall has its own timer
            params=throw_params,
        )

    scene = replace(mjlab_cfg.scene, entities=entities)
    # Extra contacts for the freejoint sphere.
    sim = mjlab_cfg.sim
    sim = replace(sim, nconmax=max(int(sim.nconmax), 128), njmax=max(int(sim.njmax), 512))
    return replace(mjlab_cfg, scene=scene, events=events, sim=sim)


def _inject_dodge_contact_terms(mjlab_cfg: Any) -> Any:
    """Ball-hit / fell terminations + contact sensors (same as dodge env_cfg)."""
    from mjlab.managers.termination_manager import TerminationTermCfg
    from mjlab.tasks.manipulation.mdp.terminations import illegal_contact

    from humanoidverse.adapt_fb.tasks.dodge.sensors import (
        BALL_CONTACT_SENSOR_NAME,
        DODGE_KILL_BODIES,
        GROUND_CONTACT_SENSOR_NAME,
        ball_contact_sensor,
        ground_contact_sensor,
    )

    sensors = list(mjlab_cfg.scene.sensors) + [
        ground_contact_sensor(DODGE_KILL_BODIES),
        ball_contact_sensor(),
    ]
    terminations = dict(mjlab_cfg.terminations)
    terminations["ball_hit"] = TerminationTermCfg(
        func=illegal_contact,
        params={"sensor_name": BALL_CONTACT_SENSOR_NAME},
    )
    terminations["fell"] = TerminationTermCfg(
        func=illegal_contact,
        params={"sensor_name": GROUND_CONTACT_SENSOR_NAME},
    )
    scene = replace(mjlab_cfg.scene, sensors=tuple(sensors))
    return replace(mjlab_cfg, scene=scene, terminations=terminations)


def build_ufo_vector_env(
    model_folder: Path,
    *,
    device: str,
    num_envs: int = 1,
    data_path: Path | None = None,
    max_episode_length_s: float = 20.0,
    headless: bool = True,
    ball: BallMode = "none",
    train: bool = False,
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
    mjlab_cfg = _inject_ball(mjlab_cfg, ball, train=train)
    if ball != "none":
        mjlab_cfg = _inject_dodge_contact_terms(mjlab_cfg)
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
    wrapped._adapt_fb_train = train  # type: ignore[attr-defined]
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


def _critic_features(mjlab_env: Any, aug: torch.Tensor) -> torch.Tensor:
    """Privileged critic: ball aug + coarse proprio (matches dodge critic group)."""
    import mjlab.envs.mdp as mjlab_mdp

    return torch.cat(
        [
            aug,
            mjlab_mdp.joint_pos_rel(mjlab_env),
            mjlab_mdp.joint_vel_rel(mjlab_env),
            mjlab_mdp.projected_gravity(mjlab_env),
            mjlab_mdp.base_lin_vel(mjlab_env),
            mjlab_mdp.base_ang_vel(mjlab_env),
        ],
        dim=-1,
    )


def _dodge_reward(mjlab_env: Any, *, ball: BallMode) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    """Dodge task reward (UFO core reward is tracking — ignore for AdaptFb)."""
    from mjlab.envs.mdp.rewards import action_rate_l2, joint_pos_limits

    from humanoidverse.adapt_fb.assets.ball import BALL_BODY_NAME
    from humanoidverse.adapt_fb.tasks.dodge.mdp.rewards import ball_clearance

    n = int(mjlab_env.num_envs)
    device = mjlab_env.device
    if ball == "none":
        zero = torch.zeros(n, device=device, dtype=torch.float32)
        return zero, {"ball_clearance": zero, "action_rate_l2": zero, "joint_pos_limits": zero}

    clearance = ball_clearance(mjlab_env, ball_name=BALL_BODY_NAME)
    rate = action_rate_l2(mjlab_env)
    limits = joint_pos_limits(mjlab_env)
    rew = clearance - 0.1 * rate - 1.0 * limits
    return rew, {
        "ball_clearance": clearance,
        "action_rate_l2": rate,
        "joint_pos_limits": limits,
    }


class _UfoHostBase:
    """Shared GoalBank + ball-aug packing over a UFO VectorEnv."""

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
        self.cfg = self.unwrapped.cfg  # required by mjlab BaseViewer / rsl_rl
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

    def _refresh_aug(self) -> None:
        self._aug = _ball_augmentation(self.unwrapped, ball=self.ball, device=self.device)

    def _pack_obs(self, ufo_obs: dict[str, torch.Tensor], *, with_critic: bool = False) -> TensorDict:
        self._refresh_aug()
        payload: dict[str, torch.Tensor] = {}
        for key, value in ufo_obs.items():
            if torch.is_tensor(value):
                payload[key] = value
            else:
                payload[key] = torch.as_tensor(value, device=self.device, dtype=torch.float32)
        payload["goal_z"] = self._goal_z.clone()
        payload["augmentation"] = self._aug.clone()
        if with_critic:
            payload["critic"] = _critic_features(self.unwrapped, self._aug)
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

    def close(self) -> None:
        return self.vector.close()


class UfoHostPlayEnv(_UfoHostBase):
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
        super().__init__(
            vector_env,
            goal_bank,
            ball=ball,
            augmentation_dim=augmentation_dim,
            multi_z=multi_z,
            fixed_goal_name=fixed_goal_name,
        )
        self.reset()

    def reset(self) -> TensorDict:
        ufo_obs, _info = self.vector.reset(to_numpy=False)
        self._resample_goals()
        self._cached_obs = self._pack_obs(ufo_obs, with_critic=False)
        return self._cached_obs

    def step(self, actions: torch.Tensor) -> tuple[TensorDict, torch.Tensor, torch.Tensor, dict]:
        # Policy actions are UFO tanh-space; VectorEnv applies normalize_action (×5).
        ufo_obs, rew, terminated, truncated, info = self.vector.step(actions, to_numpy=False)
        dones_bool = terminated.bool() | truncated.bool()
        dones = dones_bool.to(dtype=torch.long)
        # HumanoidVerseMjlabCore already reset done envs inside step — only resample z.
        if bool(dones_bool.any()):
            self._resample_goals(dones_bool.nonzero(as_tuple=False).flatten())
        self._cached_obs = self._pack_obs(ufo_obs, with_critic=False)
        return self._cached_obs, rew, dones, dict(info) if info is not None else {}


class UfoHostTrainEnv(_UfoHostBase):
    """rsl_rl ``VecEnv`` on the same UFO host used by play.

    Obs groups match ``FbWithAdapterModel`` / ``adapt_fb_agent_cfg``:

        state, last_action, history_actor, goal_z, augmentation, critic

    Rewards are AdaptFb dodge terms (ball_clearance − action_rate − joint limits);
    UFO tracking reward from the core is discarded. Terminations (ball_hit / fell /
    time_out) come from the injected mjlab MDP; the UFO core auto-resets dones.

    Implements the ``rsl_rl.env.VecEnv`` surface (duck-typed; not a subclass, so
    ``ensure_vendored_rsl_rl`` can run before this module is imported).
    """

    def __init__(
        self,
        vector_env: Any,
        goal_bank: GoalBank,
        *,
        ball: BallMode = "throw",
        augmentation_dim: int = 6,
        multi_z: bool = True,
        fixed_goal_name: str | None = None,
    ) -> None:
        super().__init__(
            vector_env,
            goal_bank,
            ball=ball,
            augmentation_dim=augmentation_dim,
            multi_z=multi_z,
            fixed_goal_name=fixed_goal_name,
        )
        self.num_actions = int(self.unwrapped.action_manager.total_action_dim)
        self.max_episode_length = int(self.unwrapped.max_episode_length)

        ufo_obs, _info = self.vector.reset(to_numpy=False)
        self._resample_goals()
        self._cached_obs = self._pack_obs(ufo_obs, with_critic=True)

    @property
    def episode_length_buf(self) -> torch.Tensor:
        return self.core.episode_length_buf

    @episode_length_buf.setter
    def episode_length_buf(self, value: torch.Tensor) -> None:
        self.core.episode_length_buf = value
        self.unwrapped.episode_length_buf = value

    def reset(self) -> TensorDict:
        ufo_obs, _info = self.vector.reset(to_numpy=False)
        self._resample_goals()
        self._cached_obs = self._pack_obs(ufo_obs, with_critic=True)
        return self._cached_obs

    def step(self, actions: torch.Tensor) -> tuple[TensorDict, torch.Tensor, torch.Tensor, dict]:
        # Same action contract as play: tanh → UFO normalize_action (×5).
        ufo_obs, _ufo_rew, terminated, truncated, info = self.vector.step(actions, to_numpy=False)
        rew, aux = _dodge_reward(self.unwrapped, ball=self.ball)
        dones_bool = terminated.bool() | truncated.bool()
        dones = dones_bool.to(dtype=torch.long)

        if bool(dones_bool.any()):
            self._resample_goals(dones_bool.nonzero(as_tuple=False).flatten())

        self._cached_obs = self._pack_obs(ufo_obs, with_critic=True)
        extras: dict[str, Any] = dict(info) if info is not None else {}
        extras["time_outs"] = truncated.bool()
        extras["log"] = {f"rew/{k}": v.detach().mean() for k, v in aux.items()}
        return self._cached_obs, rew, dones, extras
