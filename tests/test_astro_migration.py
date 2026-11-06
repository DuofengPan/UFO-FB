from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from ufo.agents.fb_cpr_aux.config import build_fb_agent
from ufo.envs.config import resolve_task_config
from ufo.motion.formats import read_robot_state_npz
from ufo.tools.robot_config import load_robot_training_spec
from ufo.train import build_mjlab_config, parse_args

ROBOT = Path("configs/robots/astro_p2_29dof.yaml")


def astro_config(**updates):
    return build_mjlab_config(**(dict(device="cpu", work_dir="/tmp/astro-config-only", num_envs=1024,
        num_env_steps=192000000, seed=0, use_wandb=False, wandb_run_name=None,
        robot_config=ROBOT, data_path="ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof_10s-clipped.pkl", buffer_size=2560000, num_agent_updates=16) | updates))


def test_astro_preserves_topology_and_actual_control_settings():
    cfg = astro_config()
    arch = cfg.agent.model.archi
    assert not arch.shared_critic and not cfg.agent.train.use_bf16_amp
    for key in ("f", "actor", "critic"):
        network = getattr(arch, key)
        assert (network.hidden_dim, network.hidden_layers) == (2048, 6)
    assert arch.f.num_parallel == arch.critic.num_parallel == 2
    assert (arch.b.hidden_dim, arch.b.hidden_layers, arch.z_dim) == (256, 1, 256)
    assert (arch.discriminator.hidden_dim, arch.discriminator.hidden_layers) == (1024, 3)
    assert arch.actor.input_filter.key == ["state", "last_action", "history_actor"]
    assert cfg.agent.train.batch_size == 1024
    assert cfg.agent.aux_rewards_scaling["penalty_ankle_roll"] == -4.0
    assert cfg.agent.train.lr_actor == cfg.agent.train.lr_f == 0.0003
    assert (cfg.buffer_size, cfg.num_agent_updates) == (2560000, 16)
    task = resolve_task_config(cfg.env, 1024)
    assert task.lie_down_init and task.lie_down_init_prob == 0.3
    assert task.obs.obs_scales.base_ang_vel == 0.25
    assert task.robot.actions_dim == 29
    assert task.robot.control.stiffness.hip_pitch == 111.584
    assert task.robot.control.damping.hip_pitch == 8.88
    assert task.robot.asset.xml_file.endswith("astro_p2_29dof_simplify_primitive_collision.xml")
    assert task.simulator.config.sim.fps / task.simulator.config.sim.control_decimation == 50


def test_astro_overrides_do_not_change_upstream_defaults():
    before = build_fb_agent(device="cpu").model_dump()
    astro_config()
    assert build_fb_agent(device="cpu").model_dump() == before
    assert before["model"]["archi"]["actor"]["hidden_dim"] == 1024
    assert before["model"]["archi"]["shared_critic"]


def test_online_replay_offload_preserves_gpu_experts_and_training_knobs():
    cfg = astro_config(device="cuda:3", replay_device="cpu")
    assert cfg.replay_device == "cpu" and cfg.buffer_device == "cuda"
    assert cfg.agent.model.device == "cuda"
    assert cfg.buffer_size == 2560000 and cfg.num_agent_updates == 16
    assert cfg.agent.train.batch_size == 1024 and not cfg.agent.train.use_bf16_amp
    assert astro_config().replay_device is None
    with patch("sys.argv", ["ufo.train", "--replay-device", "cpu", "--data-path", "/tmp/config-only.pkl"]):
        assert parse_args().replay_device == "cpu"


def test_native_residual_construction_matches_legacy_layer_depths():
    import gymnasium as gym

    from ufo.agents.common.networks import ResidualActor, ResidualForwardMap

    arch = astro_config().agent.model.archi
    space = gym.spaces.Dict({key: gym.spaces.Box(-np.inf, np.inf, shape=(3,), dtype=np.float32)
                            for key in ("state", "privileged_state", "last_action", "history_actor")})
    actor = arch.actor.model_copy(update={"hidden_dim": 16}).build(space, arch.z_dim, 29)
    forward = arch.f.model_copy(update={"hidden_dim": 16}).build(space, arch.z_dim, 29)
    assert isinstance(actor, ResidualActor) and isinstance(forward, ResidualForwardMap)
    assert len(actor.embed_z) == len(actor.embed_s) == 2
    assert len(forward.embed_z) == len(forward.embed_sa) == 6
    assert len(actor.policy) == len(forward.Fs) == 7  # Six residual blocks plus output.


def test_explicit_training_knobs_are_not_hidden_by_robot_baseline():
    cfg = astro_config(update_z_every_step=37, clip_grad_norm=0.5, lr_scale=0.5)
    assert cfg.agent.train.update_z_every_step == 37
    assert cfg.agent.train.clip_grad_norm == 0.5
    assert cfg.agent.train.lr_actor == 0.00015


def test_smoke_disables_both_cloud_loggers():
    with patch("sys.argv", ["ufo.train", "--robot-config", str(ROBOT), "--data-path", "/tmp/astro-config-test.pkl", "--smoke", "--use-swanlab", "--use-wandb"]):
        args = parse_args()
    assert not args.use_swanlab and not args.use_wandb


def test_body_link_npz_reorders_joints_and_root_quaternion(tmp_path):
    robot = load_robot_training_spec(ROBOT).robot
    names = list(reversed(robot.control_joint_names))
    dofs = np.tile(np.arange(29, dtype=np.float32) * 0.01, (3, 1))
    path = tmp_path / "body_link.npz"
    np.savez(path, dof_positions=dofs, dof_names=names, body_names=[robot.base_body],
             body_positions=np.zeros((3, 1, 3), np.float32),
             body_rotations=np.tile([1., 0., 0., 0.], (3, 1, 1)), fps=50)
    motion = read_robot_state_npz(path, source_name="astro-test", robot_spec=robot)["body_link"]
    np.testing.assert_allclose(motion.dof_pos[0], dofs[0, ::-1])
    np.testing.assert_allclose(motion.root_quat, np.tile([0, 0, 0, 1], (3, 1)))


def test_actual_motion_manifest_keeps_fixed_source_masses():
    from ufo.motion.manifest import prepare_motion_manifest

    data = Path("ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof_10s-clipped.pkl")
    if not data.exists():
        pytest.skip("Local motion binaries are intentionally not included in Git")
    manifest = prepare_motion_manifest("configs/data/astro_lafan_high_dynamic.yaml")
    assert manifest.train_data_weights == [0.9, 0.1]
    assert len(manifest.train_data_paths) == 2
