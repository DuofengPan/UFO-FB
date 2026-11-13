#!/usr/bin/env python3
"""固定世界相机回放已记录 qpos；不启动策略、不重跑物理、不修改模型资产。

python render_study.py /data/.../study --simple-geometry --failures
python render_study.py /data/.../study --check

主视频左右使用同一姿态、同一负载、同一种子，分别为原始 z0 与 CEM z*。
按 dt 与 stride 计算真实播放速度；输出视频、参考姿态 JPG 和渲染溯源清单。
--help 仅依赖 Python 标准库，--check 只读取数据且不创建 EGL 上下文。
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path


@dataclass(frozen=True)
class Job:
    name: str
    title: str
    mass: float
    offset: tuple[float, float, float]
    xml: Path
    original: Path
    cem: Path
    seed: int
    output: Path
    failure: bool = False


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def payload(value):
    mass = float(value['mass_kg'])
    offset = tuple(float(x) for x in value['offset_m'])
    if not math.isfinite(mass) or mass < 0 or len(offset) != 3 or not all(map(math.isfinite, offset)):
        raise ValueError('payload requires nonnegative mass_kg and three finite offset_m values')
    return mass, offset


def same_payload(record, mass, offset):
    value = record.get('physics', {}).get('payload') or record.get('protocol', {}).get('physics', {}).get('payload')
    if value is None:
        raise ValueError('evaluation JSON has no explicit physics.payload')
    m, xyz = payload(value)
    return abs(m - mass) < 1e-8 and all(abs(a - b) < 1e-8 for a, b in zip(xyz, offset))


def plan(root, output, seed, names, failures):
    study = load_json(root / 'study.json')
    tasks = load_json(root / 'tasks.json')
    tasks = tasks['tasks'] if isinstance(tasks, dict) else tasks
    by_name = {t['name']: t for t in tasks}
    if len(by_name) != len(tasks):
        raise ValueError('tasks.json contains duplicate task names')
    jobs, selected, seen = [], {}, set()
    requested = set(names or ())
    for item in study['tasks']:
        name = str(item['name'])
        if name in seen or Path(name).name != name or name in ('.', '..'):
            raise ValueError(f'unsafe or duplicate study task name: {name!r}')
        seen.add(name)
        if requested and name not in requested:
            continue
        if name not in by_name:
            raise ValueError(f'task {name!r} missing in tasks.json')
        if 'main_payload' not in item:
            continue
        mass, xyz = payload(item['main_payload'])
        tag = f'm{mass:g}_x{xyz[0]:g}_y{xyz[1]:g}'
        base = root / 'eval' / f'{name}_{tag}'
        original, cem = Path(str(base) + '_original.npz'), Path(str(base) + '_cem.npz')
        xml = root / 'physics' / f'{tag}_z{xyz[2]:g}.xml'
        a_json, b_json = Path(str(base) + '_original.json'), Path(str(base) + '_cem.json')
        for path in (original, cem, xml, a_json, b_json):
            if not path.is_file():
                raise FileNotFoundError(f'cannot render an incomplete pair: {path}')
        a, b = load_json(a_json), load_json(b_json)
        if a.get('task') != name or b.get('task') != name:
            raise ValueError(f'evaluation task name mismatch: {name}')
        if a.get('condition') != 'original' or b.get('condition') != 'cem':
            raise ValueError(f'evaluation condition mismatch: {name}')
        if not same_payload(a, mass, xyz) or not same_payload(b, mass, xyz):
            raise ValueError(f'comparison does not use the same declared payload: {name}')
        a_seeds, b_seeds = {int(r['seed']) for r in a['rows']}, {int(r['seed']) for r in b['rows']}
        if seed not in a_seeds or seed not in b_seeds:
            raise ValueError(f'main seed {seed} missing from evaluation JSON: {name}')
        title = str(item.get('title', by_name[name].get('title', name)))
        jobs.append(Job(name, title, mass, xyz, xml, original, cem, seed,
                        output / f'{name}_main.mp4'))
        selected[name] = by_name[name]
        if failures:
            for row in b['rows']:
                if not isinstance(row.get('success'), bool):
                    raise ValueError(f'failure rendering requires explicit bool success: {b_json}')
                failure_seed = int(row['seed'])
                # 主视频已经保留该种子的失败；不再编码一份完全相同的视频。
                if row['success'] or failure_seed == seed:
                    continue
                if failure_seed not in a_seeds:
                    raise ValueError(f'failed CEM seed {failure_seed} has no matching original control')
                jobs.append(Job(name, title, mass, xyz, xml, original, cem, failure_seed,
                                output / f'{name}_failure_seed{failure_seed}.mp4', True))
    if requested - seen:
        raise ValueError(f'unknown requested task names: {sorted(requested - seen)}')
    if not jobs:
        raise ValueError('no complete main-payload comparisons selected')
    return jobs, selected


def trajectory(path, seed):
    import numpy as np
    with np.load(path, allow_pickle=False) as archive:
        dt = float(archive['dt'])
        if not math.isfinite(dt) or dt <= 0:
            raise ValueError(f'invalid control dt in {path}')
        if 'qpos_all' in archive:
            if 'seeds' not in archive:
                raise ValueError(f'qpos_all is missing seeds: {path}')
            seeds = [int(x) for x in archive['seeds'].tolist()]
            if len(seeds) != len(set(seeds)) or seed not in seeds:
                raise ValueError(f'seed {seed} unavailable or duplicated in {path}')
            all_qpos = archive['qpos_all']
            if all_qpos.ndim != 3 or all_qpos.shape[1] != len(seeds):
                raise ValueError(f'invalid qpos_all shape in {path}: {all_qpos.shape}')
            qpos = all_qpos[:, seeds.index(seed)].copy()
        else:
            seeds = [int(x) for x in archive['seeds'].tolist()] if 'seeds' in archive else []
            if not seeds or seeds[0] != seed:
                raise ValueError(f'qpos only represents the first recorded seed, not seed {seed}: {path}')
            qpos = archive['qpos'].copy()
    if qpos.ndim != 2 or qpos.shape[1] != 36 or not len(qpos) or not np.isfinite(qpos).all():
        raise ValueError(f'expected finite (T,36) recorded qpos; will not repair invalid rollout: {path}')
    return qpos, dt


def validate_pair(job):
    a, dt = trajectory(job.original, job.seed)
    b, bdt = trajectory(job.cem, job.seed)
    if len(a) != len(b) or abs(dt - bdt) > 1e-9:
        raise ValueError(f'original/CEM must share horizon and dt: {job.name}, seed {job.seed}')
    return a, b, dt


def run(args):
    root = args.root.resolve()
    output = (args.output or root / 'videos').resolve()
    jobs, tasks = plan(root, output, args.seed, args.tasks, args.failures)
    # 先核验全部轨迹，避免编码到中途才发现种子或长度不一致。
    for job in jobs:
        a, _, dt = validate_pair(job)
        print(f'{job.name}: seed={job.seed}, mass={job.mass:g}kg, frames={len(a)}, '
              f'dt={dt:.9g}s, duration={len(a) * dt:.6g}s, output={job.output.name}', flush=True)
    if args.check:
        print('CHECK OK: recorded trajectory pairs validated; no renderer or physics launched.')
        return
    os.environ.setdefault('MUJOCO_GL', 'egl')
    os.environ.setdefault('PYOPENGL_PLATFORM', 'egl')
    import numpy as np
    import mujoco
    from PIL import Image, ImageDraw, ImageFont
    from ufo.inference.runtime import MujocoQposRenderer, video_writer

    output.mkdir(parents=True, exist_ok=True)
    manifest_path = output / 'render_manifest.json'
    previous = ({item['output']: item for item in load_json(manifest_path).get('videos', [])}
                if manifest_path.is_file() else {})
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 14)
    except OSError:
        font = ImageFont.load_default()
    manifests, rendered_targets = [], set()
    renderers = {}
    try:
        def renderer_for(xml):
            if xml not in renderers:
                renderer = MujocoQposRenderer(xml, render_size=args.size,
                    camera_distance=args.distance, camera_azimuth=args.azimuth,
                    camera_elevation=args.elevation, expected_qpos_size=36)
                # 修改的是独立的回放渲染模型，绝不改 XML 或运行时物理模型。
                for gid in range(renderer.model.ngeom):
                    name = mujoco.mj_id2name(renderer.model, mujoco.mjtObj.mjOBJ_GEOM, gid)
                    if name and name.startswith('payload_visual'):
                        renderer.model.geom_group[gid] = 2
                options = mujoco.MjvOption()
                if args.simple_geometry:
                    options.geomgroup[:] = 0
                    options.geomgroup[[0, 2, 3]] = 1
                renderers[xml] = renderer, options
            return renderers[xml]

        def image_at(renderer, options, qpos):
            renderer.data.qpos[:] = qpos
            mujoco.mj_forward(renderer.model, renderer.data)
            renderer.camera.lookat[:] = args.lookat
            renderer.renderer.update_scene(renderer.data, camera=renderer.camera, scene_option=options)
            return renderer.renderer.render().copy()

        for job in jobs:
            a, b, dt = validate_pair(job)
            renderer, options = renderer_for(job.xml)
            size, header = args.size, 76
            fps, indices = 1 / (dt * args.stride), range(0, len(a), args.stride)
            source_identity = {
                'seed': job.seed, 'original_sha256': sha256(job.original),
                'cem_sha256': sha256(job.cem), 'physics_xml_sha256': sha256(job.xml),
                'stride': args.stride, 'panel_size': size, 'simple_geometry': args.simple_geometry,
                'camera_world_lookat': list(args.lookat), 'camera_distance': args.distance,
                'camera_azimuth': args.azimuth, 'camera_elevation': args.elevation,
            }
            if job.output.exists() and not args.overwrite:
                prior = previous.get(job.output.name, {})
                if (any(prior.get(k) != v for k, v in source_identity.items())
                        or prior.get('video_sha256') != sha256(job.output)):
                    raise ValueError(f'existing video has no matching render provenance; use --overwrite: {job.output}')
                print(f'SKIP existing {job.output}; use --overwrite to re-encode.', flush=True)
            else:
                with video_writer(job.output, shape=(size + header, 2 * size), fps=fps) as writer:
                    for i in indices:
                        panel = Image.new('RGB', (2 * size, size + header), 'white')
                        draw = ImageDraw.Draw(panel)
                        for j, (label, qpos) in enumerate((('Original z0', a), ('CEM z*', b))):
                            x = j * size
                            panel.paste(Image.fromarray(image_at(renderer, options, qpos[i])), (x, header))
                            draw.text((x + 8, 5), f'{label} | seed {job.seed}', fill='#193644', font=font)
                            draw.text((x + 8, 27), f'{job.mass:g}kg; xyz=({job.offset[0]:g},{job.offset[1]:g},{job.offset[2]:g})m', fill='#526573', font=font)
                            drift = float(np.linalg.norm(qpos[i, :2]))
                            draw.text((x + 8, 49), f't={(i + 1) * dt:.2f}s | drift={drift:.3f}m', fill='#526573', font=font)
                        writer.add_image(np.asarray(panel))
                print(f'RENDERED {job.output}', flush=True)
            if job.name not in rendered_targets:
                target_path = output / f'{job.name}_target.jpg'
                if args.overwrite or not target_path.exists():
                    target = np.asarray(tasks[job.name]['qpos'], dtype=float)
                    if target.shape != (36,) or not np.isfinite(target).all():
                        raise ValueError(f'invalid reference qpos: {job.name}')
                    Image.fromarray(image_at(renderer, options, target)).save(target_path, quality=92)
                rendered_targets.add(job.name)
            manifests.append({
                'task': job.name, 'title': job.title, 'seed': job.seed,
                'cem_failure_example': job.failure, 'output': job.output.name,
                'payload': {'mass_kg': job.mass, 'offset_m': list(job.offset)},
                'original_npz': str(job.original), 'original_sha256': sha256(job.original),
                'cem_npz': str(job.cem), 'cem_sha256': sha256(job.cem),
                'physics_xml': str(job.xml), 'physics_xml_sha256': sha256(job.xml),
                'recorded_steps': len(a), 'recorded_dt_s': dt, 'recorded_duration_s': len(a) * dt,
                'stride': args.stride, 'encoded_frames': len(indices), 'fps': fps,
                'panel_size': size, 'video_sha256': sha256(job.output),
                'encoded_duration_s': len(indices) / fps,
                'camera_world_lookat': list(args.lookat), 'camera_distance': args.distance,
                'camera_azimuth': args.azimuth, 'camera_elevation': args.elevation,
                'simple_geometry': args.simple_geometry,
                'meaning': 'Replay actual recorded qpos; same payload and seed on both sides; no policy or physics rerun; no qpos repair or interpolation.',
            })
        temporary = manifest_path.with_suffix('.json.pending')
        temporary.write_text(json.dumps({'replay_only': True, 'videos': manifests}, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(manifest_path)
    finally:
        for renderer, _ in renderers.values():
            renderer.close()


def parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('root', type=Path, help='包含 study.json、tasks.json、eval/、physics/ 的实验目录')
    p.add_argument('--output', type=Path, help='默认 <root>/videos')
    p.add_argument('--seed', type=int, default=101, help='主对照视频的共同种子，默认101')
    p.add_argument('--tasks', nargs='+', help='仅渲染指定任务 name')
    p.add_argument('--failures', action='store_true', help='额外导出 CEM success=false 的其他共同种子对照')
    p.add_argument('--stride', type=int, default=5, help='每隔多少物理帧取一帧，按 dt 保持真时间，默认5')
    p.add_argument('--size', type=int, default=360, help='每侧正方形图像边长，须为偶数，默认360')
    p.add_argument('--lookat', type=float, nargs=3, default=[0., 0., .60], help='固定世界相机目标 xyz，默认0 0 .60')
    p.add_argument('--distance', type=float, default=2.8)
    p.add_argument('--azimuth', type=float, default=130.)
    p.add_argument('--elevation', type=float, default=-16.)
    p.add_argument('--simple-geometry', action='store_true', help='只显示组0/2/3，隐藏visual组1，payload_visual单列组2')
    p.add_argument('--overwrite', action='store_true', help='重新编码已有视频和目标JPG')
    p.add_argument('--check', action='store_true', help='只检查配对文件/负载/种子/轨迹，不渲染或写文件')
    return p


def main():
    p = parser()
    args = p.parse_args()
    if args.stride < 1 or args.size < 64 or args.size % 2:
        p.error('--stride must be positive and --size must be an even integer >=64')
    if args.distance <= 0 or not all(math.isfinite(x) for x in [args.distance, args.azimuth, args.elevation, *args.lookat]):
        p.error('camera values must be finite and distance must be positive')
    run(args)


if __name__ == '__main__':
    main()
