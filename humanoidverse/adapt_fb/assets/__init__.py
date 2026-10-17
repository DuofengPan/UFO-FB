"""Robot / object entity configs used by tasks."""

from humanoidverse.adapt_fb.assets.ball import BALL_BODY_NAME, BALL_GEOM_NAME, ball_entity_cfg
from humanoidverse.adapt_fb.assets.g1_ufo import get_ufo_aligned_g1_robot_cfg, ufo_action_scales

__all__ = [
    "BALL_BODY_NAME",
    "BALL_GEOM_NAME",
    "ball_entity_cfg",
    "get_ufo_aligned_g1_robot_cfg",
    "ufo_action_scales",
]
