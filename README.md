<h1 align="center">
  UFO: A General <b>U</b>nsupervised Reinforcement Learning <b>F</b>ramework for Humanoid C<b>O</b>ntrol
</h1>

<p align="center">
  <a href="https://roboparty.github.io/UFO/"><img alt="Website" src="https://img.shields.io/badge/Website-roboparty.github.io%2FUFO-2563eb?style=for-the-badge" /></a>
  <a href="https://youtu.be/uJPcLdn9sNA"><img alt="Video" src="https://img.shields.io/badge/Video-Demo-7c3aed?style=for-the-badge" /></a>
  <a href="https://roboparty.github.io/UFO/assets/UFO.pdf"><img alt="PDF" src="https://img.shields.io/badge/PDF-Available-0f766e?style=for-the-badge" /></a>
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README_zh-CN.md">中文</a>
</p>

<p align="center">
  <img src="./assets/UFO.png" alt="UFO" height="72" style="vertical-align: middle;" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="./assets/rplab_logo.png" alt="ROBO PARTY LAB Logo" height="72" style="vertical-align: middle;" />
</p>

UFO is a humanoid-control framework built on **mjlab**. This fork provides
parallel entrypoints for **Astro P2 / Unitree G1 / RoboParty RP1.3**, multi-GPU
training and robot-aware inference. **FB-CPR-Aux** is the Astro baseline;
upstream G1/RP1 **FB and TeCH** presets remain available.

## Install

