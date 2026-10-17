"""AdaptFb: ORCS-style LoRA adaptation of a frozen UFO-FB policy.

Lives inside the UFO repo as ``humanoidverse.adapt_fb`` so play/train can use
the same MJLab env, checkpoints, and goal ``z`` pickle as UFO itself.

Does **not** alter UFO's default train / goal_inference / tracking paths.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
