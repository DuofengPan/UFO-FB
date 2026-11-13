"""向量化闭环固定姿态评估；终止后 sticky mask，绝不重置累计分数。"""
from pathlib import Path
import numpy as np
import torch
from ufo.motion.reference import _motion_observations


class PoseEvaluator:
    def __init__(self, env, policy, tasks):
        self.env,self.core,self.policy,self.tasks=env,env._env,policy,tasks
        self.device=self.core.device
        self.dt=float(self.core.dt)
        self.body_names=list(self.core.body_names[:self.core.num_bodies])
        self.feet=[self.body_names.index(x+'_ankle_roll_link') for x in ('left','right')]
        self.key=[self.body_names.index(n) for n in ('waist_roll_link','left_ankle_roll_link','right_ankle_roll_link','left_wrist_yaw_link','right_wrist_yaw_link')]
        self.targets=[]
        # Canonical goal observations use the native reference preprocessing.
        for task in tasks:
            q=torch.tensor(task['dof_pos'],device=self.device,dtype=torch.float32)
            roots=torch.zeros((env.num_envs,13),device=self.device);roots[:,2]=task['qpos'][2];roots[:,:3]+=self.core.env_origins;roots[:,6]=1
            dofs=torch.zeros((env.num_envs,len(q),2),device=self.device);dofs[:,:,0]=q
            self.core.reset_all(target_states={'root_states':roots,'dof_states':dofs})
            c=self.core
            body=c.body_pos[:1].clone()-c.env_origins[:1,None]
            rot=c.body_rot[:1].clone()
            state={'rg_pos_t':body,'rg_rot_t':rot,'body_vel_t':torch.zeros_like(body),
                   'body_ang_vel_t':torch.zeros_like(body),'dof_vel':torch.zeros_like(q[None])}
            filtered,priv=_motion_observations(c,state,q[None]-c.default_dof_pos[:1],root_height_obs=bool(c.config.obs.root_height_obs),use_obs_filter=True)
            goal={'state':filtered,'privileged_state':priv,'last_action':torch.zeros_like(q[None])}
            z=policy.goal_inference(goal)[0].cpu().numpy()
            self.targets.append(dict(q=q, body=body[0], height=roots[0,2].clone(), z=z))

    @torch.no_grad()
    def evaluate(self, zs, task_id, seeds, horizon_s, record=False):
        """每个候选与相同种子交叉配对；重置含 Actor 历史/last action。"""
        c=self.core;device=self.device;N=c.num_envs
        zs=np.asarray(zs,dtype=np.float32).reshape(-1,256)
        if len(zs)*len(seeds) != N: raise ValueError('candidate x seed must equal env count')
        z=torch.tensor(np.repeat(zs,len(seeds),axis=0),device=device)
        roots=torch.zeros((N,13),device=device);roots[:,2]=.645;roots[:,:3]+=c.env_origins;roots[:,6]=1
        dofs=torch.zeros((N,c.num_dof,2),device=device);dofs[:,:,0]=c.default_dof_pos
        for k,seed in enumerate(seeds):
            if seed:
                gen=torch.Generator(device=device).manual_seed(seed)
                perturb=.015*torch.randn((c.num_dof,),device=device,generator=gen)
                dofs[k::len(seeds),:,0]+=perturb
        c.reset_all(target_states={'root_states':roots,'dof_states':dofs});c.is_evaluating=True
        obs=c.get_observation(to_numpy=False,include_last_action=self.env.include_last_action,include_history_actor=self.env.include_history_actor)
        target=self.targets[task_id];q=target['q'];target_body=target['body'];height=target['height']
        alive=torch.ones(N,device=device,dtype=torch.bool)
        steps=round(horizon_s/self.dt);warmup=round(2/self.dt)
        sums={k:torch.zeros(N,device=device) for k in ('cost','joint','height','body','speed','tilt','slip','torque','smooth','semantic','count','bad_contact')}
        survival=torch.zeros(N,device=device);max_drift=torch.zeros(N,device=device)
        previous=torch.zeros((N,c.num_dof),device=device)
        history=[]
        for t in range(steps):
            action=self.policy.act(obs,z,mean=True)
            _,_,term,info=c.step(action)
            obs=c.get_observation(to_numpy=False,include_last_action=self.env.include_last_action,include_history_actor=self.env.include_history_actor)
            position=c.robot_root_states[:,:3]-c.env_origins
            drift=position[:,:2].norm(dim=-1)
            tilt=torch.acos((-c.projected_gravity[:,2]).clamp(-1,1))
            finite=torch.isfinite(position).all(-1)&torch.isfinite(c.dof_pos).all(-1)&torch.isfinite(action).all(-1)
            alive &= finite & ~term.bool() & (position[:,2]>.28) & (tilt<1.05)
            survival+=alive*self.dt
            max_drift=torch.maximum(max_drift,torch.where(alive,drift,torch.zeros_like(drift)))
            joint=(c.dof_pos-q).abs().mean(-1)
            he=(position[:,2]-height).abs()
            # Heading-local body geometry; independent of absolute xy/yaw.
            from ufo.math import quat_rotate_inverse
            current_rel=c.body_pos-c.body_pos[:,:1]
            rootq=c.base_quat[:,None].expand(-1,c.num_bodies,-1)
            local=quat_rotate_inverse(rootq.reshape(-1,4),current_rel.reshape(-1,3),w_last=True).reshape(N,c.num_bodies,3)
            target_rel=target_body-target_body[:1]
            be=(local[:,self.key]-target_rel[self.key]).norm(dim=-1).mean(-1)
            speed=c.robot_root_states[:,7:9].norm(dim=-1)
            contact=c.contact_forces[:,self.feet].norm(dim=-1)>5
            slip=(c.body_vel[:,self.feet,:2].norm(dim=-1)*contact).sum(-1)
            torque=(c.torques.abs()/c.torque_limits).clamp(0,2)
            saturation=(torque>.95).float().mean(-1)
            smooth=(action-previous).square().mean(-1);previous=action.clone()
            undesired=(c.contact_forces[:,[j for j in range(c.num_bodies) if j not in self.feet]].norm(dim=-1)>10).any(-1)
            if self.tasks[task_id]['support']=='both':
                support_ok=contact.all(-1)
            else:
                support=0 if self.tasks[task_id]['support']=='left' else 1
                lift=1-support
                lift_height=(c.body_pos[:,self.feet[lift],2]-c.body_pos[:,self.feet[support],2])
                support_ok=contact[:,support]&~contact[:,lift]&(lift_height>.07)
            semantic=alive&(joint<.18)&(he<.07)&(be<.10)&(drift<.15)&(tilt<.35)&support_ok&~undesired
            # Dimensionless costs; terminal cost sticky and full-horizon.
            cost=2*(joint/.18).square()+1.5*(he/.07).square()+1.5*(be/.10).square()+(.5*(drift/.15).square())+(.3*(speed/.1).square())+.2*(tilt/.35).square()+.1*(slip/.1).square()+.2*saturation+.02*smooth+2*(~support_ok).float()+3*undesired.float()
            cost=torch.nan_to_num(cost,nan=100.,posinf=100.,neginf=100.).clamp(max=100)
            sums['cost']+=torch.where(alive,cost,torch.full_like(cost,100))
            if t>=warmup:
                for key,value in dict(joint=joint,height=he,body=be,speed=speed,tilt=tilt,slip=slip,torque=saturation,smooth=smooth,semantic=semantic.float(),bad_contact=undesired.float()).items():
                    sums[key]+=torch.nan_to_num(value)*alive
                sums['count']+=alive
            if record:
                qp=self.env._get_qpos_qvel(to_numpy=False)[0].clone();qp[:,:3]-=c.env_origins
                history.append(qp.cpu().numpy())
        count=sums['count'].clamp(min=1)
        rows=[]
        for i in range(N):
            rows.append(dict(seed=int(seeds[i%len(seeds)]),score=float(-sums['cost'][i]/steps),
                             survival_s=float(survival[i]),max_drift_m=float(max_drift[i]),
                             joint_mae_rad=float(sums['joint'][i]/count[i]),height_error_m=float(sums['height'][i]/count[i]),
                             key_body_error_m=float(sums['body'][i]/count[i]),speed_mps=float(sums['speed'][i]/count[i]),
                             tilt_deg=float(sums['tilt'][i]/count[i]*180/np.pi),slip_mps=float(sums['slip'][i]/count[i]),
                             torque_saturation_fraction=float(sums['torque'][i]/count[i]),
                             action_delta_mse=float(sums['smooth'][i]/count[i]),
                             undesired_contact_fraction=float(sums['bad_contact'][i]/count[i]),
                             hold_fraction=float(sums['semantic'][i]/max(1,steps-warmup)),
                             success=bool(alive[i] and sums['semantic'][i]/max(1,steps-warmup)>.9)))
        scores=np.array([r['score'] for r in rows]).reshape(len(zs),len(seeds)).mean(-1)
        return scores,rows,np.asarray(history) if record else None
