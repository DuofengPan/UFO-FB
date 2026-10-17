"""Put vendored dependencies on ``sys.path`` (no pip install required for imports)."""

from __future__ import annotations

import sys
from pathlib import Path

# humanoidverse/adapt_fb/_vendor/rsl_rl
_ADAPT_FB_ROOT = Path(__file__).resolve().parents[1]
_RSL_RL_ROOT = _ADAPT_FB_ROOT / "_vendor" / "rsl_rl"


def ensure_vendored_rsl_rl() -> Path:
    """Ensure ``import rsl_rl`` resolves to the embedded tree; return its root."""
    if not _RSL_RL_ROOT.is_dir():
        raise FileNotFoundError(
            f"Vendored rsl_rl missing at {_RSL_RL_ROOT}. "
            "Expected humanoidverse/adapt_fb/_vendor/rsl_rl in-tree."
        )
    root = str(_RSL_RL_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    return _RSL_RL_ROOT
