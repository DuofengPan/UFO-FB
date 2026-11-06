# Upstream training results / 上游历史实验

Archived from the upstream README at `4f1a6f6`. These are upstream G1/RP1
experiments, not measurements of this fork's Astro configuration.

## English

**2026-10-15 — Training performance and multi-robot update**

**192M-step FB / mjlab training:** all runs below use **8 × NVIDIA H20**, **BF16 mixed precision**, and **1024-wide networks with shared critics**.

| Experiment | Global training FPS | Last EMD ↓ | Time to 192M steps |
| --- | ---: | ---: | ---: |
| G1: original DR + original reward | **12,440** | **0.6655** | **4 h 45 min** |
| G1: extended DR + original reward | **12,467** | **0.7406** | **≈4 h 51 min** |
| G1: extended DR + updated reward | **12,217** | **0.7554** | **4 h 55 min** |
| RP1: baseline | **12,485** | **0.7139** | **4 h 48 min** |

<details>
<summary>Measurement settings and scope</summary>

All runs use 1,024 environments and batch size 1,024 per GPU, six residual layers, and 16 agent updates per rollout step. FPS counts environment transitions across all eight GPUs and is the median of the last 20 logged intervals, not whole-job throughput.

All three G1 runs use LaFAN-40 and 30% lying-down initialization. The original-DR run predates the reset-boundary fix; the extended-DR/original-reward run includes it. These historical runs span code changes and are not a controlled DR/reward ablation. The updated reward replaces the undesired-contact penalty with a body-impact penalty, sets the slip penalty weight to -4, and adds a foot-stumble penalty with weight -2. RP1 uses common LaFAN-40 and no lying-down initialization. BF16 is an experiment override for G1; the current G1 FB default remains FP32 + TF32, while RP1 FB defaults to BF16.

EMD is the mean over the last periodic tracking evaluation: all three G1 runs at 188,981,248 steps (862 clips), RP1 at 190,054,400 steps (902 clips), rather than a new evaluation of the final checkpoint. Wall time includes startup, evaluation and checkpoint saving. Times use launcher start/end records, except for G1 extended DR + original reward: its time is estimated from launch to the completed final save because its launcher completion timestamp is unavailable. All runs completed 191,995,904 steps under the nominal 192M budget.

</details>

The release also replaces the legacy `humanoidverse` layout with `ufo`, unifies G1 / RP1 and FB / TeCH commands, fixes reset-boundary observations and contact-force direction, and provides robot-aware ONNX exports, RP1 data and a G1 policy tested on hardware. See [architecture](ARCHITECTURE.md) and [training/inference](TRAIN_INFERENCE.md).

## 中文

**2026-10-15 — 训练性能与双机器人支持更新**

**FB / mjlab 完整 1.92 亿步训练**：下列实验均使用 **8 × NVIDIA H20**、**BF16 混合精度**、**1024 宽度网络与共享 critic**。

| 实验 | 全卡训练 FPS | 最后一次 EMD ↓ | 完成 1.92 亿步耗时 |
| --- | ---: | ---: | ---: |
| G1：原 DR＋原 reward | **12,440** | **0.6655** | **4 小时 45 分** |
| G1：扩展域随机化＋原 reward | **12,467** | **0.7406** | **约 4 小时 51 分** |
| G1：扩展域随机化＋新 reward | **12,217** | **0.7554** | **4 小时 55 分** |
| RP1：基准配置 | **12,485** | **0.7139** | **4 小时 48 分** |

<details>
<summary>测速配置与统计口径</summary>

各组均为每卡 1,024 个环境、batch size 1,024、六层残差主干，每次 rollout step 执行 16 次 agent 更新。FPS 表示八张卡合计的环境 transition 数／秒，取最后 20 条 FPS 日志的中位数，不代表包含全部开销的整场平均速度。

三组 G1 均使用 LaFAN-40 和 30% 躺倒初始化。原 DR 实验使用 reset 边界修复前的代码，“扩展域随机化＋原 reward”实验已包含该修复。这些历史实验跨越代码修改，不能视为仅改变 DR／reward 的严格对照。新 reward 将非期望接触惩罚替换为身体冲击惩罚，滑移惩罚权重改为 -4，并新增权重为 -2 的脚部绊倒惩罚。RP1 使用共同 LaFAN-40、关闭躺倒初始化。G1 的 BF16 为实验覆盖设置，当前 G1 FB 默认仍为 FP32＋TF32，RP1 FB 默认 BF16。

EMD 取最后一次周期跟踪评估的片段均值：三组 G1 均在 188,981,248 步评估 862 个片段，RP1 在 190,054,400 步评估 902 个片段，并非对最终 checkpoint 重新评估。总耗时包含启动、评估与 checkpoint 保存；除“G1：扩展域随机化＋原 reward”因缺少启动器结束时间、以启动至最终保存完成估算外，其余实验均使用启动器的起止记录。各组在名义 1.92 亿步预算下实际完成 191,995,904 步。

</details>

本次发布还将旧 `humanoidverse` 结构整理为 `ufo`，统一 G1／RP1、FB／TeCH 命令，修复 reset 边界观测与接触力方向，并提供机器人配置感知的 ONNX 导出、RP1 数据及已完成真机测试的 G1 policy。详见[代码结构](ARCHITECTURE.md)和[训练与推理](TRAIN_INFERENCE.md)。
