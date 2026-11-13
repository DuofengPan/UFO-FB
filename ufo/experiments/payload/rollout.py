"""固定姿态闭环评估：原始 Goal 批量编码、候选与种子配对、失败后不重置。"""
import math
from numbers import Integral

import numpy as np
import torch

from ufo.math import quat_rotate_inverse
from ufo.motion.reference import _motion_observations


def finite_or_none(value):
    """记录真实非有限末状态为 null，不伪造为零，也不阻止失败结果归档。"""
    result = float(value)
    return result if math.isfinite(result) else None


def candidate_task_ids(task_id, candidate_count, task_count):
    """一个任务配多个 z，或者每个 z 配一个任务；种子展开在之后进行。"""
    ids = [int(task_id)] * candidate_count if isinstance(task_id, Integral) else list(task_id)
    if len(ids) != candidate_count:
        raise ValueError("task_id must be an int or contain one task per candidate")
    if any(not isinstance(i, Integral) or i < 0 or i >= task_count for i in ids):
        raise ValueError("task_id contains an invalid task index")
    return [int(i) for i in ids]


def canonical_task_qpos(task, num_dof):
    """MuJoCo qpos 为 xyz+wxyz+关节；保留参考根部 roll/pitch。"""
    qp = np.asarray(task['qpos'], dtype=np.float32).copy()
    if qp.shape != (num_dof + 7,) or not np.isfinite(qp).all():
        raise ValueError("task qpos must contain finite xyz, wxyz and all control joints")
    norm = float(np.linalg.norm(qp[3:7]))
    if norm < 1e-6:
        raise ValueError("task root quaternion must be nonzero")
    qp[3:7] /= norm
    if 'dof_pos' in task:
        q = np.asarray(task['dof_pos'], dtype=np.float32)
        if q.shape != (num_dof,) or not np.allclose(q, qp[7:], atol=1e-6, rtol=0):
            raise ValueError("task dof_pos disagrees with qpos")
    return qp


