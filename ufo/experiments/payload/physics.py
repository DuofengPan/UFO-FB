"""刚性安装负载的组合质量、质心和惯量；不改变关节及观测维度。"""
from dataclasses import dataclass, asdict
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np


@dataclass(frozen=True)
class Payload:
    mass_kg: float = 2.
    body: str = 'waist_roll_link'
    offset_m: tuple = (0., 0., .10)
    size_m: tuple = (.16, .12, .12)


def combine(mass, com, inertia, payload):
    if payload.mass_kg < 0 or min(payload.size_m) <= 0 or mass <= 0:
        raise ValueError('invalid rigid body mass or size')
    p = np.asarray(payload.offset_m, dtype=float)
    c = np.asarray(com, dtype=float)
    m = payload.mass_kg
    total = mass + m
    center = (mass*c + m*p) / total
    size = np.asarray(payload.size_m)
    box = np.diag(m/12 * (np.sum(size**2) - size**2))
    def shift(v):
        return np.dot(v,v)*np.eye(3) - np.outer(v,v)
    result = np.asarray(inertia) + mass*shift(c-center) + box + m*shift(p-center)
    return total, center, result


def write_payload_xml(source, output, payload):
    import mujoco
    source, output = Path(source).resolve(), Path(output).resolve()
    model = mujoco.MjModel.from_xml_path(str(source))
    idx = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, payload.body)
    if idx < 1:
        raise ValueError(f'body missing: {payload.body}')
    rotation = np.zeros(9)
    mujoco.mju_quat2Mat(rotation, model.body_iquat[idx])
    rotation = rotation.reshape(3,3)
    inertia = rotation @ np.diag(model.body_inertia[idx]) @ rotation.T
    mass, com, tensor = combine(float(model.body_mass[idx]), model.body_ipos[idx], inertia, payload)
    tree = ET.parse(source)
    root = tree.getroot()
    compiler = root.find('compiler')
    if compiler is not None:
        for attr in ('meshdir', 'texturedir'):
            if compiler.get(attr):
                compiler.set(attr, str((source.parent / compiler.get(attr)).resolve()))
    body = root.find(f".//body[@name='{payload.body}']")
    inertial = body.find('inertial')
    if inertial is None:
        inertial = ET.SubElement(body, 'inertial')
    inertial.attrib.clear()
    fmt = lambda x: ' '.join(format(float(v), '.17g') for v in np.asarray(x).reshape(-1))
    inertial.set('mass', fmt([mass]))
    inertial.set('pos', fmt(com))
    inertial.set('fullinertia', fmt([tensor[0,0],tensor[1,1],tensor[2,2],tensor[0,1],tensor[0,2],tensor[1,2]]))
    if payload.mass_kg:
        ET.SubElement(body, 'geom', name='payload_visual', type='box', pos=fmt(payload.offset_m),
                      size=fmt(np.asarray(payload.size_m)/2), mass='0', contype='0', conaffinity='0',
                      group='1', rgba='.95 .45 .12 .8')
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding='unicode')
    changed = mujoco.MjModel.from_xml_path(str(output))
    if (model.nq, model.nv, model.nbody, model.nu) != (changed.nq, changed.nv, changed.nbody, changed.nu):
        raise AssertionError('payload changed robot state contract')
    np.testing.assert_allclose(changed.body_mass.sum()-model.body_mass.sum(), payload.mass_kg, atol=1e-8)
    return dict(payload=asdict(payload), total_robot_mass_kg=float(changed.body_mass.sum()),
                body_mass_kg=mass, body_com_m=com.tolist(), body_inertia_kgm2=tensor.tolist(), xml=str(output))
