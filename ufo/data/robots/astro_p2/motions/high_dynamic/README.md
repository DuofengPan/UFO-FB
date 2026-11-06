# Astro high dynamic motion group

`configs/data/astro_lafan_high_dynamic.yaml` samples the original Astro LaFAN
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

The 5090 eight-GPU launcher uses 1024 envs/GPU, 2,560,000 replay capacity/GPU,
16 updates/trigger and batch 1024, preserving 2048-wide independent critics and
FP32. See [Astro migration](../../../../../../docs/ASTRO_MIGRATION.md) for usage.
Validate without starting training:

```bash
bash scripts/start_astro_high_dynamic_5090_8gpu.sh --dry-run
```

This 24-motion group, its raw sources and provenance remain versioned. LaFAN
remains external and is obtained through the checksum-verifying downloader.
The original provenance JSON records the original build paths and hashes;
rebuilding with the native tools updates the generated report to native paths.
