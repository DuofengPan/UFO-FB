"""Goal 批处理、参考坐标、约束和 sticky 失败的确定性单元检查。"""
from types import SimpleNamespace
import json

import numpy as np
import pytest
import torch

from ufo.experiments.payload import rollout
from ufo.math import quat_rotate_inverse


NAMES = [
    'left_hip_pitch_joint', 'left_hip_roll_joint', 'left_hip_yaw_joint', 'left_knee_joint',
    'left_ankle_pitch_joint', 'left_ankle_roll_joint', 'right_hip_pitch_joint',
    'right_hip_roll_joint', 'right_hip_yaw_joint', 'right_knee_joint',
    'right_ankle_pitch_joint', 'right_ankle_roll_joint', 'waist_yaw_joint',
    'waist_pitch_joint', 'waist_roll_joint', 'left_shoulder_pitch_joint',
    'left_shoulder_roll_joint', 'left_shoulder_yaw_joint', 'left_elbow_joint',
    'left_wrist_roll_joint', 'left_wrist_pitch_joint', 'left_wrist_yaw_joint',
    'right_shoulder_pitch_joint', 'right_shoulder_roll_joint', 'right_shoulder_yaw_joint',
    'right_elbow_joint', 'right_wrist_roll_joint', 'right_wrist_pitch_joint',
    'right_wrist_yaw_joint',
]


def task(value=.1, height=.645, knee=1.2, quaternion=(1., 0., 0., 0.), **extra):
    q = np.zeros(29, dtype=np.float32)
    q[0] = value
    q[[3, 9]] = knee
    return {'qpos': [0., 0., height, *quaternion, *q.tolist()],
            'dof_pos': q.tolist(), 'support': 'both', **extra}


class Core:
    """只提供评估器的数据合同；不代替真实 MuJoCo 闭环验证。"""
    def __init__(self, count):
        self.device, self.dt, self.num_envs, self.num_dof = 'cpu', .1, count, 29
        self.body_names = ['pelvis', 'waist_roll_link', 'left_ankle_roll_link',
                           'right_ankle_roll_link', 'left_wrist_yaw_link',
                           'right_wrist_yaw_link', 'head_link']
        self.dof_names, self.num_bodies = NAMES, 7
        self.env_origins = torch.zeros((count, 3))
        self.env_origins[:, 0] = torch.arange(count) * 3
        self.default_dof_pos = torch.zeros((count, 29))
        self.dof_vel = torch.zeros((count, 29))
        self.config = SimpleNamespace(obs=SimpleNamespace(root_height_obs=True))
        self.contact_forces = torch.zeros((count, 7, 3))
        self.contact_forces[:, [2, 3], 2] = 20
        self.body_vel = torch.zeros((count, 7, 3))
        self.torques, self.torque_limits = torch.zeros((count, 29)), torch.ones(29)
        self.projected_gravity = torch.tensor([[0., 0., -1.]]).expand(count, -1).clone()
        self.offsets = torch.tensor([[0., 0., 0.], [0., 0., .1], [0., .1, -.6],
                                     [0., -.1, -.6], [.1, .3, .1], [.1, -.3, .1], [0., 0., .3]])
        self.reset_log, self.step_count, self.terminate_at = [], 0, None

    def update_fk(self):
        self.base_quat = self.robot_root_states[:, 3:7]
        q = self.base_quat[:, None].expand(-1, self.num_bodies, -1).clone()
        q[:, :, :3] *= -1
        rel = self.offsets[None].expand(self.num_envs, -1, -1)
        rotated = quat_rotate_inverse(q.reshape(-1, 4), rel.reshape(-1, 3), w_last=True)
        self.body_pos = rotated.reshape(self.num_envs, self.num_bodies, 3) + self.robot_root_states[:, None, :3]
        self.body_rot = self.base_quat[:, None].expand(-1, self.num_bodies, -1).clone()

    def reset_all(self, target_states):
        self.robot_root_states = target_states['root_states'].clone()
        self.dof_pos = target_states['dof_states'][:, :, 0].clone()
        self.reset_log.append({k: v.clone() for k, v in target_states.items()})
        self.step_count = 0
        self.update_fk()

    def get_observation(self, **kwargs):
        return {'state': self.dof_pos}

    def step(self, action):
        self.step_count += 1
        if hasattr(self, 'physical_q'):
            self.dof_pos = self.physical_q.clone()
        if hasattr(self, 'physical_height'):
            self.robot_root_states[:, 2] = self.physical_height + self.env_origins[:, 2]
        self.update_fk()
        if self.step_count == getattr(self, 'nonfinite_at', None):
            if self.nonfinite_kind == 'root_velocity':
                self.robot_root_states[0, 7] = float('nan')
            elif self.nonfinite_kind == 'joint_velocity':
                self.dof_vel[0, 0] = float('nan')
            elif self.nonfinite_kind == 'body_velocity':
                self.body_vel[0, 2, 0] = float('nan')
            elif self.nonfinite_kind == 'body_position':
                self.body_pos[0, 4, 0] = float('nan')
        term = torch.zeros(self.num_envs, dtype=torch.bool)
        if self.step_count == self.terminate_at:
            term[0] = True
        return None, None, term, {}


