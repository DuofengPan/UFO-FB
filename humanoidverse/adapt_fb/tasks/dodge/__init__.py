"""Dodge task package (AdaptFb).

Task id (reserved for MJLab discovery once RslRl agent cfg is wired)::

  UfoFbAdapt-Dodge-AdaptFb

Phase 4 delivers ``dodge_env_cfg`` + ``train_smoke``. Full ``register_mjlab_task``
waits on a real on-policy runner cfg (dict stubs are not accepted by MJLab).
"""

from __future__ import annotations

TASK_ID = "UfoFbAdapt-Dodge-AdaptFb"

SKIP_REASON: dict[str, str] = {
    TASK_ID: (
        "Full mjlab.register_mjlab_task pending; train via "
        "`python -m humanoidverse.adapt_fb.train` (OnPolicyRunner + FbWithAdapterModel)."
    ),
}
