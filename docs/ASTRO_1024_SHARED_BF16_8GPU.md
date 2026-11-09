# Astro 1024 / shared critic / BF16: eight-GPU reproduction

This branch preserves the Astro baseline at `886d5f2` and selects the small FB
network explicitly in dedicated launchers. The robot YAML defaults are unchanged.

## What changed on this branch

- `c617b68`: adds `--bf16-amp` / `--no-bf16-amp`, passes that optional override
  through `build_mjlab_config()` and `build_fb_agent()`, and adds the eight-GPU
  short-test launcher. Omitting the option preserves the robot baseline.
- `2e80688`: puts temporary CUDA compilation and motion caches in executable
  local `/var/tmp` paths. The tested image's `/tmp` was mounted `noexec`.
- `b37a624`: adds the formal eight-GPU launcher, including SwanLab, tracking
  evaluation, prioritization, and the full 192-million-global-step budget.

Files: `ufo/train.py`, `ufo/agents/fb_cpr_aux/config.py`,
`scripts/test_astro_1024_shared_bf16_8gpu.sh`, and
`scripts/start_astro_1024_shared_bf16_5090_8gpu.sh`.

## Measured result and scope of the eight-hour target

The formal run used code commit `b37a624ca874408e0495731d4d710e71a1a3fc3d`.
It started at **2026-11-06 16:02:11 UTC+8** and finished uploading its final
checkpoint at **23:30:58 UTC+8**, about **7 h 29 min** after process start.
Environment installation, data transfer, and earlier smoke tests are excluded.
Compilation caches had already been exercised by the smoke tests.

- Final saved global step: **191,995,904**. The 192,000,000 budget is rounded
  down by the trainer's 8,192-step global increment.
- Optimizer updates per rank: **374,816**; world size: **8**.
- Final rank parameter/buffer consistency check: `max_abs_diff_from_rank0=0`.
- Best recorded tracking EMD: **1.074284** at 182,575,104 steps.
- Last recorded evaluation EMD: **1.083497** at 188,981,248 steps. The final
  saved checkpoint at 191,995,904 steps has no separate terminal evaluation.
- SwanLab: https://swanlab.cn/@DuofengPan/ufo-humanoid/runs/qjj0v614

This is one validated run, **not an eight-hour runtime guarantee**. Equal GPU
model and count alone do not establish equal throughput. CPU scheduling, NUMA
layout, PCIe links, GPU clocks/power limits, competing workloads, drivers, and
storage affect elapsed time. Reproduce the environment below and measure the
short run before accepting an eight-hour target. Including evaluation and saves,
192 million steps in eight hours requires about **6,667 global env steps/s**.
The completed run averaged about **7,130 global env steps/s** from process start
through final save/upload. Normal training-only intervals were about 7,500–8,400
steps/s after warmup; these are not end-to-end rates or guaranteed lower bounds.

## Hardware and image prerequisites

- Linux x86_64, tested with Ubuntu 22.04, eight exclusively available RTX 5090
  GPUs (32 GiB each), NVIDIA driver 580.126.09, Python 3.10.12.
- Tested host CPU: Xeon Gold 6530; 64 physical / 128 logical CPUs visible.
- Tested RAM: about 503 GiB. Replay alone allocates **21.875 GiB per rank**
  (175 GiB total); observed worker RSS was about 26–27 GiB per rank.
  Reserve at least 256 GiB free host RAM, and leave additional headroom for
  checkpoint loading and OS caches; matching the tested 512-GB-class host is
  preferred.
- Tested container `/dev/shm`: 8 GiB. Do not inherit the usual 64-MiB Docker
  default. Follow `docs/MuitiGPU_TIPS.md` with its machine-specific caveats.
- A local, executable, writable `/var/tmp` filesystem for compilation caches.
- Persistent run storage with capacity for model, optimizer, current and previous
  replay snapshots; each full rank-0 replay is about 23.5 GB. Reserve at least
  100 GB free for one formal run and its checkpoint rotation.
- C/C++ build tools and **Python 3.10 development headers**. The compiler tests
  failed without `Python.h`. These OS packages are not installed by Git or uv.
  A recreated container must be provisioned again, even when `/data` persists.

For the Ubuntu system Python used by this run, provision as root (or with sudo):

```bash
apt-get update
apt-get install -y python3.10-dev build-essential
```

## Checkout and Python dependencies

Use a fresh checkout or a separate worktree for this experiment:

