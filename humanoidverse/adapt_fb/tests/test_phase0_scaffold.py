"""Phase 0 acceptance: package imports and metadata."""

from __future__ import annotations

from pathlib import Path

import humanoidverse.adapt_fb


ROOT = Path(__file__).resolve().parents[1]


def test_version_string() -> None:
    assert humanoidverse.adapt_fb.__version__ == "0.1.0"


def test_required_attribution_files_exist() -> None:
    for name in (
        "LICENSE",
        "NOTICE",
        "THIRD_PARTY_NOTICES.md",
        "docs/ROADMAP.md",
        "readme.md",
        "readme_zh-CN.md",
        "deps.lock.json",
    ):
        path = ROOT / name
        assert path.is_file(), f"missing {name}"
        assert path.stat().st_size > 0


def test_notice_mentions_orcs_author() -> None:
    text = (ROOT / "NOTICE").read_text(encoding="utf-8")
    assert "Lokesh Krishna" in text
    assert "ORCS" in text
    assert "UFO-FB" in text or "UFO-FB-adapt" in text
