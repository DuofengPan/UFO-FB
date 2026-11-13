"""按支撑与深蹲类别独立配额筛原始功夫姿态；固定Goal不要求源序列低速。"""
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import hashlib,json,pickle
import numpy as np
import mujoco
from scipy.spatial import ConvexHull
from scipy.spatial.transform import Rotation
ROOT=Path('/data/kungfu-payload-cem-20261113');ROOT.mkdir(exist_ok=True)
SOURCE=Path('/data/astro-payload-cem-20261113/kungfu-source')
XML=Path('/data/UFO-next/ufo/data/robots/astro_p2/mjcf/astro_p2_29dof_simplify_primitive_collision.xml')
m=mujoco.MjModel.from_xml_path(str(XML));d=mujoco.MjData(m)
feet=[m.body(s+'_ankle_roll_link').id for s in ('left','right')]
geoms=[[i for i in range(m.ngeom) if m.geom_bodyid[i]==b and (m.geom_contype[i] or m.geom_conaffinity[i])] for b in feet]
corners=np.array([[x,y,z] for x in [-1,1] for y in [-1,1] for z in [-1,1]])

def geometry(raw,i):
 d.qpos[:3]=raw['root_pos'][i];d.qpos[3:7]=np.roll(raw['root_rot'][i],1);d.qpos[7:]=raw['dof_pos'][i];mujoco.mj_forward(m,d)
 polygons=[];bottom=[]
 for gs in geoms:
  vertices=[]
  for g in gs:
   R=d.geom_xmat[g].reshape(3,3);p=d.geom_xpos[g];s=m.geom_size[g]
   if m.geom_type[g]==mujoco.mjtGeom.mjGEOM_CAPSULE:
    for sign in [-1,1]:vertices.extend(p+sign*s[1]*R[:,2]+corners*s[0])
   elif m.geom_type[g]==mujoco.mjtGeom.mjGEOM_BOX:vertices.extend((corners*s)@R.T+p)
  v=np.asarray(vertices);bottom.append(float(v[:,2].min()));polygons.append(v[:,:2])
 gap=abs(bottom[0]-bottom[1]);support='both' if gap<.025 else ('left' if bottom[0]<bottom[1] else 'right')
 use=[0,1] if support=='both' else [0 if support=='left' else 1]
 hull=ConvexHull(np.concatenate([polygons[j] for j in use]));com=(d.xipos*m.body_mass[:,None]).sum(0)/m.body_mass.sum()
 margin=float(-(hull.equations[:,:2]@com[:2]+hull.equations[:,2]).max())
 qpos=d.qpos.copy();qpos[2]+=.002-min(bottom)
 rot=Rotation.from_quat(qpos[[4,5,6,3]]);yaw=rot.as_euler('xyz')[2];rot=Rotation.from_euler('z',-yaw)*rot;qpos[3:7]=rot.as_quat()[[3,0,1,2]];qpos[:2]=0
 return qpos,support,gap,margin

inventory=[];all_rows=[]
for p in sorted(SOURCE.glob('*.pkl')):
 raw=pickle.load(p.open('rb'));fps=float(raw['fps']);q=np.asarray(raw['dof_pos'],float);n=len(q);sha=hashlib.sha256(p.read_bytes()).hexdigest()
 tilt=np.degrees(np.arccos(np.clip(Rotation.from_quat(raw['root_rot']).as_matrix()[:,2,2],-1,1)))
 dq=np.gradient(q,1/fps,axis=0);speed=np.mean(np.abs(dq),axis=1)
 rows=[]
 for i in range(1,n-1,max(1,round(fps/6))):
  if tilt[i]>22:continue
  qp,support,gap,margin=geometry(raw,i);knees=q[i,[3,9]]
  if margin<-.005:continue
  category=None
  if support in ('left','right') and gap>.08 and .43<qp[2]<.75:category='single_'+support
  elif support=='both' and .34<qp[2]<=.50 and min(knees)>=1. and knees.mean()>=1.2 and abs(knees[0]-knees[1])<=.6:category='deep_squat'
  if not category:continue
  r=dict(category=category,support=support,source_file=p.name,source_frame=i,source_fps=fps,source_time_s=i/fps,source_sha256=sha,
         qpos=qp.tolist(),dof_pos=qp[7:].tolist(),source_root_height_m=float(qp[2]),source_knee_angles_rad=knees.tolist(),
         source_sole_gap_m=gap,source_support_margin_m=margin,source_tilt_deg=float(tilt[i]),source_joint_speed_rad_s=float(speed[i]),
         score=float(.06*min(speed[i],5)-4*margin+.05*np.abs(q[i,15:]).mean()))
  if category=='deep_squat':r.update(max_root_height_m=.50,min_mean_knee_angle_rad=1.05)
  rows.append(r)
 # 类别独立配额，每个源/类别最多8项，去除近似姿态；不被双脚站立占位。
 selected=[]
 for category in ('single_left','single_right','deep_squat'):
  pool=sorted([r for r in rows if r['category']==category],key=lambda r:r['score']);chosen=[]
  for r in pool:
   if all(np.mean(np.abs(np.array(r['dof_pos'])-np.array(v['dof_pos'])))>.055 for v in chosen):chosen.append(r)
   if len(chosen)>=8:break
  selected.extend(chosen)
 all_rows.extend(selected);inventory.append(dict(file=p.name,sha256=sha,frames=n,fps=fps,feasible=len(rows),selected=len(selected)))
 print(p.stem,len(rows),len(selected),flush=True)
# 平衡各类别和源，最多每类192；使用明确类别名，不把宽弓步自动叫深蹲。
selected=[]
for category in ('single_left','single_right','deep_squat'):
 pool=[r for r in all_rows if r['category']==category]
 for r in sorted(pool,key=lambda r:r['score'])[:192]:selected.append(r)
for i,r in enumerate(selected):
 r['name']=f"kf_{i:04d}_{r['category']}";r['title']=f"{r['source_file'].split('_Skeleton')[0]} {r['source_time_s']:.2f}s · {r['category']}"
(ROOT/'candidates.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2))
(ROOT/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
print('TOTAL',len(selected),{c:sum(r['category']==c for r in selected) for c in ('single_left','single_right','deep_squat')},flush=True)
