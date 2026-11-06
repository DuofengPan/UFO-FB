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

UFO 是基于 **mjlab** 的人形机器人无监督强化学习框架。本分支提供
**Astro P2 / Unitree G1 / RoboParty RP1.3** 三种机器人入口，支持多卡训练与机器人配置感知的推理。
Astro 维护 **FB-CPR-Aux** 基线，G1/RP1 继续保留上游 **FB、TeCH** 预设。

## 安装

使用 [DuofengPan/UFO-FB](https://github.com/DuofengPan/UFO-FB) 的
`migration/astro-new-architecture` 分支，在包含 `ufo/` 的仓库根目录执行：

```bash
python3 -m pip install --user uv
export PATH="$HOME/.local/bin:$PATH"
uv sync --locked
```

需要 Linux 和兼容 CUDA 12.8 的 NVIDIA 驱动。锁文件选择 PyTorch 2.7.1、mjlab 1.6、
MuJoCo 3.11 和 NCCL 2.26.5；导出视频需要 `ffmpeg`。
现有 `.22` 服务器的容器目录为 `/root/code/UFO-next`，独立 `.venv` 已就绪，
进入方法见[服务器／VNC 开发入口](docs/ASTRO_MIGRATION.md#server-development-entry)。

## 选择机器人

以下命令均以 **FB** 为例。动作数据和 checkpoint 必须与机器人匹配。
`--smoke` 只检查启动和采样，关闭云端日志、不更新权重；完整训练命令会实际启动训练。
新实验使用新的 `--work-dir`，通用入口会恢复该目录里已有的 checkpoint。

### Astro P2 · 29 自由度

[机器人配置](configs/robots/astro_p2_29dof.yaml) ·
[90/10 数据配置](configs/data/astro_lafan_high_dynamic.yaml) ·
[实际网络层数](docs/ASTRO_NETWORK.md)

LaFAN：**54 条完整动作 / 1,192 个训练片段**；高动态：**24 条完整动作 / 43 个片段**
（20 条功夫、4 条后空翻）。数据源占比保持 **90% / 10%**，优先采样只在各源内部调整。
LaFAN 单独下载；高动态动作、原始来源与溯源文件随本分支版本管理。

```bash
bash scripts/download_data.sh astro_lafan
./run_train.sh --agent fb --data-manifest configs/data/astro_lafan_high_dynamic.yaml \
  --gpu-ids single --smoke --buffer-size 8192 --work-dir /tmp/astro_smoke
./run_train.sh --agent fb --data-manifest configs/data/astro_lafan_high_dynamic.yaml \
  --gpu-ids all --num-envs 1024 --buffer-size 2560000 --num-agent-updates 16 --replay-device cpu \
  --work-dir runs/astro_fb
```

网络保留 **2048 宽度的 Actor、Forward 和独立 Critic，6 层残差主干，z=256，FP32**
（关闭 BF16，训练允许 TF32）。输入 embedding 的层数另计，详见上面的网络说明。
5090 专用预设为 **8 卡、每卡 1024 环境、256 万 buffer、16 updates、batch 1024**：

5090 预设将在线 replay 放在主机内存（`--replay-device cpu`），抽样批次再传入 GPU；
专家数据仍留在 GPU。这样保留 FP32 数据和完整 buffer 容量，为物理模拟及优化器留出显存。
该八卡预设建议至少留出 **256 GiB 主机可用内存**。

```bash
bash scripts/start_astro_high_dynamic_5090_8gpu.sh --dry-run  # 仅校验、打印命令
# 从头启动新的后台训练，启用 SwanLab：
bash scripts/start_astro_high_dynamic_5090_8gpu.sh
```

专用脚本拒绝复用已有运行目录。资产、前向和通信检查已通过，八卡满 buffer 长跑尚未验证。
数据重建、SuperMimic 导入及迁移记录见 [Astro 使用说明](docs/ASTRO_MIGRATION.md)。

### Unitree G1 · 29 自由度

[机器人配置](configs/robots/g1_29dof.yaml) ·
[已发布动作数据](https://huggingface.co/datasets/xuewang/UFO-MotionData) ·
[已发布 FB 模型](https://huggingface.co/xuewang/ufo-g1-policy)

发布的 LaFAN 数据包含 **40 条完整动作**。需要上游 TeCH 预设时，将 `--agent fb` 改为
`--agent tech`。

```bash
bash scripts/download_data.sh g1_lafan
./run_train.sh --robot g1 --agent fb --gpu-ids single --smoke \
  --buffer-size 8192 --work-dir /tmp/g1_smoke
./run_train.sh --robot g1 --agent fb --gpu-ids all --work-dir runs/g1_fb
./run_train.sh --robot g1  --agent tech --gpu-ids all --work-dir runs/g1_tech
```

### RoboParty RP1.3 · 24 自由度

[机器人配置](configs/robots/rp1_3.yaml) ·
[已发布动作数据](https://huggingface.co/datasets/xuewang/UFO-MotionData)

发布的数据包含 **55 条完整动作 / 1,166 个训练片段，50 Hz**。
需要上游 TeCH 预设时改为 `--agent tech`。RP1 的 TeCH 策略尚未进行真机测试。

```bash
bash scripts/download_data.sh rp1_lafan
./run_train.sh --robot rp1 --agent fb --gpu-ids single --smoke \
  --buffer-size 8192 --work-dir /tmp/rp1_smoke
./run_train.sh --robot rp1 --agent fb --gpu-ids all --work-dir runs/rp1_fb
./run_train.sh --robot rp1 --agent tech --gpu-ids all --work-dir runs/rp1_tech
```

## 训练参数与日志

`--num-envs`、`--buffer-size` 和 agent 的 batch size 均为**每卡值**；
`--num-env-steps` 为**全局采样预算**。`--gpu-ids all` 使用所有可见 GPU，
可通过 `CUDA_VISIBLE_DEVICES` 选择显卡。不同机器人的网络与精度基线不同，Astro 已显式固定为上文配置。

**SwanLab**，默认项目 `ufo-humanoid`：

```bash
uv run swanlab login
export SWANLAB_WORKSPACE=DuofengPan  # 可选的个人／组织工作空间
./run_train.sh --agent fb --data-manifest configs/data/astro_lafan_high_dynamic.yaml \
  --gpu-ids all --num-envs 1024 --buffer-size 2560000 --num-agent-updates 16 --replay-device cpu \
  --work-dir runs/astro_fb_swanlab --use-swanlab --swanlab-run-name astro_fb
```

可用 `SWANLAB_PROJECT` 修改项目名。只有 rank 0 上传训练与评估指标，横轴为全局环境步数。
正常结束、异常和可处理的中断会结束云端运行状态；凭据由 SDK 本地保存。

**W&B** 可独立启用：先执行 `uv run wandb login`，再给训练命令添加
`--use-wandb --wandb-run-name NAME`，通过 `WANDB_PROJECT`、`WANDB_ENTITY` 选择项目／账号。
评估、模型与 replay 的保存周期及恢复语义见[训练与推理](docs/TRAIN_INFERENCE.md)。

## 推理与导出

推理读取训练时保存的机器人配置。Tracking 应选择匹配的完整动作，三种机器人使用相同入口：

```bash
./run_inference.sh tracking --model-folder runs/astro_fb \
  --data-path ufo/data/robots/astro_p2/motions/lafan/astro_lafan_29dof.pkl \
  --motion-list 0 --save-mp4
./run_inference.sh tracking --model-folder runs/g1_fb \
  --data-path ufo/data/lafan_29dof.pkl --motion-list 0 --save-mp4
./run_inference.sh tracking --model-folder runs/rp1_fb \
  --data-path ufo/data/rp1_24dof_lafan_v7.pkl --motion-list 0 --save-mp4
```

Tracking／ONNX 导出需要对应机器人训练好的 checkpoint；资产迁移本身不产生已训练的 Astro 策略。
FB 的 reward 推理需要保存的 rank-0 replay，非 G1 当前支持根节点运动与移动类任务；
非 G1 的 goal 推理需要机器人专属 goal JSON。
完整命令见[训练、推理与导出](docs/TRAIN_INFERENCE.md)，或执行
`./run_inference.sh <tracking|reward|goal> --help`。

<details>
<summary>使用已发布的 G1 FB 模型</summary>

```bash
uv run hf download xuewang/ufo-g1-policy --local-dir model
./run_inference.sh tracking --model-folder model/g1_policy \
  --data-path ufo/data/lafan_29dof.pkl --motion-list 7 --save-mp4
```

发布包包含约 1.92 亿步的策略、ONNX 和配套 z，不含优化器状态／replay。
重新计算 reward z 需要自行保存的 replay。

</details>

## 更多文档

- [训练与推理](docs/TRAIN_INFERENCE.md)：调度、评估、checkpoint 和推理参数。
- [Astro 实际网络配置](docs/ASTRO_NETWORK.md)：层数、输入输出维度和对应源码。
- [Astro 资产与迁移](docs/ASTRO_MIGRATION.md)：服务器／VNC、数据重建和验证记录。
- [机器人与数据适配](docs/ROBOT_ADAPTATION.md)：自定义机器人与动作转换。
- [代码结构](docs/ARCHITECTURE.md) · [多卡排障](docs/MuitiGPU_TIPS.md)。
- [上游历史测速](docs/UPSTREAM_RESULTS.md)：H20 上的 G1/RP1 实验和完整统计口径。
- 真机部署：[G1](https://github.com/Roboparty/UFO/tree/deploy) · [RP1](https://github.com/Roboparty/roboparty_deploy)。

## 引用与许可

UFO 采用 [CC BY-NC 4.0](LICENSE) 许可，用于非商业研究。

```bibtex
@misc{ufo2026,
  author       = {{RoboParty Lab Team}},
  title        = {UFO: An Unsupervised Reinforcement Learning Framework for Humanoid Control},
  year         = {2026},
  howpublished = {\url{https://github.com/Roboparty/UFO}},
  note         = {Project page: \url{https://roboparty.github.io/UFO/}}
}
```
