"""对真实评估轨迹做固定世界相机回放；不改物理 rollout。"""
import os
os.environ.setdefault('MUJOCO_GL','egl')
os.environ.setdefault('PYOPENGL_PLATFORM','egl')
import argparse
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import mujoco
from ufo.inference.runtime import MujocoQposRenderer,video_writer


def render(root,output):
    root,output=Path(root),Path(output);output.mkdir(parents=True,exist_ok=True)
    tasks=json.loads((root/'tasks.json').read_text())[:3]
    renderer=MujocoQposRenderer(root/'physics/m8_x0.3_y0_z0.1.xml',render_size=360,camera_distance=2.8,camera_azimuth=130,camera_elevation=-16,expected_qpos_size=36)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
    def frame(q):
        renderer.data.qpos[:]=q
        mujoco.mj_forward(renderer.model,renderer.data)
        renderer.camera.lookat[:]=[0,0,.63]
        renderer.renderer.update_scene(renderer.data,camera=renderer.camera)
        return renderer.renderer.render().copy()
    for task in tasks:
        name=task['name'];a=np.load(root/'eval'/f'{name}_m8_x0.3_y0_original.npz');b=np.load(root/'eval'/f'{name}_m8_x0.3_y0_cem.npz')
        A,B=a['qpos'],b['qpos'];dt=float(a['dt']);stride=5
        with video_writer(output/f'{name}.mp4',fps=round(1/(dt*stride)),shape=(416,720)) as writer:
            for i in range(0,min(len(A),len(B)),stride):
                panel=Image.new('RGB',(720,416),'white');panel.paste(Image.fromarray(frame(A[i])),(0,55));panel.paste(Image.fromarray(frame(B[i])),(360,55))
                draw=ImageDraw.Draw(panel)
                for j,(label,Q) in enumerate([('Original z0',A),('CEM z*',B)]):
                    draw.text((10+j*360,5),f'{label} | 8kg, x=0.30m',fill='#193644',font=font)
                    drift=float(np.linalg.norm(Q[i,:2]));draw.text((10+j*360,29),f't={(i+1)*dt:4.1f}s   xy drift={drift:.3f}m',fill='#526573',font=font)
                writer.add_image(np.asarray(panel))
        Image.fromarray(frame(np.array(task['qpos']))).save(output/f'{name}_target.jpg',quality=92)
        print(name,'rendered',flush=True)
    renderer.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('output');a=p.parse_args();render(a.root,a.output)
