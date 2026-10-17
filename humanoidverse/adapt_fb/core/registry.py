"""Task registration that survives an incomplete checkout.

Adapted from ORCS ``orcs.core.registry`` (BSD-3-Clause; Lokesh Krishna).
"""

from __future__ import annotations

from typing import Callable, Iterable

__all__ = ["TaskRow", "register_all", "MISSING_DATA"]

MISSING_DATA = (FileNotFoundError, NotADirectoryError, OSError, ImportError)

TaskRow = tuple[str, Callable[..., object], Callable[[], object]]
"""(task_id, env_cfg factory taking ``play=``, rl_cfg factory taking nothing)."""


def register_all(rows: Iterable[TaskRow]) -> dict[str, str]:
    """Register each row with MJLab; return {task_id: reason} for skips."""
    from mjlab.tasks.registry import register_mjlab_task

    skipped: dict[str, str] = {}
    for task_id, env_cfg, rl_cfg in rows:
        try:
            register_mjlab_task(
                task_id=task_id,
                env_cfg=env_cfg(),
                play_env_cfg=env_cfg(play=True),
                rl_cfg=rl_cfg(),
            )
        except MISSING_DATA as e:
            skipped[task_id] = f"{type(e).__name__}: {e}"
    return skipped