class PoseEvaluator:
    """固定模型与物理条件；支持数百个不同源姿态的向量化无负载筛选。"""

    @torch.no_grad()
    def __init__(self, env, policy, tasks):
        if not tasks:
            raise ValueError("at least one task is required")
        self.env, self.core, self.policy, self.tasks = env, env._env, policy, tasks
        c = self.core
        self.device, self.dt = c.device, float(c.dt)
        self.body_names = list(c.body_names[:c.num_bodies])
        self.feet = [self.body_names.index(x + '_ankle_roll_link') for x in ('left', 'right')]
        self.key = [self.body_names.index(n) for n in (
            'waist_roll_link', 'left_ankle_roll_link', 'right_ankle_roll_link',
            'left_wrist_yaw_link', 'right_wrist_yaw_link')]
        names = list(getattr(c, 'dof_names', ()))
        self.knees = ([names.index(x + '_knee_joint') for x in ('left', 'right')]
                      if all(x + '_knee_joint' in names for x in ('left', 'right'))
                      else [3, 9])  # 旧 Astro 29-DoF 的显式关节顺序。
        self.joint_groups = {
            'leg': [i for i, n in enumerate(names) if any(x in n for x in ('hip_', 'knee_', 'ankle_'))],
            'waist': [i for i, n in enumerate(names) if 'waist_' in n],
            'arm': [i for i, n in enumerate(names) if any(x in n for x in ('shoulder_', 'elbow_', 'wrist_'))],
        }
        if not names and c.num_dof == 29:
            self.joint_groups = {'leg': list(range(12)), 'waist': list(range(12, 15)),
                                 'arm': list(range(15, 29))}
        self.targets = []
        # 每块最多 N 个目标：只做一次 FK/reset 和一次 Backward 调用。
        # 尾块填充末目标，既不改变任务数，也不把填充项写入目标库。
        for start in range(0, len(tasks), c.num_envs):
            chunk = tasks[start:start + c.num_envs]
            qps = [canonical_task_qpos(t, c.num_dof) for t in chunk]
            count = len(qps)
            qps.extend([qps[-1]] * (c.num_envs - count))
            qp = torch.as_tensor(np.stack(qps), device=self.device)
            roots = torch.zeros((c.num_envs, 13), device=self.device)
            roots[:, :3] = qp[:, :3] + c.env_origins
            roots[:, 3:7] = qp[:, [4, 5, 6, 3]]
            dofs = torch.zeros((c.num_envs, c.num_dof, 2), device=self.device)
            dofs[:, :, 0] = qp[:, 7:]
            c.reset_all(target_states={'root_states': roots, 'dof_states': dofs})
            body = c.body_pos.clone() - c.env_origins[:, None]
            rot = c.body_rot.clone()
            state = {'rg_pos_t': body, 'rg_rot_t': rot,
                     'body_vel_t': torch.zeros_like(body),
                     'body_ang_vel_t': torch.zeros_like(body),
                     'dof_vel': torch.zeros_like(qp[:, 7:])}
            filtered, priv = _motion_observations(
                c, state, qp[:, 7:] - c.default_dof_pos,
                root_height_obs=bool(c.config.obs.root_height_obs), use_obs_filter=True)
            z = policy.goal_inference({'state': filtered, 'privileged_state': priv,
                                       'last_action': torch.zeros_like(qp[:, 7:])})
            relative = body - body[:, :1]
            rootq = c.base_quat[:, None].expand(-1, c.num_bodies, -1)
            local = quat_rotate_inverse(rootq.reshape(-1, 4), relative.reshape(-1, 3),
                                        w_last=True).reshape(c.num_envs, c.num_bodies, 3)
            for j in range(count):
                self.targets.append({'q': qp[j, 7:].clone(), 'body': local[j].clone(),
                                     'height': qp[j, 2].clone(),
                                     'z': z[j].float().cpu().numpy().copy()})

    @torch.no_grad()
    def evaluate(self, zs, task_id, seeds, horizon_s, record=False):
        """z 顺序在外、同一 seeds 顺序在内；重置包含历史和 last action。"""
        c, device, N = self.core, self.device, self.core.num_envs
        zs = np.asarray(zs, dtype=np.float32).reshape(-1, 256)
        if not seeds or len(zs) * len(seeds) != N:
            raise ValueError('candidate x seed must equal env count')
        ids = candidate_task_ids(task_id, len(zs), len(self.targets))
        expanded_ids = [i for i in ids for _ in seeds]
        target_rows = [self.targets[i] for i in expanded_ids]
        tasks = [self.tasks[i] for i in expanded_ids]
        q = torch.stack([t['q'] for t in target_rows])
        target_body = torch.stack([t['body'] for t in target_rows])
        height = torch.stack([t['height'] for t in target_rows])
        max_height = torch.tensor([t.get('max_root_height_m', float('inf')) for t in tasks], device=device)
        min_knee = torch.tensor([t.get('min_mean_knee_angle_rad', -float('inf')) for t in tasks], device=device)
        is_both = torch.tensor([t['support'] == 'both' for t in tasks], device=device)
        support_side = torch.tensor([0 if t['support'] == 'left' else 1 for t in tasks], device=device)
        z = torch.tensor(np.repeat(zs, len(seeds), axis=0), device=device)
        roots = torch.zeros((N, 13), device=device)
        roots[:, 2] = .645
        roots[:, :3] += c.env_origins
        roots[:, 6] = 1
        dofs = torch.zeros((N, c.num_dof, 2), device=device)
        dofs[:, :, 0] = c.default_dof_pos
        for k, seed in enumerate(seeds):
            if seed:
                gen = torch.Generator(device=device).manual_seed(seed)
                perturb = .015 * torch.randn((c.num_dof,), device=device, generator=gen)
                dofs[k::len(seeds), :, 0] += perturb
        c.reset_all(target_states={'root_states': roots, 'dof_states': dofs})
        c.is_evaluating = True
        obs = c.get_observation(to_numpy=False, include_last_action=self.env.include_last_action,
                                include_history_actor=self.env.include_history_actor)
        alive = torch.ones(N, device=device, dtype=torch.bool)
        steps, warmup = round(horizon_s / self.dt), round(2 / self.dt)
        if steps <= 0:
            raise ValueError('horizon_s must contain at least one control step')
        tail_steps = min(steps, max(1, round(1 / self.dt)))
        tail = {k: torch.zeros(N, device=device) for k in ('hold', 'support', 'depth')}
        names = ('cost', 'joint', 'height', 'body', 'speed', 'tilt', 'slip', 'torque', 'smooth',
                 'semantic', 'count', 'bad_contact', 'root_height', 'lift_height', 'support',
                 'left_knee', 'right_knee', 'mean_knee', 'depth', 'leg_joint', 'waist_joint', 'arm_joint')
        sums = {k: torch.zeros(N, device=device) for k in names}
        survival = torch.zeros(N, device=device)
        max_drift = torch.zeros(N, device=device)
        previous = torch.zeros((N, c.num_dof), device=device)
        history = []
        batch = torch.arange(N, device=device)
        for t in range(steps):
            action = self.policy.act(obs, z, mean=True)
            _, _, term, info = c.step(action)
            obs = c.get_observation(to_numpy=False, include_last_action=self.env.include_last_action,
                                    include_history_actor=self.env.include_history_actor)
            position = c.robot_root_states[:, :3] - c.env_origins
            drift = position[:, :2].norm(dim=-1)
            tilt = torch.acos((-c.projected_gravity[:, 2]).clamp(-1, 1))
            # 最后一帧的速度异常也必须判失败，不能等下一帧位置/Actor 被污染。
            finite = (torch.isfinite(c.robot_root_states).all(-1)
                      & torch.isfinite(c.dof_pos).all(-1)
                      & torch.isfinite(c.dof_vel).all(-1)
                      & torch.isfinite(c.body_pos).flatten(1).all(-1)
                      & torch.isfinite(c.body_vel).flatten(1).all(-1)
                      & torch.isfinite(action).all(-1))
            alive &= finite & ~term.bool() & (position[:, 2] > .28) & (tilt < 1.05)
            survival += alive * self.dt
            max_drift = torch.maximum(max_drift, torch.where(alive, drift, torch.zeros_like(drift)))
            joint_errors = (c.dof_pos - q).abs()
            joint = joint_errors.mean(-1)
            he = (position[:, 2] - height).abs()
            current_rel = c.body_pos - c.body_pos[:, :1]
            rootq = c.base_quat[:, None].expand(-1, c.num_bodies, -1)
            local = quat_rotate_inverse(rootq.reshape(-1, 4), current_rel.reshape(-1, 3),
                                        w_last=True).reshape(N, c.num_bodies, 3)
            be = (local[:, self.key] - target_body[:, self.key]).norm(dim=-1).mean(-1)
            speed = c.robot_root_states[:, 7:9].norm(dim=-1)
            contact = c.contact_forces[:, self.feet].norm(dim=-1) > 5
            slip = (c.body_vel[:, self.feet, :2].norm(dim=-1) * contact).sum(-1)
            torque = (c.torques.abs() / c.torque_limits).clamp(0, 2)
            saturation = (torque > .95).float().mean(-1)
            smooth = (action - previous).square().mean(-1)
            previous = action.clone()
            nonfeet = [j for j in range(c.num_bodies) if j not in self.feet]
            undesired = (c.contact_forces[:, nonfeet].norm(dim=-1) > 10).any(-1)
            foot_height = c.body_pos[:, self.feet, 2]
            lift_height = foot_height[batch, 1 - support_side] - foot_height[batch, support_side]
            single_ok = (contact[batch, support_side] & ~contact[batch, 1 - support_side]
                         & (lift_height > .07))
            support_ok = torch.where(is_both, contact.all(-1), single_ok)
            lift_height = torch.where(is_both, (foot_height[:, 0] - foot_height[:, 1]).abs(), lift_height)
            left_knee, right_knee = c.dof_pos[:, self.knees[0]], c.dof_pos[:, self.knees[1]]
            mean_knee = (left_knee + right_knee) / 2
            depth_ok = (position[:, 2] <= max_height) & (mean_knee >= min_knee)
            semantic = (alive & (joint < .18) & (he < .07) & (be < .10) & (drift < .15)
                        & (tilt < .35) & support_ok & ~undesired & depth_ok)
            if t >= steps - tail_steps:
                tail['hold'] += semantic.float()
                tail['support'] += (alive & support_ok).float()
                tail['depth'] += (alive & depth_ok).float()
            # 旧任务代价、常数、阈值均保留。仅显式指定深蹲字段时追加约束。
            cost = (2 * (joint / .18).square() + 1.5 * (he / .07).square()
                    + 1.5 * (be / .10).square() + .5 * (drift / .15).square()
                    + .3 * (speed / .1).square() + .2 * (tilt / .35).square()
                    + .1 * (slip / .1).square() + .2 * saturation + .02 * smooth
                    + 2 * (~support_ok).float() + 3 * undesired.float())
            height_excess = (position[:, 2] - max_height).clamp(min=0)
            knee_deficit = (min_knee - mean_knee).clamp(min=0)
            cost += 1.5 * (height_excess / .07).square() + 2 * (knee_deficit / .18).square()
            cost = torch.nan_to_num(cost, nan=100., posinf=100., neginf=100.).clamp(max=100)
            sums['cost'] += torch.where(alive, cost, torch.full_like(cost, 100))
            if t >= warmup:
                values = dict(joint=joint, height=he, body=be, speed=speed, tilt=tilt, slip=slip,
                              torque=saturation, smooth=smooth, semantic=semantic.float(),
                              bad_contact=undesired.float(), root_height=position[:, 2],
                              lift_height=lift_height, support=support_ok.float(), left_knee=left_knee,
                              right_knee=right_knee, mean_knee=mean_knee, depth=depth_ok.float())
                for group, indices in self.joint_groups.items():
                    values[group + '_joint'] = (joint_errors[:, indices].mean(-1) if indices
                                               else torch.zeros(N, device=device))
                for key, value in values.items():
                    sums[key] += torch.nan_to_num(value) * alive
                sums['count'] += alive
            if record:
                qp = self.env._get_qpos_qvel(to_numpy=False)[0].clone()
                qp[:, :3] -= c.env_origins
                history.append(qp.cpu().numpy())
        count = sums['count'].clamp(min=1)
        hold_steps = max(1, steps - warmup)
        rows = []
        for i in range(N):
            row = dict(seed=int(seeds[i % len(seeds)]), task_id=expanded_ids[i],
                       score=float(-sums['cost'][i] / steps), survival_s=float(survival[i]),
                       max_drift_m=float(max_drift[i]), joint_mae_rad=float(sums['joint'][i] / count[i]),
                       height_error_m=float(sums['height'][i] / count[i]),
                       key_body_error_m=float(sums['body'][i] / count[i]),
                       speed_mps=float(sums['speed'][i] / count[i]),
                       tilt_deg=float(sums['tilt'][i] / count[i] * 180 / np.pi),
                       slip_mps=float(sums['slip'][i] / count[i]),
                       torque_saturation_fraction=float(sums['torque'][i] / count[i]),
                       action_delta_mse=float(sums['smooth'][i] / count[i]),
                       undesired_contact_fraction=float(sums['bad_contact'][i] / count[i]),
                       hold_fraction=float(sums['semantic'][i] / hold_steps),
                       success=bool(alive[i] and sums['semantic'][i] / hold_steps > .9),
                       root_height_m=float(sums['root_height'][i] / count[i]),
                       lift_height_m=float(sums['lift_height'][i] / count[i]),
                       support_fraction=float(sums['support'][i] / hold_steps),
                       depth_fraction=float(sums['depth'][i] / hold_steps),
                       left_knee_angle_rad=float(sums['left_knee'][i] / count[i]),
                       right_knee_angle_rad=float(sums['right_knee'][i] / count[i]),
                       mean_knee_angle_rad=float(sums['mean_knee'][i] / count[i]),
                       target_left_knee_angle_rad=float(q[i, self.knees[0]]),
                       target_right_knee_angle_rad=float(q[i, self.knees[1]]),
                       final_root_height_m=finite_or_none(position[i, 2]),
                       final_tilt_deg=finite_or_none(tilt[i] * 180 / np.pi),
                       final_lift_height_m=finite_or_none(lift_height[i]),
                       final_left_knee_angle_rad=finite_or_none(left_knee[i]),
                       final_right_knee_angle_rad=finite_or_none(right_knee[i]),
                       final_hold=bool(semantic[i]),
                       last_second_hold_fraction=float(tail['hold'][i] / tail_steps),
                       last_second_support_fraction=float(tail['support'][i] / tail_steps),
                       last_second_depth_fraction=float(tail['depth'][i] / tail_steps))
            for group in self.joint_groups:
                row[group + '_joint_mae_rad'] = float(sums[group + '_joint'][i] / count[i])
            rows.append(row)
        scores = np.array([r['score'] for r in rows]).reshape(len(zs), len(seeds)).mean(-1)
        return scores, rows, np.asarray(history) if record else None
