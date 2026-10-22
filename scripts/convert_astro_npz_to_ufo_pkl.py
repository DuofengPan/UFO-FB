#!/usr/bin/env python3
"""Convert Astro SuperMimic body-link NPZ motions into UFO training PKLs.

Supports the share pack layout under motions/ with a YAML selection list.
Converts NPZ -> RobotState (pelvis root + dof) -> UFO motion dict, then clips
to near-10s windows and writes shard PKLs + a train manifest.

Example:
  python -m scripts.convert_astro_npz_to_ufo_pkl \\
    --robot configs/robots/astro_p2_29dof.yaml \\
    --motion-root /data/share/astro_supermimic_88883_20261022/motions \\
    --selection /data/share/astro_supermimic_88883_20261022/training_selection_88724.yaml \\
    --out-dir humanoidverse/data/astro_supermimic_ufo \\
    --manifest-out configs/data/astro_supermimic_near10s.yaml
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import joblib
import yaml
from omegaconf import OmegaConf

# Allow `python scripts/convert_...py` from repo root without installing.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from humanoidverse.utils.motion_data.adapters import load_robot_state_npz
from humanoidverse.utils.motion_data.clip import clip_ufo_motion_dict
from humanoidverse.utils.motion_data.schema import validate_ufo_motion_dict
from humanoidverse.utils.robot_spec import load_robot_spec

# Diversity keywords used for reporting / optional boost sampling.
_DIVERSITY_RE = re.compile(
    r"fall|get.?up|getup|stand.?up|standup|recover|lie_down|lying|crawl|prone|supine|roll",
    re.IGNORECASE,
)


def _load_selection(path: Path) -> list[str]:
    raw = yaml.safe_load(path.read_text())
    if isinstance(raw, dict):
        files = raw.get("selected_files") or raw.get("files") or raw.get("motions")
    elif isinstance(raw, list):
        files = raw
    else:
        raise ValueError(f"Unsupported selection YAML schema: {path}")
    if not isinstance(files, list) or not files:
        raise ValueError(f"Selection YAML has no file list: {path}")
    return [str(item).strip() for item in files if str(item).strip()]


def _convert_one_npz(path: Path, *, robot_spec, motion_root: Path, source_name: str) -> dict[str, Any]:
    converted = load_robot_state_npz(
        path,
        source_name=source_name,
        robot_spec=robot_spec,
        base_dir=motion_root,
    )
    if len(converted) != 1:
        raise ValueError(f"Expected one motion from {path}, got {len(converted)}")
    return next(iter(converted.values()))


def _write_shard(data: dict[str, Any], path: Path, source_name: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    validated = validate_ufo_motion_dict(data, source_name)
    joblib.dump(validated, path)
    return path


def _rel_or_abs(path: Path, *, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return str(path.resolve())


def _write_manifest(
    *,
    out_path: Path,
    robot: str,
    shard_paths: list[Path],
    weight: float,
    repo_root: Path,
) -> Path:
    datasets = []
    per = float(weight) / max(len(shard_paths), 1)
    for idx, shard in enumerate(shard_paths):
        datasets.append(
            {
                "name": f"astro_supermimic_shard{idx:03d}",
                "format": "ufo_pkl",
                "train_path": _rel_or_abs(shard, base=repo_root),
                "weight": per,
            }
        )
    config = {
        "robot_config": robot,
        "datasets": datasets,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    OmegaConf.save(OmegaConf.create(config), out_path)
    return out_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--robot", default="configs/robots/astro_p2_29dof.yaml")
    parser.add_argument("--motion-root", required=True, type=Path)
    parser.add_argument("--selection", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--manifest-out", required=True, type=Path)
    parser.add_argument("--clip-seconds", type=float, default=10.0)
    parser.add_argument("--stride-seconds", type=float, default=10.0)
    parser.add_argument("--min-clip-seconds", type=float, default=1.0)
    parser.add_argument("--shard-size", type=int, default=4000, help="Clipped motions per shard PKL")
    parser.add_argument("--limit", type=int, default=None, help="Optional max source NPZ files")
    parser.add_argument(
        "--prefer-diversity",
        action="store_true",
        help="Put fall/getup/crawl/recover-like paths first (still converts the rest unless --limit).",
    )
    parser.add_argument(
        "--diversity-only",
        action="store_true",
        help="Only convert paths matching fall/getup/crawl/recover/lie/roll keywords.",
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    motion_root = args.motion_root.expanduser().resolve()
    selection = _load_selection(args.selection.expanduser().resolve())
    out_dir = args.out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    diversity = [p for p in selection if _DIVERSITY_RE.search(p)]
    others = [p for p in selection if not _DIVERSITY_RE.search(p)]
    if args.diversity_only:
        ordered = diversity
    elif args.prefer_diversity:
        ordered = diversity + others
    else:
        ordered = selection
    if args.limit is not None:
        ordered = ordered[: max(0, int(args.limit))]

    by_ds: dict[str, int] = defaultdict(int)
    for rel in ordered:
        by_ds[rel.split("/", 1)[0]] += 1
    print(
        f"convert plan: total={len(ordered)} diversity_hits={len(diversity)} "
        f"by_dataset={dict(sorted(by_ds.items(), key=lambda kv: -kv[1]))}"
    )

    robot_spec = load_robot_spec(args.robot)
    source_name = "astro_supermimic"
    shard_paths: list[Path] = []
    buffer: dict[str, Any] = {}
    converted = 0
    clips = 0
    skipped = 0
    errors = 0

    def flush_shard() -> None:
        nonlocal buffer, clips
        if not buffer:
            return
        shard_idx = len(shard_paths)
        shard_path = out_dir / f"train_near10s_shard{shard_idx:03d}.pkl"
        if shard_path.exists() and not args.force:
            raise FileExistsError(f"{shard_path} exists; pass --force to overwrite")
        _write_shard(buffer, shard_path, f"{source_name}:shard{shard_idx:03d}")
        shard_paths.append(shard_path)
        print(f"wrote {shard_path} motions={len(buffer)}")
        clips += len(buffer)
        buffer = {}

    for idx, rel in enumerate(ordered, start=1):
        path = motion_root / rel
        if not path.is_file():
            skipped += 1
            print(f"[skip-missing] {rel}")
            continue
        try:
            motion = _convert_one_npz(path, robot_spec=robot_spec, motion_root=motion_root, source_name=source_name)
            clipped = clip_ufo_motion_dict(
                {motion["motion_key"]: motion},
                clip_seconds=args.clip_seconds,
                stride_seconds=args.stride_seconds,
                keep_short=True,
                min_clip_seconds=args.min_clip_seconds,
                source_name=source_name,
            )
            for key, record in clipped.items():
                if key in buffer:
                    raise ValueError(f"Duplicate clipped key={key}")
                buffer[key] = record
            converted += 1
            if len(buffer) >= args.shard_size:
                flush_shard()
        except Exception as exc:  # noqa: BLE001 - keep converting remaining files
            errors += 1
            print(f"[error] {rel}: {exc}")
        if idx % 500 == 0 or idx == len(ordered):
            print(f"progress {idx}/{len(ordered)} converted={converted} errors={errors} buffer={len(buffer)}")

    flush_shard()
    if not shard_paths:
        raise RuntimeError("No shards written; nothing converted successfully")

    manifest_path = _write_manifest(
        out_path=args.manifest_out.expanduser().resolve(),
        robot=_rel_or_abs(Path(args.robot).expanduser().resolve(), base=_REPO_ROOT)
        if Path(args.robot).expanduser().is_absolute() or Path(args.robot).exists()
        else str(args.robot),
        shard_paths=shard_paths,
        weight=1.0,
        repo_root=_REPO_ROOT,
    )
    summary = {
        "source_files": len(ordered),
        "converted": converted,
        "skipped_missing": skipped,
        "errors": errors,
        "diversity_in_selection": len(diversity),
        "clip_seconds": args.clip_seconds,
        "shards": [str(p) for p in shard_paths],
        "approx_clips": clips,
        "manifest": str(manifest_path),
    }
    summary_path = out_dir / "conversion_summary.yaml"
    summary_path.write_text(yaml.safe_dump(summary, sort_keys=False))
    print(f"done summary={summary_path}")
    print(yaml.safe_dump(summary, sort_keys=False))


if __name__ == "__main__":
    main()
