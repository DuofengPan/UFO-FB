"""六个显式固定目标。只构造 Goal，不修改任何训练 motion 的速度或帧。"""
import numpy as np

TITLES = ['双脚自然站立', '双脚双臂前举', '浅蹲保持', '中蹲保持', '左脚支撑右脚抬起', '右脚支撑左脚抬起']
NAMES = ['stand', 'arms_forward', 'shallow_squat', 'medium_squat', 'left_support', 'right_support']


def make_tasks(xml, joint_names, default):
    import mujoco
    model = mujoco.MjModel.from_xml_path(str(xml))
    data = mujoco.MjData(model)
    jid = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, n) for n in joint_names]
    addresses = model.jnt_qposadr[jid]
    feet = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, s+'_ankle_roll_link') for s in ('left','right')]
    out = []
    for i, (name, title) in enumerate(zip(NAMES,TITLES)):
        q = np.array(default, dtype=float).copy()
        def setq(n,v): q[joint_names.index(n)] = v
        if i == 1:
            for side in ('left','right'):
                setq(side+'_shoulder_pitch_joint', -1.)
                setq(side+'_elbow_joint', .25)
        if i in (2,3):
            hip,knee,ankle = (-.50,1.05,-.55) if i==2 else (-.70,1.45,-.75)
            for side in ('left','right'):
                for n,v in [('hip_pitch',hip),('knee',knee),('ankle_pitch',ankle)]:
                    setq(side+'_'+n+'_joint',v)
        if i in (4,5):
            lift = 'right' if i==4 else 'left'
            for n,v in [('hip_pitch',-.9),('knee',1.7),('ankle_pitch',-.8)]:
                setq(lift+'_'+n+'_joint',v)
        mujoco.mj_resetData(model,data)
        data.qpos[:7] = [0,0,.645,1,0,0,0]
        data.qpos[addresses] = q
        mujoco.mj_forward(model,data)
        bottom = []
        for g in range(model.ngeom):
            if model.geom_bodyid[g] not in feet or not (model.geom_contype[g] or model.geom_conaffinity[g]): continue
            rot = data.geom_xmat[g].reshape(3,3)
            typ = int(model.geom_type[g]); size=model.geom_size[g]
            if typ == int(mujoco.mjtGeom.mjGEOM_BOX): extent=np.abs(rot[2]) @ size
            elif typ in (int(mujoco.mjtGeom.mjGEOM_CAPSULE),int(mujoco.mjtGeom.mjGEOM_CYLINDER)):
                extent=abs(rot[2,2])*size[1]+size[0]
            else: extent=size[0]
            bottom.append(data.geom_xpos[g,2]-extent)
        if not bottom: raise ValueError('no foot collision geometry')
        data.qpos[2] += .002 - min(bottom)
        mujoco.mj_forward(model,data)
        out.append(dict(name=name,title=title,dof_pos=q.tolist(),qpos=data.qpos.tolist(),
                        support='left' if i==4 else 'right' if i==5 else 'both',
                        construction='explicit fixed pose, FK floor alignment; no motion edits'))
    return out