```bash
git clone --branch exp/astro-1024-shared-bf16 --single-branch \
  https://github.com/DuofengPan/UFO-FB.git UFO-next-small
cd UFO-next-small
uv sync --locked --group dev
```

The tested uv version was 0.12.3. `uv.lock` pins the actual dependencies, including
PyTorch 2.7.1+cu128, mjlab 1.6.0, MuJoCo 3.11.0, and NCCL 2.26.5. Do not reuse a
virtualenv copied from a different checkout. If an existing editable environment
was relocated, rerun `uv sync --locked --group dev` to repair the install path.
The launcher sources `scripts/runtime_libraries.sh` to select the checkout's NCCL.

## External data: a clone alone is insufficient

High-dynamic assets are tracked in Git. The following two Astro LaFAN files are
external and ignored by Git. Obtain the authorized copies from an existing
training server and place them at the paths below, or mount those files there.
Do not substitute a different preprocessing/version when comparing runtimes or
quality. There is no dataset download or credential embedded in this branch.

SHA256 checksums, relative to the checkout:

```text
c832ad890de4ba766378e3e6843d1b089e398cef77b8656f81df4796bdf6e1a7  ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof.pkl
4e727221206c0e86dd9e01c53bafac2a743ba74c5866710134c07dad8ea2e5b3  ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof_10s-clipped.pkl
a357c568e4b8e6b4369e113d8d65267672583253cbd5c200c460f50be6186ad7  ufo/data/robots/astro_p2/motions/high_dynamic/astro_high_dynamic_50hz.pkl
5690116b71893ca17ddabcdb9016986b74cfc9ab0827affbe2e99ebb534e6240  ufo/data/robots/astro_p2/motions/high_dynamic/astro_high_dynamic_50hz_10s-clipped.pkl
```

The manifest is `configs/data/astro_lafan_high_dynamic.yaml`: 90% LaFAN and 10%
high-dynamic source sampling weight, 1,192 and 43 clipped training motions.

## Verify, smoke test, then launch

For formal online logging, log in on the target machine using its own local
SwanLab SDK store. Do not commit login files, API keys, or SSH keys:

```bash
.venv/bin/python -m swanlab login
.venv/bin/python -m swanlab verify
```

Verify the model overrides and dataset manifest without launching workers:

```bash
bash scripts/start_astro_1024_shared_bf16_5090_8gpu.sh --dry-run
```

The dry run checks the model/data configuration; GPU-count/free-memory checks
run on an actual launch. Run the bounded 384,000-step test first:

```bash
bash scripts/test_astro_1024_shared_bf16_8gpu.sh
```

The launcher prints the background PID and run directory. Wait for that test to
finish before starting the formal job. Inspect `launcher.log`,
`checkpoint/train_status.json`, and `checkpoint/distributed_sync.json` for actual
optimizer updates and cross-rank consistency. The original short test completed
560 updates. Its default scalar log interval is 384,000 steps, beyond its rounded
save endpoint, so it does not produce a training scalar row.

Once all eight GPUs are free:

```bash
bash scripts/start_astro_1024_shared_bf16_5090_8gpu.sh
```

Formal settings: 1,024 envs/rank (8,192 global); actor/forward/critic width 1,024;
shared critic; BF16 autocast with FP32 model parameters; CPU online replay with
2,560,000 transitions/rank; expert data on GPU; batch 1,024/rank; 16 optimizer
updates per trigger; seed 4,728 plus rank; evaluation/prioritization enabled;
192,000,000 global env-step budget; model saves every 3,200,000 global steps;
rank-0 replay saves every 16,000,000 steps and at termination.

Launch environment includes `NCCL_P2P_DISABLE=1`, `NCCL_SHM_DISABLE=0`,
`NCCL_CUMEM_HOST_ENABLE=0`, `TORCH_NCCL_USE_COMM_NONBLOCKING=0`,
`OMP_NUM_THREADS=1`, and executable local compile caches. These settings were
validated on this eight-5090 topology; see the multi-GPU tips before adapting
them to different hardware. The launch guard requires exactly eight visible
GPUs and at least 28,000 MiB free on every GPU.

Runs use unique timestamped folders under `runs/`. Each contains the command,
Git commit, dirty patch, effective configuration, robot config, manifest, and
data provenance. Runtime logs, datasets, virtualenvs, compiled caches, and model
checkpoints are not uploaded by publishing this source branch.
