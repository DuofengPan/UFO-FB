"""MJLab task-discovery entry point for UFO-FB-adapt."""

from __future__ import annotations

from humanoidverse.adapt_fb.core.vendor_paths import ensure_vendored_rsl_rl

ensure_vendored_rsl_rl()

import humanoidverse.adapt_fb.tasks.dodge as _dodge

SKIP_REASON: dict[str, str] = {
    **_dodge.SKIP_REASON,
}
"""{task_id: why it could not fully register}."""

MULTI_CLIP_CFGS: tuple = ()
