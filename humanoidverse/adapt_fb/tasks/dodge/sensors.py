"""Dodge contact sensors — adapted from ORCS ``orcs.tasks.dodge.sensors``."""

from __future__ import annotations

from mjlab.sensor import ContactSensorCfg
from mjlab.sensor.contact_sensor import ContactMatch

from humanoidverse.adapt_fb.assets import BALL_BODY_NAME
from humanoidverse.adapt_fb.core.sensors import (
    GROUND_CONTACT_SENSOR_NAME,
    ROOT_KILL_BODIES,
    ground_contact_sensor,
)

__all__ = [
    "BALL_CONTACT_SENSOR_NAME",
    "DODGE_KILL_BODIES",
    "GROUND_CONTACT_SENSOR_NAME",
    "ball_contact_sensor",
    "ground_contact_sensor",
]

BALL_CONTACT_SENSOR_NAME = "ball_contact"
DODGE_KILL_BODIES = ROOT_KILL_BODIES
_EVERY_COLLISION_GEOM = (".*_collision",)


def ball_contact_sensor(
    exclude: tuple[str, ...] = (), name: str = BALL_CONTACT_SENSOR_NAME
) -> ContactSensorCfg:
    return ContactSensorCfg(
        name=name,
        primary=ContactMatch(
            mode="geom",
            pattern=_EVERY_COLLISION_GEOM,
            exclude=exclude or None,
            entity="robot",
        ),
        secondary=ContactMatch(mode="body", pattern=BALL_BODY_NAME, entity=BALL_BODY_NAME),
        fields=("found",),
    )