Use the native `ufo/` checkout of [DuofengPan/UFO-FB](https://github.com/DuofengPan/UFO-FB),
branch `migration/astro-new-architecture`. From its repository root:

```bash
python3 -m pip install --user uv
export PATH="$HOME/.local/bin:$PATH"
uv sync --locked
```

Requires Linux and a CUDA 12.8-compatible NVIDIA driver. The lockfile selects
PyTorch 2.7.1, mjlab 1.6, MuJoCo 3.11 and NCCL 2.26.5. Video export requires
`ffmpeg`. On the existing `.22` server, use `/root/code/UFO-next` inside
`atom9-ufo-vnc`; its separate `.venv` is ready. See [server/VNC entry](docs/ASTRO_MIGRATION.md#server-development-entry).

## Choose a robot

Commands below use **FB**. Motion data and checkpoints must match the robot.
The smoke command checks startup and sampling only; it disables cloud logging
and does not update weights. Full-training commands start training deliberately.
Use a fresh `--work-dir`; an existing checkpoint is resumed by the generic entrypoint.

### Astro P2 · 29 DoF

[Robot config](configs/robots/astro_p2_29dof.yaml) ·
[90/10 data manifest](configs/data/astro_lafan_high_dynamic.yaml) ·
[Network details](docs/ASTRO_NETWORK.md)

LaFAN: **54 full motions / 1,192 clips**. High dynamic: **24 full motions / 43 clips**
(20 kungfu and four backflips). Source weights remain **90% / 10%**, with
prioritization inside each source. LaFAN is downloaded separately; the
high-dynamic group, raw sources and provenance are versioned in this branch.

```bash
bash scripts/download_data.sh astro_lafan
./run_train.sh --agent fb --data-manifest configs/data/astro_lafan_high_dynamic.yaml \
  --gpu-ids single --smoke --buffer-size 8192 --work-dir /tmp/astro_smoke
./run_train.sh --agent fb --data-manifest configs/data/astro_lafan_high_dynamic.yaml \
  --gpu-ids all --num-envs 1024 --buffer-size 2560000 --num-agent-updates 16 --replay-device cpu \
  --work-dir runs/astro_fb
```

Astro retains **2048-wide Actor/Forward/independent Critics, six residual trunk
blocks, z=256 and FP32** (BF16 disabled; training allows TF32). Embedding depths
are separate from trunk depth; see the network document above. The 5090 preset
uses **eight GPUs, 1024 envs/GPU, 2,560,000 replay/rank, 16 updates and batch 1024**.
Online replay uses host RAM (`--replay-device cpu`); sampled batches and expert
data use the GPU. This keeps FP32 data and the full replay capacity while
leaving GPU memory for physics and optimizer updates. Plan for at least
256 GiB available host RAM for this eight-rank preset:

```bash
bash scripts/start_astro_high_dynamic_5090_8gpu.sh --dry-run  # validate/print only
# Start a new background run with SwanLab:
bash scripts/start_astro_high_dynamic_5090_8gpu.sh
```

The dedicated launcher refuses an existing run directory. Asset/forward and
communication checks passed; eight-GPU full-buffer long-run stability remains
untested. Rebuilding, SuperMimic import and migration notes are in
[Astro usage](docs/ASTRO_MIGRATION.md).

### Unitree G1 · 29 DoF

[Robot config](configs/robots/g1_29dof.yaml) ·
[Released motion data](https://huggingface.co/datasets/xuewang/UFO-MotionData) ·
[Released FB policy](https://huggingface.co/xuewang/ufo-g1-policy)

The released LaFAN data contains **40 full motions**. Use `--agent tech` to
select the upstream TeCH preset.

```bash
bash scripts/download_data.sh g1_lafan
./run_train.sh --robot g1 --agent fb --gpu-ids single --smoke \
  --buffer-size 8192 --work-dir /tmp/g1_smoke
./run_train.sh --robot g1 --agent fb --gpu-ids all --work-dir runs/g1_fb
./run_train.sh --robot g1  --agent tech --gpu-ids all --work-dir runs/g1_tech
```

### RoboParty RP1.3 · 24 DoF

[Robot config](configs/robots/rp1_3.yaml) ·
[Released motion data](https://huggingface.co/datasets/xuewang/UFO-MotionData)

The released data contains **55 full motions / 1,166 training clips at 50 Hz**.
Use `--agent tech` to select the upstream TeCH preset. The RP1 TeCH policy has
not been tested on the physical robot.

```bash
bash scripts/download_data.sh rp1_lafan
./run_train.sh --robot rp1 --agent fb --gpu-ids single --smoke \
  --buffer-size 8192 --work-dir /tmp/rp1_smoke
./run_train.sh --robot rp1 --agent fb --gpu-ids all --work-dir runs/rp1_fb
./run_train.sh --robot rp1 --agent tech --gpu-ids all --work-dir runs/rp1_tech
```

## Training and logging

`--num-envs`, `--buffer-size` and agent batch size are **per GPU**;
`--num-env-steps` is the **global** transition budget. `--gpu-ids all` uses all
visible GPUs; set `CUDA_VISIBLE_DEVICES` to select them. Robot network/precision
baselines differ; the Astro preset above is explicit.

**SwanLab** (default project `ufo-humanoid`):

```bash
uv run swanlab login
export SWANLAB_WORKSPACE=DuofengPan  # optional personal/org workspace
./run_train.sh --agent fb --data-manifest configs/data/astro_lafan_high_dynamic.yaml \
  --gpu-ids all --num-envs 1024 --buffer-size 2560000 --num-agent-updates 16 --replay-device cpu \
  --work-dir runs/astro_fb_swanlab --use-swanlab --swanlab-run-name astro_fb
```

Set `SWANLAB_PROJECT` to choose another project. Only rank zero uploads training
and evaluation metrics, using global steps. Normal exit and handled errors or
interruptions finalize the run; credentials stay in the SDK login store.

**W&B** is independently available: run `uv run wandb login`, then add
`--use-wandb --wandb-run-name NAME` to a training command. `WANDB_PROJECT` and
`WANDB_ENTITY` select the destination. See [training details](docs/TRAIN_INFERENCE.md)
for evaluation, separate model/replay save intervals and recovery semantics.

## Inference and export

Inference reads the robot configuration saved with the run. Select a matching
full-motion file for tracking; G1, RP1 and Astro use the same entrypoint:

```bash
./run_inference.sh tracking --model-folder runs/astro_fb \
  --data-path ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof.pkl \
  --motion-list 0 --save-mp4
./run_inference.sh tracking --model-folder runs/g1_fb \
  --data-path ufo/data/lafan_29dof.pkl --motion-list 0 --save-mp4
./run_inference.sh tracking --model-folder runs/rp1_fb \
  --data-path ufo/data/rp1_24dof_lafan_v7.pkl --motion-list 0 --save-mp4
```

Tracking/ONNX outputs require a newly trained matching checkpoint; asset
migration does not produce a trained Astro policy. FB reward inference needs
saved rank-zero replay; non-G1 reward tasks currently cover root/locomotion.
Non-G1 goal inference needs a robot-specific goal JSON. See
[tracking, reward, goal and export](docs/TRAIN_INFERENCE.md) or
`./run_inference.sh <tracking|reward|goal> --help`.

<details>
<summary>Use the released G1 FB policy</summary>

```bash
uv run hf download xuewang/ufo-g1-policy --local-dir model
./run_inference.sh tracking --model-folder model/g1_policy \
  --data-path ufo/data/lafan_29dof.pkl --motion-list 7 --save-mp4
```

The release includes the approximately 192M-step policy, ONNX and matching z,
but no optimizer/replay. Recomputing reward z requires your own replay.

</details>

## Documentation

- [Training and inference](docs/TRAIN_INFERENCE.md): schedules, evaluation, checkpoint and inference options.
- [Astro network](docs/ASTRO_NETWORK.md): effective layer counts, input/output dimensions and source files.
- [Astro assets and migration](docs/ASTRO_MIGRATION.md): server/VNC, data rebuilding and validation status.
- [Robot/data adaptation](docs/ROBOT_ADAPTATION.md): custom robots and motion conversion.
- [Architecture](docs/ARCHITECTURE.md) · [Multi-GPU troubleshooting](docs/MuitiGPU_TIPS.md).
- [Upstream historical benchmarks](docs/UPSTREAM_RESULTS.md): H20 G1/RP1 results and measurement scope.
- Deployment: [G1](https://github.com/Roboparty/UFO/tree/deploy) · [RP1](https://github.com/Roboparty/roboparty_deploy).

## Citation and license

UFO is released under [CC BY-NC 4.0](LICENSE) for non-commercial research use.

```bibtex
@misc{ufo2026,
  author       = {{RoboParty Lab Team}},
  title        = {UFO: An Unsupervised Reinforcement Learning Framework for Humanoid Control},
  year         = {2026},
  howpublished = {\url{https://github.com/Roboparty/UFO}},
  note         = {Project page: \url{https://roboparty.github.io/UFO/}}
}
```
