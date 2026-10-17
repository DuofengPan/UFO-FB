"""Thrown-ball entity — a free-flying sphere.

A primitive, not a mesh from the `assets` dep: a ball is fully specified by a
radius and a mass, so generating the spec is exact and a roster of ball sizes
costs nothing. That is the whole difference from `objects.py`, whose variants
exist because a suitcase cannot be written down.

Defaults are a basketball (r 0.12 m, 0.62 kg). Size is what sets both the visual
angular size at range and the collision cross-section, so it is the one knob a
perception experiment varies.
"""

from __future__ import annotations

from typing import Callable

import mujoco
from mjlab.entity import EntityCfg

__all__ = ["BALL_BODY_NAME", "BALL_GEOM_NAME", "PARKED_BALL_POS", "ball_entity_cfg"]

BALL_BODY_NAME = "ball"
BALL_GEOM_NAME = "ball_collision"

# Far lateral park when throws are disabled (``--no-ball``): same freejoint
# entity for obs/sensor consistency, but never lands on the robot at the origin.
PARKED_BALL_POS: tuple[float, float, float] = (50.0, 50.0, 5.0)

_XML = """
<mujoco model="ball">
  <asset>
    <material name="ball_mat" rgba="{r} {g} {b} 1" specular="0.3" shininess="0.4"/>
  </asset>
  <worldbody>
    <body name="{body}" pos="{spawn_x} {spawn_y} {spawn_z}">
      <freejoint/>
      <geom name="{geom}" type="sphere" size="{radius}" mass="{mass}"
            material="ball_mat" friction="0.6 0.005 0.0001"
            solref="0.01 1" solimp="0.9 0.95 0.001"/>
    </body>
  </worldbody>
</mujoco>
"""


def _spec_fn(xml: str) -> Callable[[], mujoco.MjSpec]:
    return lambda: mujoco.MjSpec.from_string(xml)


def ball_entity_cfg(
    radius: float = 0.12,
    mass: float = 0.62,
    rgb: tuple[float, float, float] = (0.85, 0.25, 0.12),
    spawn_z: float = 5.0,
    spawn_pos: tuple[float, float, float] | None = None,
) -> EntityCfg:
    """One sphere with a freejoint, parked out of the way until thrown.

    Default park is ``(0, 0, spawn_z)`` — high above the robot until ``ThrowBall``
    teleports it. Pass ``spawn_pos`` (e.g. :data:`PARKED_BALL_POS`) to keep the
    ball in-scene but far from the robot when throws are off.
    """
    if spawn_pos is None:
        spawn_pos = (0.0, 0.0, float(spawn_z))
    sx, sy, sz = (float(spawn_pos[0]), float(spawn_pos[1]), float(spawn_pos[2]))
    xml = _XML.format(
        body=BALL_BODY_NAME,
        geom=BALL_GEOM_NAME,
        radius=radius,
        mass=mass,
        r=rgb[0],
        g=rgb[1],
        b=rgb[2],
        spawn_x=sx,
        spawn_y=sy,
        spawn_z=sz,
    )
    return EntityCfg(
        spec_fn=_spec_fn(xml),
        init_state=EntityCfg.InitialStateCfg(pos=(sx, sy, sz)),
    )
