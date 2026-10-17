"""Put vendored dependencies on ``sys.path`` (no pip install required for imports)."""

from __future__ import annotations

import sys
from pathlib import Path

# humanoidverse/adapt_fb/_vendor/rsl_rl
_ADAPT_FB_ROOT = Path(__file__).resolve().parents[1]
_RSL_RL_ROOT = _ADAPT_FB_ROOT / "_vendor" / "rsl_rl"


def ensure_vendored_rsl_rl() -> Path:
    """Ensure ``import rsl_rl`` resolves to the embedded tree; return its root.

    If a different ``rsl_rl`` (e.g. site-packages) is already in ``sys.modules``,
    drop those entries and re-bind after prepending the vendor root.
    """
    if not _RSL_RL_ROOT.is_dir():
        raise FileNotFoundError(
            f"Vendored rsl_rl missing at {_RSL_RL_ROOT}. "
            "Expected humanoidverse/adapt_fb/_vendor/rsl_rl in-tree."
        )
    root = str(_RSL_RL_ROOT.resolve())
    # Prefer vendor even if already present further down the path.
    while root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)

    vendor_pkg = (_RSL_RL_ROOT / "rsl_rl").resolve()
    stale = [
        name
        for name, mod in list(sys.modules.items())
        if name == "rsl_rl" or name.startswith("rsl_rl.")
    ]
    for name in stale:
        mod = sys.modules.get(name)
        origin = getattr(mod, "__file__", None) if mod is not None else None
        if origin is None:
            sys.modules.pop(name, None)
            continue
        try:
            Path(origin).resolve().relative_to(vendor_pkg)
        except (ValueError, OSError):
            sys.modules.pop(name, None)

    return _RSL_RL_ROOT
