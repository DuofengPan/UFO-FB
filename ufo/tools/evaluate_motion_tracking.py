"""Batch checkpoint tracking evaluation with per-clip diagnostics and saved playback.

No training, no objects, reference-state initialization, deterministic mean actions,
noise/DR disabled. Fall flags are screening heuristics, not a feasibility proof.
"""

from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MUJOCO_GL", "egl")
import argparse
import json
import math
import random
import time
from pathlib import Path

import joblib
import numpy as np
import torch
from torch.utils._pytree import tree_map

from ufo.agents.common.checkpoint import checkpoint_load_device, load_model_from_checkpoint_dir
from ufo.inference.runtime import _target_states_from_obs, load_mjlab_env_cfg
from ufo.motion.reference import get_backward_observation
from ufo.tools.bones_motion_import import sha256


@torch.no_grad()
def evaluate(args):
    output = Path(args.output).resolve()
    if output.exists():
        raise ValueError(f"Refusing to overwrite {output}")
    output.mkdir(parents=True)
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.set_num_threads(1)
    started = time.monotonic()
    model_folder = Path(args.model_folder).resolve()
    data_path = Path(args.data_path).resolve()
    cfg, spec = load_mjlab_env_cfg(
        model_folder,
        data_path=data_path,
        robot_config=args.robot_config,
        device=args.device,
        disable_dr=True,
        disable_obs_noise=True,
        max_episode_length_s=10000.0,
    )
    model = load_model_from_checkpoint_dir(model_folder / "checkpoint", device=checkpoint_load_device(args.device))
    model.to(args.device)
    model.eval()
    count = len(joblib.load(data_path))
    env, _ = cfg.build(num_envs=count)
    core = env._env
    trajectories = []
    records = []
    try:
        core.is_evaluating = True
        core._motion_lib.load_all_motions()
        if int(core._motion_lib._num_unique_motions) != count:
            raise ValueError("Motion count changed while loading")
        contexts = []
        refs = []
        init = []
        for motion_id in range(count):
            obs, ref = get_backward_observation(core, motion_id, use_root_height_obs=cfg.root_height_obs)
            z = model.tracking_inference(tree_map(lambda x: x[1:].to(args.device), obs))
            if len(z) < 1:
                raise ValueError("Empty tracking context")
            contexts.append(z)
            refs.append(ref)
            init.append(_target_states_from_obs(ref, device=args.device, num_dof=core.num_dof))
            print(f"prepared {motion_id + 1}/{count}: {core._motion_lib.curr_motion_keys[motion_id]}, steps={len(z)}", flush=True)
        lengths = torch.tensor([len(z) for z in contexts], device=args.device)
        maxlen = int(lengths.max())
        times = torch.arange(maxlen, device=args.device)
        zs = torch.stack([z[times.clamp_max(len(z) - 1)] for z in contexts])
        target_q = torch.stack([r["dof_pos"][(times + 1).clamp_max(len(r["dof_pos"]) - 1)] for r in refs])
        target_body = torch.stack([r["ref_body_pos"][(times + 1).clamp_max(len(r["ref_body_pos"]) - 1), : core.num_bodies] for r in refs])
        initial = {"root_states": torch.cat([s["root_states"] for s in init]), "dof_states": torch.cat([s["dof_states"] for s in init])}
        obs, _ = env.reset(target_states=initial, to_numpy=False)
        if not torch.allclose(core.dof_pos, initial["dof_states"][..., 0], atol=1e-6):
            raise ValueError("Reference initialization failed")
        hand_ids = [list(core.body_names).index(n) for n in spec.robot.hands]
        # Accumulate on GPU; transfer once. All per-motion means use its own length.
        stats = torch.empty((maxlen, count, 6), device=args.device)
        qpos = []
        fallen = torch.zeros(count, dtype=torch.bool, device=args.device)
        fall_run = torch.zeros(count, dtype=torch.long, device=args.device)
        first_fall = torch.full((count,), -1, device=args.device, dtype=torch.long)
        fall_hold = max(1, math.ceil(args.fall_hold_s / core.dt))
        rollout_start = time.monotonic()
        for step in range(maxlen):
            actions = model.act(obs, zs[:, step], mean=True)
            obs, _, terminated, truncated, _ = env.step(actions, to_numpy=False)
            if bool((terminated | truncated).any()):
                raise RuntimeError("Unexpected reset; refusing invalid tracking metrics")
            valid = step < lengths
            pos = core.body_pos
            root = pos[:, 0]
            local = pos - root[:, None]
            target_local = target_body[:, step] - target_body[:, step, :1]
            local_error = torch.linalg.vector_norm(local - target_local, dim=-1)
            height = root[:, 2]
            # Torso local Z axis projected onto world Z, using XYZW quaternions.
            torso = core.body_rot[:, core.torso_index]
            upright = 1 - 2 * (torso[:, 0] ** 2 + torso[:, 1] ** 2)
            bad = (height < args.fall_height_m) | (upright < math.cos(math.radians(args.fall_tilt_deg)))
            fall_run = torch.where(bad & valid, fall_run + 1, 0)
            new_fall = (fall_run >= fall_hold) & ~fallen & valid
            first_fall = torch.where(new_fall, step - fall_hold + 1, first_fall)
            fallen |= new_fall
            stats[step, :, 0] = (core.dof_pos - target_q[:, step]).abs().mean(-1)
            stats[step, :, 1] = local_error.mean(-1)
            stats[step, :, 2] = local_error[:, hand_ids].mean(-1)
            stats[step, :, 3] = torch.linalg.vector_norm(root - target_body[:, step, 0], dim=-1)
            stats[step, :, 4] = height
            stats[step, :, 5] = torch.rad2deg(torch.acos(upright.clamp(-1, 1)))
            qpos.append(torch.cat([core.robot_root_states[:, :3], core.base_quat[:, [3, 0, 1, 2]], core.dof_pos], dim=-1).clone())
            if step % 100 == 0 or step == maxlen - 1:
                print(f"rollout {step + 1}/{maxlen}", flush=True)
        torch.cuda.synchronize() if args.device.startswith("cuda") else None
        rollout_seconds = time.monotonic() - rollout_start
        values = stats.cpu().numpy()
        qposes = torch.stack(qpos).cpu().numpy()
        first = first_fall.cpu().numpy()
        for i in range(count):
            n = len(contexts[i])
            arr = values[:n, i]
            f = int(first[i])
            before = max(0, f) if f >= 0 else n
            record = dict(
                motion_id=i,
                motion_key=str(core._motion_lib.curr_motion_keys[i]),
                steps=n,
                duration_s=n * core.dt,
                joint_mae_rad=float(arr[:, 0].mean()),
                local_body_error_m=float(arr[:, 1].mean()),
                local_hand_error_m=float(arr[:, 2].mean()),
                root_error_m=float(arr[:, 3].mean()),
                pelvis_min_m=float(arr[:, 4].min()),
                torso_tilt_max_deg=float(arr[:, 5].max()),
                fall_detected=f >= 0,
                first_fall_s=f * core.dt if f >= 0 else None,
                fraction_before_fall=before / n,
                joint_mae_before_fall_rad=float(arr[:before, 0].mean()) if before else None,
            )
            record["screening_fail_reasons"] = [
                name
                for name, failed in [
                    ("fall", record["fall_detected"]),
                    ("joint_mae", record["joint_mae_rad"] >= args.mae_threshold),
                    ("local_body_error", record["local_body_error_m"] >= args.body_threshold),
                    ("local_hand_error", record["local_hand_error_m"] >= args.hand_threshold),
                    ("root_error", record["root_error_m"] >= args.root_threshold),
                ]
                if failed
            ]
            record["screening_pass"] = not record["screening_fail_reasons"]
            records.append(record)
            ref = refs[i]
            reference_qpos = (
                torch.cat(
                    [ref["ref_body_pos"][1 : n + 1, 0], ref["ref_body_rots"][1 : n + 1, 0][:, [3, 0, 1, 2]], ref["dof_pos"][1 : n + 1]],
                    dim=-1,
                )
                .cpu()
                .numpy()
            )
            trajectories.append(dict(motion_key=record["motion_key"], policy_qpos=qposes[:n, i], reference_qpos=reference_qpos, dt=core.dt))
        result = dict(
            status="complete",
            model_folder=str(model_folder),
            weights_sha256=sha256(model_folder / "checkpoint/model/model.safetensors"),
            data_path=str(data_path),
            data_sha256=sha256(data_path),
            robot=spec.robot.name,
            robot_xml_sha256=sha256(spec.robot.xml_path),
            device=args.device,
            seed=args.seed,
            dr=False,
            observation_noise=False,
            initialization="reference first state with reference velocities",
            mean_actions=True,
            control_dt_s=core.dt,
            rollout_wall_s=rollout_seconds,
            elapsed_wall_s=time.monotonic() - started,
            definitions=dict(
                local_body_error="mean link position distance after subtracting pelvis translation; world-oriented axes",
                local_hand_error="same, wrist links only",
                root_error="world root position distance from reference",
                fall=f"pelvis height < {args.fall_height_m}m OR torso tilt > {args.fall_tilt_deg}deg, for {fall_hold} consecutive steps",
                screening_pass=f"no heuristic fall AND joint MAE < {args.mae_threshold}rad AND local body error < {args.body_threshold}m AND local hand error < {args.hand_threshold}m AND root error < {args.root_threshold}m; custom screen, not official benchmark",
            ),
            motion_count=count,
            screening_pass_count=sum(r["screening_pass"] for r in records),
            fall_count=sum(r["fall_detected"] for r in records),
            mean_joint_mae_rad=float(np.mean([r["joint_mae_rad"] for r in records])),
            mean_local_body_error_m=float(np.mean([r["local_body_error_m"] for r in records])),
            motions=records,
        )
        joblib.dump(trajectories, output / "trajectories.pkl", compress=3)
        (output / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
        print(json.dumps({k: v for k, v in result.items() if k != "motions"}, ensure_ascii=False, indent=2), flush=True)
        return result
    finally:
        env.close()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model-folder", type=Path, required=True)
    p.add_argument("--data-path", type=Path, required=True)
    p.add_argument("--robot-config", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--fall-height-m", type=float, default=0.25)
    p.add_argument("--fall-tilt-deg", type=float, default=80.0)
    p.add_argument("--fall-hold-s", type=float, default=0.2)
    p.add_argument("--mae-threshold", type=float, default=0.3)
    p.add_argument("--body-threshold", type=float, default=0.15)
    p.add_argument("--hand-threshold", type=float, default=0.2)
    p.add_argument("--root-threshold", type=float, default=0.3)
    args = p.parse_args()
    if (
        not 0 < args.fall_tilt_deg < 180
        or min(args.fall_height_m, args.fall_hold_s, args.mae_threshold, args.body_threshold, args.hand_threshold, args.root_threshold) <= 0
    ):
        p.error("Thresholds must be positive and tilt < 180 degrees")
    evaluate(args)


if __name__ == "__main__":
    main()
