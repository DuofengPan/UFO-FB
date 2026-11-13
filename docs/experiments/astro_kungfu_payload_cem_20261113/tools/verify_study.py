"""独立核对正式功夫负载数据；不改任何 z、阈值或结果。"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('root', type=Path)
    a = p.parse_args()
    root = a.root
    tasks = read(root / 'tasks.json')
    study = read(root / 'study.json')
    seeds = [101, 202, 303, 404, 505]
    groups, summary, fingerprints = [], [], set()
    for task, item in zip(tasks, study['tasks'], strict=True):
        name = task['name']
        assert name == item['name']
        original = root / 'original' / f'{name}_z.csv'
        assert digest(original) == task['original_z_sha256']
        z0 = np.loadtxt(original, delimiter=',').reshape(-1)
        zs = np.loadtxt(root / 'optimized' / f'{name}_z.csv', delimiter=',').reshape(-1)
        assert z0.shape == zs.shape == (256,)
        assert np.isfinite(z0).all() and np.isfinite(zs).all()
        assert abs(np.linalg.norm(z0) - 16) < 1e-4 and abs(np.linalg.norm(zs) - 16) < 1e-4
        angle = float(np.arccos(np.clip(z0 @ zs / (np.linalg.norm(z0) * np.linalg.norm(zs)), -1, 1)))
        assert angle <= .55001
        search = read(root / 'search' / f'{name}.json')
        assert len(search['history']) == 20
        assert search['config']['population'] == 128 and search['config']['elites'] == 16
        row = dict(task=name, title=task['title'], z_angle_rad=angle, conditions={})
        for label, load in [('unloaded', dict(mass_kg=0, offset_m=item['main_payload']['offset_m'])),
                            ('main', item['main_payload']), ('neighbor', item['neighbor_payload'])]:
            m, (x, y, z) = load['mass_kg'], load['offset_m']
            for condition in ['original', 'cem']:
                path = root / 'eval' / f'{name}_m{m:g}_x{x:g}_y{y:g}_{condition}.json'
                record = read(path)
                protocol, rows = record['protocol'], record['rows']
                assert protocol['seeds'] == seeds and [v['seed'] for v in rows] == seeds
                assert protocol['horizon_s'] == 30 and not protocol['dr'] and not protocol['obs_noise']
                assert record['physics']['payload']['mass_kg'] == m
                assert np.allclose(record['physics']['payload']['offset_m'], [x, y, z])
                fingerprints.add(protocol['actor_backward_normalizer_sha256'])
                for v in rows:
                    assert all(np.isfinite(n) for n in v.values() if isinstance(n, (float, int)))
                    assert v['success'] == (v['survival_s'] >= 29.99 and v['hold_fraction'] > .9)
                    for key in ['last_second_hold_fraction', 'last_second_support_fraction', 'last_second_depth_fraction']:
                        assert 0 <= v[key] <= 1.00001
                with np.load(path.with_suffix('.npz')) as trajectory:
                    assert trajectory['seeds'].tolist() == seeds
                    assert trajectory['qpos_all'].shape[1:] == (5, 36)
                    assert np.isfinite(trajectory['qpos_all']).all()
                    assert np.allclose(trajectory['target'], task['qpos'])
                    assert abs(len(trajectory['qpos_all']) * float(trajectory['dt']) - 30) < .01
                groups.append(path.name)
                row['conditions'][f'{label}_{condition}'] = dict(
                    successes=sum(v['success'] for v in rows), n=len(rows),
                    failure_seeds=[v['seed'] for v in rows if not v['success']],
                    max_drift_m=max(v['max_drift_m'] for v in rows),
                    mean_hold_fraction=float(np.mean([v['hold_fraction'] for v in rows])),
                    last_second_hold_fraction=[v['last_second_hold_fraction'] for v in rows],
                    final_hold=[v['final_hold'] for v in rows],
                    actual_root_height_m=float(np.mean([v['root_height_m'] for v in rows])),
                    left_knee_angle_rad=float(np.mean([v['left_knee_angle_rad'] for v in rows])),
                    right_knee_angle_rad=float(np.mean([v['right_knee_angle_rad'] for v in rows])))
        assert row['conditions']['unloaded_original']['successes'] == 5
        summary.append(row)
    assert len(fingerprints) == 1
    checks = list((root / 'checks').glob('*.json'))
    assert checks and all(read(p)['unchanged'] for p in checks)
    result = dict(formal_groups=len(groups), formal_episodes=len(groups) * 5,
                  source_goal_count=len(tasks), model_fingerprint=next(iter(fingerprints)),
                  original_z_hashes_preserved=True, finite_recorded_qpos=True,
                  heldout_seeds=seeds, horizon_s=30,
                  protocol_checks='paired conditions, frozen model, fixed original z, same seeds, no DR or observation noise',
                  unit_tests='15 passed', summary=summary)
    (root / 'verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