class Env:
    include_last_action = True
    include_history_actor = True

    def __init__(self, count):
        self._env, self.num_envs = Core(count), count


class Policy:
    def __init__(self):
        self.calls = []

    def goal_inference(self, goal):
        self.calls.append(goal)
        z = torch.zeros((len(goal['last_action']), 256))
        z[:, 0] = goal['state'][:, 0]
        return z

    def act(self, obs, z, mean):
        assert mean
        return torch.zeros((len(z), 29))


@pytest.fixture(autouse=True)
def native_preprocessing_contract(monkeypatch):
    def observation(core, motion, q, **kwargs):
        # 保留原生预处理接口；几何变换由真实 quat_rotate_inverse 执行。
        return q, motion['rg_rot_t']
    monkeypatch.setattr(rollout, '_motion_observations', observation)


def prepare(count, tasks):
    env, policy = Env(count), Policy()
    evaluator = rollout.PoseEvaluator(env, policy, tasks)
    return env, policy, evaluator


def test_qpos_keeps_full_root_rotation_and_checks_joint_contract():
    q = (.98, .1, .02, .04)
    t = task(quaternion=q)
    qp = rollout.canonical_task_qpos(t, 29)
    np.testing.assert_allclose(qp[3:7], np.array(q) / np.linalg.norm(q), rtol=1e-6)
    assert np.any(qp[4:7] != 0)
    t['dof_pos'][0] += .01
    with pytest.raises(ValueError, match='disagrees'):
        rollout.canonical_task_qpos(t, 29)
    with pytest.raises(ValueError, match='nonzero'):
        rollout.canonical_task_qpos(task(quaternion=(0., 0., 0., 0.)), 29)


def test_batched_goal_encoding_pads_only_tail_and_uses_root_local_fk():
    q = (np.cos(.12), np.sin(.12), 0., 0.)
    tasks = [task(value=(i + 1) / 10, quaternion=q) for i in range(5)]
    env, policy, evaluator = prepare(2, tasks)
    assert len(env._env.reset_log) == 3
    assert len(policy.calls) == 3
    assert len(evaluator.targets) == 5
    np.testing.assert_allclose([t['z'][0] for t in evaluator.targets], [.1, .2, .3, .4, .5])
    for target in evaluator.targets:
        np.testing.assert_allclose(target['body'], env._env.offsets, atol=5e-7)
    np.testing.assert_allclose(env._env.reset_log[0]['root_states'][0, 3:7], [q[1], q[2], q[3], q[0]])
    assert torch.count_nonzero(policy.calls[-1]['last_action']) == 0


def test_task_seed_cartesian_order_and_pairwise_initial_perturbations():
    tasks = [task(value=.1), task(value=.2)]
    env, _, evaluator = prepare(4, tasks)
    env._env.physical_q = torch.stack([evaluator.targets[i]['q'] for i in [1, 1, 0, 0]])
    env._env.physical_height = .645
    scores, rows, _ = evaluator.evaluate(np.zeros((2, 256)), [1, 0], [0, 11], 3)
    assert [r['task_id'] for r in rows] == [1, 1, 0, 0]
    assert [r['seed'] for r in rows] == [0, 11, 0, 11]
    assert all(r['success'] for r in rows)
    np.testing.assert_allclose(scores, 0, atol=1e-9)
    np.testing.assert_array_equal(env._env.reset_log[-1]['dof_states'][0], env._env.reset_log[-1]['dof_states'][2])
    np.testing.assert_array_equal(env._env.reset_log[-1]['dof_states'][1], env._env.reset_log[-1]['dof_states'][3])
    assert rows[0]['support_fraction'] == pytest.approx(1)
    assert rows[0]['mean_knee_angle_rad'] == pytest.approx(1.2)
    assert rows[0]['final_hold']
    assert rows[0]['last_second_hold_fraction'] == pytest.approx(1)
    assert rows[0]['last_second_support_fraction'] == pytest.approx(1)
    assert rows[0]['last_second_depth_fraction'] == pytest.approx(1)


