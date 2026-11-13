"""冻结模型，批量筛选各功夫原始Goal；种子0/11，独立于最终验证。"""
import os
os.environ.setdefault('MUJOCO_GL','egl');os.environ.setdefault('OMP_NUM_THREADS','1');os.environ.setdefault('TORCH_COMPILE_DISABLE','1')
import argparse,json,time,hashlib,shutil
from pathlib import Path
import numpy as np,torch
from ufo.experiments.payload.policy import FrozenPolicy
from ufo.experiments.payload.rollout import PoseEvaluator
from ufo.experiments.payload.run import save
from ufo.inference.runtime import load_mjlab_env_cfg

def main():
 p=argparse.ArgumentParser();p.add_argument('--device',default='cuda:0');p.add_argument('--part',type=int,default=0);p.add_argument('--parts',type=int,default=2);p.add_argument('--batch',type=int,default=96);p.add_argument('--horizon',type=float,default=10);p.add_argument('--candidates',type=Path);p.add_argument('--out',type=Path);p.add_argument('--original-from',type=Path);a=p.parse_args()
 root=Path('/data/kungfu-payload-cem-20261113');candidates=json.loads((a.candidates or root/'candidates.json').read_text());candidates=[r for i,r in enumerate(candidates) if i%a.parts==a.part]
 torch.cuda.set_device(a.device);torch.set_num_threads(1);torch.set_float32_matmul_precision('highest');torch.manual_seed(0)
 run=Path('/data/UFO-next/runs/astro_fb_1024_shared_bf16_8gpu_no_backflips_20261110_183440')
 cfg,_=load_mjlab_env_cfg(run,data_path=Path('/data/model-comparison-20261111/selected_motions.pkl'),robot_config=Path('/data/UFO-next/configs/robots/astro_p2_29dof.yaml'),device=a.device,disable_dr=True,disable_obs_noise=True,max_episode_length_s=10000)
 env,_=cfg.build(num_envs=a.batch*2);policy=FrozenPolicy(run,a.device);before=policy.fingerprint();results=[];start=time.time();out=a.out or root/'broad-screen';out.mkdir(exist_ok=True);(out/'original').mkdir(exist_ok=True)
 for lo in range(0,len(candidates),a.batch):
  true_batch=candidates[lo:lo+a.batch];batch=true_batch+[true_batch[-1]]*(a.batch-len(true_batch))
  evaluator=PoseEvaluator(env,policy,batch);zs=np.stack([x['z'] for x in evaluator.targets])
  if a.original_from:zs=np.stack([np.loadtxt(a.original_from/f"{t['name']}_z.csv",delimiter=',') for t in batch]).astype(np.float32)
  scores,rows,_=evaluator.evaluate(zs,list(range(a.batch)),[0,11],a.horizon,record=False)
  batch_after=policy.fingerprint()
  assert batch_after==before
  for i,t in enumerate(true_batch):
   path=out/'original'/f"{t['name']}_z.csv"
   if a.original_from:shutil.copy2(a.original_from/path.name,path)
   else:np.savetxt(path,zs[i:i+1],delimiter=',',fmt='%.9g')
   record=dict(target=t,rows=rows[2*i:2*i+2],original_z_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),model_before=before,model_after=batch_after,horizon_s=a.horizon)
   record['screen_pass']=all(r['success'] for r in record['rows']);results.append(record)
  save(out/f'part{a.part}.json',dict(results=results,elapsed_s=time.time()-start,model_unchanged=policy.fingerprint()==before))
  print('BATCH',lo,'cases',len(true_batch),'pass',[(r['target']['name'],r['target']['source_file'],r['target']['source_time_s']) for r in results if r['screen_pass']],flush=True)
 env.close()
if __name__=='__main__':
 with torch.no_grad():main()
