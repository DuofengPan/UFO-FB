# Astro P2 on the native UFO architecture

This fork ports Astro assets and integration from UFO-FB `938ca44` onto upstream
`4f1a6f6`. The original worktree, Python environment, runs and checkpoints remain
separate. Old checkpoints and replay are not migrated or resumed.

## Robot and network baseline

`configs/robots/astro_p2_29dof.yaml` is the reviewed source of truth. It preserves
29 controlled joints, their order, initial pose, PD gains, motor limits,
armature/friction and contact semantics. The active XML remains
`astro_p2_29dof_simplify_primitive_collision.xml`; the capsulefeet XML is retained
as an alternative asset, not silently selected. Old metadata described that
alternative even though the active YAML selected the primitive collision XML.

The native configuration replaces legacy Hydra selections. It explicitly keeps
30% lying-down initialization and angular-velocity observation scale `0.25`.
Auxiliary critic rewards and their weights are copied from the old FB baseline;
they are distinct from the scalar environment reward weights.

The Astro FB preset preserves:

- Actor, Forward and both independent Critics: width 2048, six residual layers,
  Forward/Critic ensembles contain two members. Actor embeddings have two
  layers; Forward/Critic embeddings use six, as in the actual legacy residual
  implementation (its old `embedding_layers: 2` field was not used there).
- Backward: width 256, one hidden layer; latent dimension 256.
- Discriminator: width 1024, three hidden layers.
- Existing input filters, normalizers, sequence length 8, actor standard
  deviation 0.05, learning rates and other FB hyperparameters.
- FP32 parameters, BF16 autocast disabled. Upstream FP32 matmul policy allows
  TF32; this is not a promise of strict IEEE FP32 matrix multiplication.

Upstream execution optimizations (forward compilation, fused Adam, tensor
rollouts, actor isolation, bucketed synchronization) remain present. The 5090
Torch-cache release workaround is opt-in and enabled by the Astro launcher.
This port does not establish 5090 long-run stability or guarantee old/new
physics, evaluation scores or trajectories are numerically identical.

## Motion data

`configs/data/astro_lafan.yaml` selects LaFAN only.
`configs/data/astro_lafan_high_dynamic.yaml` selects these fixed source masses:

- LaFAN: 90%, 54 full motions / 1,192 training clips.
- High dynamic: 10%, 20 retargeted kungfu + four Qingtong backflips,
  24 full motions / 43 training clips at 50 Hz.

Prioritization operates within each source. Full motions and training clips keep
their separate purposes; full-motion indices must not be substituted for clip
indices. The existing PKLs are copied unchanged, not rebuilt during migration.
Raw high-dynamic sources, provenance JSON and rebuild tooling are retained.
The copied provenance describes the original build paths; its hashes remain
valid. Rebuilding with native tools produces native-path provenance.

LaFAN motion binaries remain external to Git; a fresh clone needs them separately.
The small, previously versioned high-dynamic group (including raw sources and
provenance) stays versioned in this branch. LaFAN can be obtained with the
checksum-verifying command:

```bash
bash scripts/download_data.sh astro_lafan
```

The high-dynamic files are included in this branch, not downloaded from a new
external URL. To rebuild the generated PKLs from the included raw sources:

```bash
.venv/bin/python scripts/build_astro_high_dynamic.py --force
```

`--force` replaces generated datasets and their manifest; it is not needed for
normal training. To reconstruct LaFAN from the original GMR source archive:

```bash
.venv/bin/python scripts/convert_astro_gmr_lafan_to_ufo_pkl.py --help
```

The documented SuperMimic import remains available for external data packs;
those large packs are not part of this migration:

```bash
.venv/bin/python scripts/convert_astro_npz_to_ufo_pkl.py \
  --robot configs/robots/astro_p2_29dof.yaml \
  --motion-root /path/to/astro_supermimic/motions \
  --selection /path/to/training_selection.yaml \
  --out-dir ufo/data/astro_supermimic_ufo \
  --manifest-out configs/data/astro_supermimic_near10s.yaml \
  --prefer-diversity
```

The reader retains Astro body-link NPZ support (`dof_positions`, body transforms,
named joints), in addition to the upstream RobotState format. It preserves the
legacy quaternion-order heuristic for body-link packs; review quaternion
conventions before importing a different source.

## Server development entry

On `.22`, the host worktree is `/data/atom9/code/UFO-next` and the same files
are visible inside `atom9-ufo-vnc` at `/root/code/UFO-next`:

```bash
ssh atom9-22
docker exec -it -w /root/code/UFO-next atom9-ufo-vnc bash --noprofile --norc
source .venv/bin/activate
```

In an existing VNC terminal, use `cd /root/code/UFO-next` followed by
`source .venv/bin/activate`. The old terminal startup and old training shortcut
still refer to the old project; use the new checkout's scripts explicitly.

## Environment and validation commands

From the new checkout, create its own environment; do not upgrade the old `ufo`
Conda environment in place:

```bash
uv sync --locked --group dev
./run_train.sh --agent fb --data-manifest configs/data/astro_lafan_high_dynamic.yaml \
  --gpu-ids single --smoke --buffer-size 8192 --work-dir /tmp/astro_native_smoke
```