def test_sticky_failure_is_not_erased_when_term_clears_next_step():
    env, _, evaluator = prepare(1, [task()])
    env._env.physical_q = evaluator.targets[0]['q'][None]
    env._env.physical_height = .645
    env._env.terminate_at = 3
    resets = len(env._env.reset_log)
    scores, rows, _ = evaluator.evaluate(np.zeros((1, 256)), 0, [0], 3)
    assert len(env._env.reset_log) == resets + 1
    assert rows[0]['survival_s'] == pytest.approx(.2)
    assert rows[0]['hold_fraction'] == 0
    assert not rows[0]['success']
    assert scores[0] == pytest.approx(-28 * 100 / 30)


def test_explicit_squat_limits_add_cost_without_changing_legacy_cost():
    def run(**limits):
        env, _, evaluator = prepare(1, [task(height=.52, knee=1., **limits)])
        env._env.physical_q = evaluator.targets[0]['q'][None]
        env._env.physical_height = .52
        return evaluator.evaluate(np.zeros((1, 256)), 0, [0], 3)
    old_score, old_rows, _ = run()
    new_score, new_rows, _ = run(max_root_height_m=.50, min_mean_knee_angle_rad=1.05)
    assert old_rows[0]['success']
    assert not new_rows[0]['success']
    assert new_rows[0]['depth_fraction'] == 0
    assert new_rows[0]['root_height_m'] == pytest.approx(.52)
    assert new_rows[0]['final_root_height_m'] == pytest.approx(.52)
    assert new_rows[0]['target_left_knee_angle_rad'] == pytest.approx(1.)
    expected_penalty = 1.5 * (.02 / .07) ** 2 + 2 * (.05 / .18) ** 2
    assert float(old_score[0] - new_score[0]) == pytest.approx(expected_penalty, abs=2e-6)


def test_task_mapping_and_batch_size_reject_errors_before_reset():
    assert rollout.candidate_task_ids(1, 3, 2) == [1, 1, 1]
    for invalid in ([0], [0, 2], [0, .5]):
        with pytest.raises(ValueError, match='task'):
            rollout.candidate_task_ids(invalid, 2, 2)
    env, _, evaluator = prepare(1, [task()])
    resets = len(env._env.reset_log)
    with pytest.raises(ValueError, match='candidate x seed'):
        evaluator.evaluate(np.zeros((1, 256)), 0, [0, 11], 3)
    assert len(env._env.reset_log) == resets


def test_nonfinite_final_state_is_json_null_and_still_counts_as_failure():
    env, _, evaluator = prepare(1, [task()])
    env._env.physical_q = evaluator.targets[0]['q'][None].clone()
    env._env.physical_q[:, [3, 9]] = float('nan')
    env._env.physical_height = float('nan')
    scores, rows, _ = evaluator.evaluate(np.zeros((1, 256)), 0, [0], 3)
    assert scores[0] == -100
    assert not rows[0]['success']
    assert rows[0]['survival_s'] == 0
    assert rows[0]['final_root_height_m'] is None
    assert rows[0]['final_lift_height_m'] is None
    assert rows[0]['final_left_knee_angle_rad'] is None
    assert rows[0]['final_right_knee_angle_rad'] is None
    encoded = json.dumps(rows, allow_nan=False)
    assert 'null' in encoded


@pytest.mark.parametrize('kind', ['root_velocity', 'joint_velocity', 'body_velocity', 'body_position'])
def test_nonfinite_only_on_last_step_cannot_pass_despite_over_90_percent_hold(kind):
    env, _, evaluator = prepare(1, [task()])
    core = env._env
    core.physical_q = evaluator.targets[0]['q'][None].clone()
    core.physical_height = .645
    core.nonfinite_at, core.nonfinite_kind = 50, kind
    scores, rows, _ = evaluator.evaluate(np.zeros((1, 256)), 0, [0], 5)
    # 早先姿态保持比例已经足够，必须由非有限状态触发 sticky 失败。
    assert rows[0]['hold_fraction'] > .9
    assert not rows[0]['success']
    assert rows[0]['survival_s'] == pytest.approx(4.9, abs=5e-6)
    assert scores[0] == pytest.approx(-100 / 50)
    assert rows[0]['final_root_height_m'] == pytest.approx(.645)
    assert torch.isfinite(core.dof_pos).all()
    assert torch.isfinite(core.robot_root_states[:, :7]).all()
    assert not rows[0]['final_hold']
    assert rows[0]['last_second_hold_fraction'] == pytest.approx(.9)
    assert rows[0]['last_second_support_fraction'] == pytest.approx(.9)
    assert rows[0]['last_second_depth_fraction'] == pytest.approx(.9)
    json.dumps(rows, allow_nan=False)
