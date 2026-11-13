"""python -m ufo.experiments.payload.run --help"""
import os
os.environ.setdefault('MUJOCO_GL','egl')
os.environ.setdefault('PYOPENGL_PLATFORM','egl')
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('TORCH_COMPILE_DISABLE','1')
import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import torch
from .cem import CEMConfig, optimize
from .physics import Payload,write_payload_xml
from .tasks import make_tasks
from .policy import FrozenPolicy
from .rollout import PoseEvaluator
from ufo.inference.runtime import load_mjlab_env_cfg


def save(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.pending');tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False));tmp.replace(path)


def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def main():
    p=argparse.ArgumentParser(description='固定姿态、冻结 UFO、球面局部 CEM 负载适应')
    p.add_argument('--run',required=True,type=Path);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--robot',default='configs/robots/astro_p2_29dof.yaml',type=Path)
    p.add_argument('--data',required=True,type=Path);p.add_argument('--device',default='cuda:0')
    p.add_argument('--mass',type=float,default=2);p.add_argument('--offset',type=float,nargs=3,default=[0,0,.1])
    p.add_argument('--task',type=int,nargs='+',default=[0,1,2])
    p.add_argument('--phase',choices=['baseline','search','validate'],required=True)
    p.add_argument('--population',type=int,default=128);p.add_argument('--elites',type=int,default=16)
    p.add_argument('--iterations',type=int,default=20);p.add_argument('--horizon',type=float,default=None)
    p.add_argument('--seeds',type=int,nargs='+',default=None)
    p.add_argument('--sigma',type=float,default=.18);p.add_argument('--max-angle',type=float,default=.55)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    torch.cuda.set_device(a.device);torch.set_num_threads(1);torch.set_float32_matmul_precision('highest');torch.manual_seed(0);np.random.seed(0)
    seeds=a.seeds or ([0,11] if a.phase=='search' else [101,202,303,404,505])
    horizon=a.horizon or (10 if a.phase=='search' else 30)
    count=(a.population if a.phase=='search' else 2 if a.phase=='validate' else 1)*len(seeds)
    cfg,spec=load_mjlab_env_cfg(a.run,data_path=a.data,robot_config=a.robot,device=a.device,disable_dr=True,disable_obs_noise=True,max_episode_length_s=10000)
    original_xml=Path(cfg.mjcf_path)
    xml=a.out/f'physics/m{a.mass:g}_x{a.offset[0]:g}_y{a.offset[1]:g}_z{a.offset[2]:g}.xml'
    physics=write_payload_xml(original_xml,xml,Payload(a.mass,offset_m=tuple(a.offset)))
    cfg=cfg.model_copy(update={'mjcf_path':str(xml.resolve()),'seed':0})
    print('BUILD',count,a.phase,a.mass,flush=True)
    env,_=cfg.build(num_envs=count)
    c=env._env
    tasks=make_tasks(original_xml,list(c.dof_names),c.default_dof_pos[0].cpu().numpy())
    policy=FrozenPolicy(a.run,a.device);before=policy.fingerprint()
    evaluator=PoseEvaluator(env,policy,tasks)
    # The original files are write-once and checked on every subsequent invocation.
    for i,task in enumerate(tasks):
        path=a.out/'original'/f"{task['name']}_z.csv"
        path.parent.mkdir(exist_ok=True)
        z=evaluator.targets[i]['z']
        if path.exists():
            canonical=np.loadtxt(path,delimiter=',').astype(np.float32)
            if (a.out/'tasks.json').exists():
                saved=json.loads((a.out/'tasks.json').read_text())[i]
                if digest(path)!=saved['original_z_sha256']: raise AssertionError('original z file changed')
                np.testing.assert_allclose(task['qpos'],saved['qpos'],rtol=0,atol=1e-7)
            evaluator.targets[i]['z']=canonical
        else:
            np.savetxt(path,z[None],delimiter=',',fmt='%.9g')
        task['original_z_sha256']=digest(path)
    if not (a.out/'tasks.json').exists():save(a.out/'tasks.json',tasks)
    tag=f'm{a.mass:g}_x{a.offset[0]:g}_y{a.offset[1]:g}'
    protocol=dict(run=str(a.run.resolve()),robot=str(a.robot.resolve()),data=str(a.data.resolve()),
                  actor_backward_normalizer_sha256=before,checkpoint_sha256=digest(a.run/'checkpoint/model/model.safetensors'),
                  robot_xml_sha256=digest(original_xml),physics=physics,seeds=seeds,horizon_s=horizon,
                  dt=evaluator.dt,actor_precision='FP32 eager, deterministic mean actions',dr=False,obs_noise=False,
                  entry='YAML neutral standing z=.645; zero velocities; heldout Gaussian joint perturbation std .015 rad; fresh action/history',
                  termination='sticky death: simulator termination, nonfinite state/action, root<.28m, tilt>60deg; no automatic reset',
                  metrics='hold evaluated after 2s; full-horizon denominator; alive-only pose MAE; semantic success requires >90% hold and full survival')
    save(a.out/'protocol'/f'{a.phase}_{tag}_gpu{a.device[-1]}.json',protocol)
    started=time.time()
    for task_id in a.task:
        task_started=time.time()
        task=tasks[task_id];name=task['name'];anchor=np.loadtxt(a.out/'original'/f'{name}_z.csv',delimiter=',').astype(np.float32)
        if a.phase=='search':
            config=CEMConfig(population=a.population,elites=a.elites,iterations=a.iterations,sigma=a.sigma,max_angle=a.max_angle,seed=20261113+task_id)
            def objective(z):return evaluator.evaluate(z,task_id,seeds,horizon)[0]
            def callback(z,hist):
                dest=a.out/'optimized'/f'{name}_z.csv';dest.parent.mkdir(exist_ok=True)
                np.savetxt(dest,z[None],delimiter=',',fmt='%.9g')
                save(a.out/'search'/f'{name}.json',dict(config=asdict(config),physics=physics,history=hist,elapsed_s=time.time()-task_started))
                print(name,hist[-1],flush=True)
            optimize(anchor,objective,config,callback)
        else:
            zs=[anchor];labels=['original']
            if a.phase=='validate':
                zs.append(np.loadtxt(a.out/'optimized'/f'{name}_z.csv',delimiter=',').astype(np.float32));labels.append('cem')
            scores,rows,traj=evaluator.evaluate(zs,task_id,seeds,horizon,record=True)
            for i,label in enumerate(labels):
                dest=a.out/'eval'/f'{name}_{tag}_{label}'
                save(Path(str(dest)+'.json'),dict(task=name,title=task['title'],condition=label,physics=physics,protocol=protocol,
                                                   rows=rows[i*len(seeds):(i+1)*len(seeds)],elapsed_s=time.time()-started))
                dest.parent.mkdir(exist_ok=True)
                # Only seed101 has a movie; all seeds retain full scalar results.
                np.savez_compressed(str(dest)+'.npz',qpos=traj[:,i*len(seeds)],target=np.array(task['qpos']),dt=evaluator.dt)
            print(name,[(l,float(s)) for l,s in zip(labels,scores)],flush=True)
    after=policy.fingerprint()
    if before!=after:raise AssertionError('model or normalizer changed')
    save(a.out/'checks'/f'{a.phase}_{tag}_gpu{a.device[-1]}_{"_".join(map(str,a.task))}.json',dict(model_before=before,model_after=after,unchanged=True,elapsed_s=time.time()-started))
    env.close()

if __name__=='__main__':main()
