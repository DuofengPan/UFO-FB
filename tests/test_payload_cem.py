import numpy as np
from ufo.experiments.payload.cem import CEMConfig,constrain,optimize
from ufo.experiments.payload.physics import Payload,combine


def test_cem_improves_without_losing_spherical_trust_region():
    anchor=np.array([4.,0,0,0]);target=np.array([3.8,.8,.2,0])
    seen=[]
    def score(z):
        seen.extend(z.copy());return -((z-target)**2).sum(-1)
    best,h=optimize(anchor,score,CEMConfig(population=32,elites=6,iterations=12,sigma=.2,max_angle=.4))
    assert h[-1]['best_score']>h[0]['anchor_score']+.2
    np.testing.assert_allclose(np.linalg.norm(seen,axis=1),4,atol=1e-6)
    assert np.max(np.arccos(np.clip(np.asarray(seen)[:,0]/4,-1,1)))<.40001
    best2,_=optimize(anchor,score,CEMConfig(population=32,elites=6,iterations=12,sigma=.2,max_angle=.4))
    np.testing.assert_array_equal(best,best2)


def test_payload_parallel_axis_and_zero_identity():
    inertia=np.diag([1.,2,3]);com=np.zeros(3)
    m,c,I=combine(10,com,inertia,Payload(0))
    assert m==10;np.testing.assert_array_equal(I,inertia);np.testing.assert_array_equal(c,com)
    m,c,I=combine(10,com,inertia,Payload(2,offset_m=(.3,0,0),size_m=(.2,.2,.2)))
    np.testing.assert_allclose(c,[.05,0,0])
    np.testing.assert_allclose(np.diag(I)-np.diag(inertia),[2*.04/6,2*.04/6+.15,2*.04/6+.15])
    assert np.linalg.eigvalsh(I).min()>0


def test_xml_payload_preserves_contract_and_rotated_inertia(tmp_path):
    import mujoco
    from ufo.experiments.payload.physics import write_payload_xml
    source=tmp_path/'robot.xml';output=tmp_path/'loaded.xml'
    source.write_text('''<mujoco><worldbody><body name="torso"><freejoint/>
    <inertial mass="10" pos=".02 .01 -.03" quat=".9238795 0 0 .3826834" diaginertia=".1 .12 .14"/>
    <geom type="box" size=".1 .1 .1" mass="0"/></body></worldbody></mujoco>''')
    info=write_payload_xml(source,output,Payload(2,body='torso',offset_m=(.3,0,.1)))
    loaded=mujoco.MjModel.from_xml_path(str(output));original=mujoco.MjModel.from_xml_path(str(source))
    assert (loaded.nq,loaded.nv,loaded.nbody)==(original.nq,original.nv,original.nbody)
    np.testing.assert_allclose(loaded.body_mass[1],12)
    np.testing.assert_allclose(loaded.body_ipos[1],(10*np.array([.02,.01,-.03])+2*np.array([.3,0,.1]))/12)
    rot=np.zeros(9);mujoco.mju_quat2Mat(rot,loaded.body_iquat[1]);rot=rot.reshape(3,3)
    np.testing.assert_allclose(rot@np.diag(loaded.body_inertia[1])@rot.T,info['body_inertia_kgm2'],rtol=0,atol=2e-8)


def test_cem_rejects_invalid_objective():
    import pytest
    with pytest.raises(ValueError,match='finite score'):
        optimize(np.array([1.,0,0]),lambda z: np.full(len(z),np.nan),CEMConfig(population=4,elites=1,iterations=1))
