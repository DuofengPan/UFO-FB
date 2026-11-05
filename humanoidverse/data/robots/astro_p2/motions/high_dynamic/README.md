# Astro high dynamic motion group

`humanoidverse/data/robots/astro_p2/config/lafan_high_dynamic.yaml` samples the original Astro LaFAN
source with mass 0.9 and this single high dynamic source with mass 0.1.
These are source sampling weights, not ten percent of stored frames and not a
separate ten percent for each subcategory. Existing within-source expert
prioritization remains enabled.

This group contains 20 selected Astro kungfu takes and the four previously
evaluated Qingtong backflips (012, 015, 048, 049). All four are included, including
the two that the previous fine-tuned policy did not track successfully.

Files in `raw/kungfu/` are the original selected PKLs. Their provenance sidecars
in `raw/provenance/` identify the matching Astro retarget XML and output hashes.
`joint_layout.json` records that XML's 29 hinge joints in qpos order; the builder
checks it against the training RobotSpec. Root quaternion order is xyzw, Z is up,
positions are metres and joint angles are radians. `raw/qingtong/` contains the
previously resampled 50 Hz robot-state CSV references, without changes.

Rebuild from the repository root with the project's Python environment:

```bash
.venv/bin/python scripts/build_astro_high_dynamic.py --force
```

Kungfu trajectories are resampled from approximately 70 Hz to 50 Hz using linear
interpolation for position/joints and SLERP for root rotation, without time
scaling, frame duplication, or removing flight phases. The full dataset has 24
named motions. The training twin uses the repository's non-overlapping 10 second
clipper, preserving tails of at least one second. `manifest.json` records counts,
source hashes, durations and generated artifact hashes. The builder validates
finite arrays, quaternion norms, source provenance, rotation/joint reconstruction,
clip coverage and serialization. This validates the data contract, not policy
tracking success; no joint clipping or trajectory correction is silently applied.

Start a new eight-GPU training run (4096 envs/GPU, default 5,120,000 buffer per
rank, 64 updates/trigger, 192 million global env steps, SwanLab enabled):

```bash
bash scripts/start_astro_high_dynamic_8gpu.sh
```

The launcher creates a new timestamped run, records the commit/data manifest,
refuses an existing directory, and never copies a checkpoint or replay buffer.
Original baseline and flip-only runs are preserved. The original
`humanoidverse/data/robots/astro_p2/config/lafan.yaml` stays available for baseline reproduction.

GPU startup requires at least 32 GiB free on each of GPUs 0-7 (a conservative
startup margin, not a measured peak allocation). The first attempt with about
9 GiB free failed in Warp CUDA graph creation. If resources are occupied, use
`--wait-for-gpus`; the launcher checks every 60 seconds for at most 24 hours and
then starts the same full training command. It never resets GPUs or kills other
jobs. `MIN_FREE_GPU_MIB` and `MAX_GPU_WAIT_SECONDS` are explicit overrides.