The server container globally preloads NCCL 2.27.7. New checkout entrypoints
(`run_train.sh`, `run_inference.sh` and the Astro launcher) prefer this checkout's
locked NCCL 2.26.5, preserving unrelated preloads. The old checkout/container
settings are unchanged. If launching Python directly inside this container,
select the new runtime first:

```bash
source scripts/runtime_libraries.sh
ufo_use_project_nccl "$PWD"
```

PyTorch's reported NCCL tuple is its compiled version; the actual loaded library
was checked with `ncclGetVersion`, then exercised with a two-rank all-reduce.

The upstream `--smoke` checks startup/sampling, disables cloud logging and does
not update model weights. It is not a training-quality or eight-GPU capacity test.
The asset/config regression tests do not require training:

```bash
.venv/bin/python -m pytest tests/test_astro_migration.py tests/test_swanlab_logging.py
bash scripts/start_astro_high_dynamic_5090_8gpu.sh --dry-run
```

## SwanLab and deliberate training launch

```bash
.venv/bin/swanlab login
export SWANLAB_WORKSPACE=DuofengPan
# Optional; default project is ufo-humanoid:
export SWANLAB_PROJECT=ufo-humanoid
```

Login uses the SDK's user credential store. No key belongs in the robot YAML,
README or Git. In the existing server container, the previously authorized
account login is shared by the new environment; no new credential copy is needed.
Only rank zero initializes/uploads. Training and tracking-evaluation metrics
use global environment steps, and the run is finalized on normal exit,
exceptions or handled SIGINT/SIGTERM. SIGKILL cannot run cleanup.

For a generic training command, add `--use-swanlab --swanlab-run-name NAME`.
W&B remains independently available. The 5090 launcher below is a deliberate
start command, not something executed by asset migration:

```bash
bash scripts/start_astro_high_dynamic_5090_8gpu.sh
```

It starts a new background run: eight visible GPUs, 1024 envs/GPU, 2,560,000
replay transitions/rank in host RAM, batch 1024 and 16 updates, 192M global transitions, model snapshots
every 3.2M and rank-zero replay every 16M. It refuses an existing run directory
and insufficient GPU memory; it does not stop another process or resume an old
run. Set `RUN_NAME` for an explicit new name.

Periodic rank-zero replay is suitable for the upstream recovery policy and FB
reward inference; it is not a full eight-rank replay snapshot. Upstream
`SAVE_AND_STOP` requests an all-rank snapshot at the next checkpoint boundary.
Exact continuation of simulator/RNG state is not claimed. Do not treat old
UFO-FB checkpoints as native-format checkpoints.

Tracking and ONNX export use the new robot-aware entrypoints described in
[training/inference](TRAIN_INFERENCE.md), with a newly trained matching model.
Non-G1 goal inference requires a robot-specific goal JSON; non-G1 FB reward
inference is limited to supported root/locomotion tasks. Physical deployment
and policy quality are outside this asset-port validation.

## Migration validation (2026-11-06)

- 91 asset files checked; model, dataset and raw-source bytes retained. The
  native-path README and Git attributes are deliberately adapted.
- The six network families match both the legacy implementation and saved
  checkpoint header's tensor names/sizes. Actual observations: state=64,
  privileged=463, last_action=29, history_actor=372.
- Native mjlab 1.6 / MuJoCo 3.11: four simulated environments, full 2048-wide
  model, 16 forward/physics steps, 12 timeout-reset transitions. Validation
  alone shortens timeouts to 0.1 s; the real config keeps 10 s.
- CPU regression suite: 440 passed, 19 skipped. Two subsequent runtime-wrapper
  tests also passed; the combined Astro/SwanLab/wrapper subset passed 17 tests.
- Locked NCCL 2.26.5: two GPUs, three 1,048,576-element all-reduces passed.
- High-dynamic rebuilding in scratch reproduced all 24 motions with zero
  difference in pose_aa, root position, joint position and root quaternion.
- Real SwanLab SDK initialization, train/eval logging and finish checked in
  explicit offline mode; account verification returned DuofengPan.

No optimizer was created by the physics/forward or NCCL checks. No formal run
was started/resumed and no cloud training experiment was created. Eight-GPU
full-buffer and repeated checkpoint/evaluation stress tests remain separate.


## 5090 online replay memory placement

The native replay stores both current and next observations. With the migrated
Astro observation schema, capacity 2,560,000 consumes **21.875 GiB/rank** in FP32
(175 GiB across eight ranks). Keeping this replay on each 32 GiB 5090 caused
Warp CUDA-graph OOM during collection after the initial tracking evaluation.

The Astro 5090 launcher therefore uses `--replay-device cpu`. Only online replay
storage moves to host RAM; expert data, sampled training batches, network
parameters, optimizer state and simulation remain on GPUs. Capacity, network
topology, FP32 data, batch size and update count are unchanged. The eight-rank
preset should have at least 256 GiB available host RAM. This avoids reducing
replay precision or capacity, but CPU sampling and transfers affect throughput;
measure actual training FPS. Omitting this optional flag retains upstream
device defaults. Replay checkpoint loading uses the selected online device.

Multi-GPU launch now disables automatic elastic restarts so an error preserves
its first failure and does not silently restart from an earlier checkpoint.
