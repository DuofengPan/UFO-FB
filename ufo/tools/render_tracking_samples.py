"""Render representative or all clips from saved trajectories, without rerollout."""

from __future__ import annotations

import argparse
import json
import os
import shutil

os.environ.setdefault("MUJOCO_GL", "egl")
os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
from pathlib import Path

import joblib
import mediapy
import mujoco
import numpy as np

from ufo.inference.runtime import MujocoQposRenderer, video_writer
from ufo.tools.bones_motion_import import sha256
from ufo.tools.robot_config import load_robot_spec


def select_samples(records, per_group=2):
    def score(r):
        return (
            r["joint_mae_rad"] / 0.3
            + r["local_body_error_m"] / 0.15
            + r["local_hand_error_m"] / 0.2
            + r["root_error_m"] / 0.3
            + 10 * r["fall_detected"]
        )

    ordered = sorted(records, key=lambda r: (score(r), r["motion_key"]))
    n = len(ordered)
    groups = {
        "good": ordered[: max(per_group, n // 3)],
        "medium": ordered[n // 3 : 2 * n // 3],
        "poor": list(reversed(ordered[2 * n // 3 :])),
    }
    selected = []
    used = set()
    for group, pool in groups.items():
        if group == "medium":
            pool = sorted(pool, key=lambda r: abs(ordered.index(r) - (n - 1) / 2))
        for r in pool:
            if r["motion_key"] in used:
                continue
            selected.append(dict(group=group, score=score(r), **r))
            used.add(r["motion_key"])
            if sum(x["group"] == group for x in selected) == per_group:
                break
    return selected


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--evaluation", type=Path, required=True)
    p.add_argument("--robot-config", type=Path, required=True)
    p.add_argument("--per-group", type=int, default=2)
    p.add_argument("--all", action="store_true", help="Render every motion, grouped by screening result")
    p.add_argument("--camera-azimuth", type=float, default=135.0)
    p.add_argument("--size", type=int, default=360)
    p.add_argument("--stride", type=int, default=2)
    args = p.parse_args()
    if shutil.which("ffmpeg") is None:
        try:
            import imageio_ffmpeg

            mediapy.set_ffmpeg(imageio_ffmpeg.get_ffmpeg_exe())
        except ImportError as exc:
            raise RuntimeError("Install ffmpeg on PATH or provide imageio-ffmpeg for video encoding") from exc
    if min(args.per_group, args.size, args.stride) < 1:
        p.error("Positive counts required")
    result = json.loads((args.evaluation / "results.json").read_text())
    spec = load_robot_spec(args.robot_config)
    if sha256(spec.xml_path) != result["robot_xml_sha256"]:
        raise ValueError("Renderer XML differs from evaluation robot")
    trajectories = joblib.load(args.evaluation / "trajectories.pkl")
    by_key = {t["motion_key"]: t for t in trajectories}
    selected = (
        [dict(group="pass" if r["screening_pass"] else "review", **r) for r in result["motions"]]
        if args.all
        else select_samples(result["motions"], args.per_group)
    )
    videos = args.evaluation / ("videos_all" if args.all else "videos")
    videos.mkdir(exist_ok=True)
    renderer = MujocoQposRenderer(
        Path(spec.xml_path), render_size=args.size, camera_distance=3.0, camera_azimuth=args.camera_azimuth, camera_elevation=-15.0
    )

    def render(qpos, anchor):
        renderer.data.qpos[:] = qpos
        renderer.data.qvel[:] = 0
        mujoco.mj_forward(renderer.model, renderer.data)
        renderer.camera.lookat[:] = [anchor[0], anchor[1], max(anchor[2], 0.75)]
        renderer.renderer.update_scene(renderer.data, camera=renderer.camera)
        return renderer.renderer.render().copy()

    try:
        for record in selected:
            t = by_key[record["motion_key"]]
            path = videos / f"{record['group']}_{record['motion_id']:02d}.mp4"
            if path.exists():
                raise ValueError(f"Refusing to overwrite {path}")
            ids = range(0, len(t["policy_qpos"]), args.stride)
            fps = 1 / (t["dt"] * args.stride)
            with video_writer(path, shape=(args.size, 2 * args.size), fps=fps) as writer:
                for i in ids:
                    ref = t["reference_qpos"][i]
                    policy = t["policy_qpos"][i]
                    writer.add_image(np.concatenate([render(ref, ref[:3]), render(policy, ref[:3])], axis=1))
            record.update(video=str(path.relative_to(args.evaluation)), sha256=sha256(path), frames=len(ids), fps=fps)
            sidecar = path.with_suffix(".json")
            sidecar.write_text(json.dumps(record, ensure_ascii=False, indent=2))
            print("rendered", record["video"], len(ids), flush=True)
    finally:
        renderer.close()
    (args.evaluation / ("all_videos.json" if args.all else "video_selection.json")).write_text(
        json.dumps(
            dict(
                source_results_sha256=sha256(args.evaluation / "results.json"),
                layout="left: reference FK; right: actual policy rollout; common camera follows reference root, so root drift stays visible",
                grouping=(
                    "all motions grouped by existing screening_pass"
                    if args.all
                    else "relative thirds ranked by sum of joint/.3 + body/.15 + hand/.2 + root/.3 + 10*fall; two from each group, not absolute labels"
                ),
                camera_azimuth=args.camera_azimuth,
                videos=selected,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
