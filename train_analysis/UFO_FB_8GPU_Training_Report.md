# UFO-FB 八卡训练实验报告（性能基线）

- 目标 Run：`1ci2ojfy`（`ufo_fb_8gpu`）
- 报告生成目录：`UFO/train_analysis/`
- 主要数据来源：W&B API、本地 `runs/ufo_fb_8gpu/`、本地 `_wandb/wandb/run-20261013_014204-1ci2ojfy/`、容器内软件版本与 `nvidia-smi`/`lscpu`
- 原则：观测值 / 计算结果 / 估计值 / 推测分开标注；缺数据写明“未记录/数据不足”

---

## 1. 执行摘要

本次 UFO-FB（实际 agent：`FBcprAuxAgent`）在 **8× NVIDIA GeForce RTX 5090** 上完成接近满预算训练：

| 项目 | 结果 | 口径 |
| --- | --- | --- |
| 训练状态 | **Finished**（正常结束） | W&B `state=finished`；rank0 日志写明因达到全局采样预算主动停止 |
| 计划全局环境步 | 192,000,000 | Config `num_env_steps` |
| 实际完成全局环境步 | **191,741,952**（约 99.87%） | `train_log.txt` / W&B summary |
| 训练墙钟（训练 logger） | **49.91 h** | `train/duration [minutes]=2994.60` |
| W&B runtime | **49.975 h**（179910.4 s） | summary `_runtime` |
| 全程平均吞吐 | **约 1067 env-steps/s** | 终局步数 / logger 时长 |
| 窗口 FPS 中位数 | **1077.3** | `train_log` 的 `FPS` 列 |
| GPU-hours | **约 399.3** | `8 × 49.91 h` |
| 最终 checkpoint | `global_time=188,981,248` | 磁盘 `checkpoint/train_status.json`（略早于训练结束） |

**主要性能特征**

1. **八卡持续高占用且均衡**：稳定阶段 GPU utilization 均值约 **96.4%–97.0%**，显存 allocated 约 **93%**，功耗约 **188–214 W**（远低于 575 W 功耗墙）。
2. **吞吐非常平稳**：除首个日志点 FPS=1350 外，FPS 基本落在 955–1078，中后期均值约 1064–1065。
3. **算法侧**：`disc_loss` 快速下降后稳定；`Q_fb` 持续上升；`torso_z_mean` 从约 0.26 m 抬升并稳定在约 0.74 m，躯干接触比例明显下降。这是行为/辅助指标，**不能**直接等同于 tracking 任务分数——本次训练 **关闭了 online tracking eval**。
4. **重要纠正**：W&B tag 为 `4090*8`，但 metadata、Warp 日志与当前 `nvidia-smi` 均显示硬件为 **RTX 5090 × 8**。后续对比请以硬件实测为准，不要用 tag。

同项目内已存在 H200×2 Run `u1igc4kn`（可作对照草稿），但其 buffer / 全局并行环境数 / 有效 batch 与本基线不同，**不能直接当作同负载对比**。

---

## 2. 实验基本信息

### 2.1 选定主实验

| 字段 | 值 | 来源 |
| --- | --- | --- |
| Run 名称 | `ufo_fb_8gpu` | W&B |
| Run ID | `1ci2ojfy` | 用户指定；本地目录 `run-20261013_014204-1ci2ojfy` |
| Group | `ufo_fb` | W&B / config `wandb_gname` |
| Tags | `["4090*8"]`（**与硬件不符**） | W&B |
| Entity / Project | `1914708967-harbin-institute-of-technology` / `ufo-humanoid` | W&B API |
| URL | https://wandb.ai/1914708967-harbin-institute-of-technology/ufo-humanoid/runs/1ci2ojfy | W&B |
| 状态 | finished | W&B |

### 2.2 时间（UTC 与新加坡时间 UTC+8）

| 事件 | UTC | Asia/Singapore |
| --- | --- | --- |
| W&B created / startedAt | 2026-10-13 01:42:05Z | **2026-10-13 09:42:05 +08** |
| 训练进程启动（torchrunx 日志） | 2026-10-13 01:41:19 起 | 09:41:19 +08 |
| 最后一次 checkpoint | 约 2026-10-15 02:53:23（日志） / 文件 mtime 10:53–10:54（宿主机本地时区） | 见说明 |
| 训练主动停止 | 2026-10-15 03:40:34 | **11:40:34 +08** |
| W&B heartbeat / 结束附近 | 2026-10-15 03:40:40Z | **2026-10-15 11:40:40 +08** |

说明：容器日志时间为 UTC；宿主机文件 mtime 显示为本地时区（与 UTC+8 接近）。以 W&B UTC / 容器日志为准最稳妥。

总运行时长：

- W&B `_runtime`：179910.4 s ≈ **49.975 h**（观测值）
- 训练指标 `duration [minutes]`：2994.60 min ≈ **49.910 h**（观测值，训练 logger 累计）

二者高度一致，说明本次主 Run **没有明显的长时间挂起后继续记 runtime、但训练 logger 不走的情况**。

### 2.3 相关 Run 筛选（避免合并错误阶段）

| Run ID | 名称 | 创建时间 (UTC) | 状态 | 结论 |
| --- | --- | --- | --- | --- |
| `6e4eekpk` | ufo_fb_8gpu | 2026-10-12 08:18:23 | finished | **短启动/失败残留**，runtime≈9 s，无有效训练指标；同名但不是本基线 |
| **`1ci2ojfy`** | ufo_fb_8gpu | 2026-10-13 01:42:05 | finished | **主基线** |
| `u1igc4kn` | ufo_fb_2gpu | 2026-10-14 01:12:37 | finished | H200×2 对照候选；配置不同 |

本地 `runs/ufo_fb_8gpu/torchrunx/` 中还有 2026-10-12 多组短启动日志，对应早期调试，**不应并入本报告的时间线或吞吐统计**。

八卡验证依据（不仅看名字）：

1. Config / summary：`distributed_world_size=8`，`global_parallel_envs=8192`
2. Metadata：`gpu_count=8`，8 条 RTX 5090 UUID
3. Warp 日志枚举 `cuda:0`…`cuda:7`
4. System metrics 存在 `system.gpu.0`…`system.gpu.7`
5. Checkpoint buffers：`train_rank_0`…`train_rank_7`

---

## 3. 软硬件环境与多卡配置

### 3.1 硬件（已验证）

| 项目 | 值 | 来源 |
| --- | --- | --- |
| GPU | **NVIDIA GeForce RTX 5090 × 8** | W&B metadata、Warp 日志、`nvidia-smi` |
| 单卡显存 | 34190917632 B（W&B）≈ **31.85 GiB**；`nvidia-smi` 显示 32607 MiB | 观测 |
| 功耗上限 | **575 W / 卡** | `nvidia-smi power.limit` |
| CPU | **AMD EPYC 9654 96-Core × 2 socket** | `lscpu` |
| 逻辑 CPU | 192 核 / 384 线程；NUMA=2 | W&B metadata + `lscpu` |
| 系统内存 | 约 **1.0 TiB**（1081555980288 B） | W&B metadata / `free -h` |
| OS | Linux 5.15.0-198-generic，glibc 2.35 | W&B metadata |
| 主机名（容器） | `cf2aab823c85` | W&B / 日志 |
| GPU 互联 | Warp 日志：**CUDA peer access Not supported**；system 流中 nvlink 字节基本可视为无有效 NVLink 使用 | 观测 |
| PCIe | 有 `pcieRxBytes/pcieTxBytes` 系统指标 | 有记录，未做带宽标定 |

进程-GPU 映射：`torchrunx` 启动 8 worker；每 rank 使用 `cuda:{local_rank}`（rank0 日志 `device=cuda:0, rank=0/8`）。

### 3.2 软件（已验证）

| 项目 | 版本 / 值 | 来源 |
| --- | --- | --- |
| Python | CPython **3.10.22** | W&B metadata |
| PyTorch | **2.7.0+cu128** | 容器 `pip show` / import |
| CUDA（PyTorch 构建） | 12.8 | `torch.version.cuda` |
| 驱动侧 CUDA（Warp） | Toolkit 13.4，Driver 13.3 | 训练日志 |
| cuDNN | 90701 | `torch.backends.cudnn.version()` |
| mjlab | **1.4.0** | pip |
| mujoco / mujoco-warp | **3.8.1** | pip / import |
| warp-lang | **1.18.0** | 日志 / import |
| rsl-rl-lib | 5.2.0 | pip |
| wandb | 0.30.0 | run metadata |
| 仿真后端 | **MJLab + MuJoCo Warp**（非 Isaac Gym/Lab） | 代码与日志 |
| 分布式 | `torchrunx` 多进程 + `torch.distributed` NCCL；`loss_mode=local_loss_average` | config / summary |
| 代码仓库 | `https://github.com/Roboparty/UFO.git` | W&B git |
| Commit | `18693b13839c1295964306635c18c83c71dcc929` | W&B git |
| 分支（当前工作树） | 历史提交信息对应 FB-only 精简树；**训练当时工作区是否有未提交修改：未记录** | 局限 |

### 3.3 多卡启动事实

- 工作目录：`/root/code/UFO/runs/ufo_fb_8gpu`
- 数据：`humanoidverse/data/lafan_29dof_10s-clipped.pkl`
- `compile=False`（多卡默认关闭 compile）
- `buffer_device=cuda`，每卡 `buffer_size=2,500,000`
- 启动日志摘要：`num_envs_per_rank=1024, global_parallel_envs=8192, num_env_steps_global=192000000`

完整 CLI 一行未在 torchrunx 汇总日志中完整保存；上述参数来自 rank0 打印的 `[INFO] UFO train: ...` 与 W&B config（**已验证**）。

---

## 4. UFO-FB 训练参数与配置说明

实际 agent 名称：`FBcprAuxAgent` / `FBcprAuxModel`（CLI `--agent fb` 的 preset）。

### A. 算法参数（影响学习结果）

| 参数 | 值 |
| --- | --- |
| z_dim / norm_z | 256 / True |
| discount | 0.98 |
| seq_length | 8 |
| actor_std / stddev_clip | 0.05 / 0.3 |
| lr_f / lr_actor / lr_critic / lr_aux_critic | 3e-4 |
| lr_b / lr_discriminator | 1e-5 |
| fb_target_tau / critic_target_tau | 0.01 / 0.005 |
| ortho_coef | 100 |
| train_goal_ratio / expert_asm_ratio / relabel_ratio | 0.2 / 0.6 / 0.8 |
| reg_coeff / reg_coeff_aux | 0.05 / 0.02 |
| update_z_every_step | 100 |
| aux rewards | torques, action_rate, dof/torque limits, undesired contact, feet_ori, ankle_roll, slippage |
| seed | 4728（各 rank 为 seed+rank） |
| prioritization / evaluations | **False / []**（本次无 online tracking eval） |
| amp（混合精度） | False |
| q_loss_coef | 0 |

### B. 计算参数（影响显存/吞吐）

| 参数 | 值 | 备注 |
| --- | --- | --- |
| online_parallel_envs（每卡） | 1024 | |
| 全局并行环境 | 8192 | 8×1024 |
| batch_size（每卡） | 1024 | |
| effective_batch_size | 8192 | world_size 倍增记账 |
| buffer_size（每卡） | **2,500,000** | 小于默认 5.12M；放在 CUDA |
| use_trajectory_buffer | True | trajectory_steps_per_rank≈2441 |
| num_seed_steps | 10240（本地步） | |
| update_agent_every | 1024（本地步） | |
| num_agent_updates | 16 | 每次触发 16 次 optimizer update |
| compile / cudagraphs | False / False | |
| 物理步长 / 控制步长 | 0.005 s / 0.02 s | MJLab Base Environment 表 |
| 网络 | F/actor/critic/aux residual 2048×6；B 256×1；D 1024×3 | |

### C. 分布式参数

| 参数 | 值 |
| --- | --- |
| world_size | 8 |
| distributed_sync / average_metrics / global_steps | True |
| loss_mode | local_loss_average |
| checkpoint_rank_buffers | True（每卡独立 buffer 文件） |
| rank0_only_writes | True |

### 对后续 H200×2 公平对比的影响

必须对齐或显式归一化的项：

1. **全局并行环境数**（本基线 8192）与每卡 envs  
2. **buffer_size 与 buffer_device**（本基线每卡 2.5M @ CUDA；已有 H200 run 为每卡 5.12M）  
3. **effective batch / optimizer update 密度**（同样 `update_agent_every` 下，全局 env 更少会导致更多 local 步与更多 optimizer steps）  
4. **compile / AMP**  
5. **代码 commit**  
6. **是否开启 eval/prioritization**（本基线关闭）

---

## 5. 模型产物与路径

### 5.1 W&B

- Run URL：见第 2 节  
- Artifacts：run files 列表中仅有 `wandb_manifest.json` 占位；**未发现可用的模型 Artifact 实体文件**（数据不足：不能声称 W&B Artifact 中有可下载权重）

### 5.2 磁盘路径（已验证存在）

根目录：`/data/atom9/code/UFO/runs/ufo_fb_8gpu/`（容器内 `/root/code/UFO/runs/ufo_fb_8gpu/`）

| 路径 | 大小 / 说明 | 对应进度 |
| --- | --- | --- |
| `checkpoint/model/model.safetensors` | **3.15 GiB**（3384968272 B） | 与最后一次成功 checkpoint 一致 |
| `checkpoint/optimizers.pth` | **3.28 GiB** | 同上 |
| `checkpoint/train_status.json` | `global_time=188981248`, `optimizer_steps=368928` | **最新磁盘 checkpoint** |
| `checkpoint/distributed_sync.json` | 8 rank 参数校验和完全一致，`max_abs_diff_from_rank0=0.0` | 保存时同步健康 |
| `checkpoint/buffers/train_rank_{0..7}/buffer.hdf5` | 各约 12.09 GiB，合计约 **103.8 GB** | 每卡 replay |
| `exported/FBcprAuxModel.onnx` | 122 MB | 训练后导出（mtime 2026-10-15） |
| `exported/backward_encoder.onnx` | 802 KB | 同上 |
| `exported/FBcprAuxModel.meta.json` | z_dim=256, num_dof=29 等 | 已读 |

**最终训练步 vs checkpoint：** logger 最终 `191,741,952` 步；磁盘 checkpoint 停在 `188,981,248`（日志显示 02:53 左右的一次保存）。之后仍继续训练到预算截止，**但未再写新的完整 checkpoint**（或写盘未更新 train_status）。因此：

- “最终模型权重文件” = 最后一次落盘的 checkpoint（差约 2.76M 全局步）  
- “训练过程走到的最远步” = 191,741,952  

未在本报告中实际执行 `load()` 推理校验；仅确认文件存在、safetensors/onnx 体积合理、distributed sync 校验通过。**加载可运行性：未实测。**

### 5.3 易混淆文件

`humanoidverse_tracking_eval.csv` mtime 为 **2026-10-12 16:16**，早于本 Run 开始，且本 Run `evaluations=[]`。**该 CSV 不属于本次八卡正式训练的评估产物。**

---

## 6. 训练过程关键指标与收敛分析

数据：`runs/ufo_fb_8gpu/train_log.txt`（498 行，约每 385024 全局步一条；与 `log_every_updates≈384000` 一致）及 W&B history（498 points，已导出 `data/wandb_train_history.csv`）。

> 口径：下列 loss / Q 为优化目标相关量；**降低或升高并不自动等于任务变好**。本次无 tracking eval，行为侧主要参考 torso 高度与接触比例。

### 6.1 阶段划分（按日志三等分，计算结果）

| 阶段 | 全局步范围 | FPS 均值 | fb_loss 均值 | actor_loss 均值 | disc_loss 均值 | Q_fb 均值 | torso_z 均值 | 接触比例均值 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| early | 0.39M–63.9M | 1067.9 | -12098 | 23743 | 0.167 | 3387 | 0.699 | 0.164 |
| mid | 64.3M–127.8M | 1064.4 | -12363 | 50490 | 0.142 | 5336 | 0.736 | 0.080 |
| late | 128.2M–191.7M | 1064.5 | -12282 | 58730 | 0.140 | 5964 | 0.737 | 0.077 |

### 6.2 关键指标

#### `train/FPS`（窗口吞吐）

- 含义：训练代码在日志窗口内估算的环境步吞吐量（不是纯仿真内部 FPS）。  
- first/mid/last：1350.5 / ~1077 / 1077.3  
- min/max/mean/median：955.5 / 1350.5 / 1065.6 / 1077.3  
- 趋势：除起步偏高外长期平稳；偶发跌到 ~960（多与 checkpoint 时间邻近，**相关但未做因果证明**）。

#### `train/fb_loss`

- first→last：+10239.8 → -12297.6（首点后迅速转为大幅负值并稳定在约 -1.2e4）  
- 不宜解释为“越低越好”的任务分数；反映 FB 目标优化数值。

#### `train/actor_loss`

- first→last：-29.5 → 61505.8，持续上升  
- 与 `Q_fb` 增大、actor 目标 `-Q_fb - reg*Q_disc` 的符号结构一致（观测一致，机制为代码层面解释）。

#### `train/disc_loss` / `mean_disc_reward`

- disc_loss：0.694 → 0.137，快速下降后平台  
- mean_disc_reward：-1.60 → -5.65  
- 判别器很快进入稳定对抗区间。

#### `train/critic_loss` / `train/aux_critic_loss`

- critic 均值约 2.09，过程中有尖峰（最大约 10.3）但会回到 ~1.1  
- aux_critic 相对平稳（约 0.4–2.7）

#### `train/Q_fb` / `train/Q_discriminator`

- Q_fb：56.7 → 6192（单调抬升后缓增）  
- Q_discriminator：-4.0 → -190  

#### 行为代理指标

- `torso_z_mean`：0.26 → ~0.74 m（站立高度恢复）  
- `torso_contact_force_contact_frac`：0.62 → ~0.05（躯干触地变少）  
- 解释：更像“不再长期躺地/砸地”，**不是**官方 motion tracking 分数。

图表：`figures/train_*.png`。

---

## 7. GPU / CPU / 显存等资源使用

数据：W&B system stream，23990 点，导出为 `data/wandb_system_history.csv`。  
稳定段定义：`_runtime ∈ [600, max_runtime-600]` 秒（去掉首尾各 10 分钟），n≈23830。

### 7.1 每卡稳定段统计（观测值）

| GPU | Util 均值 / P95 (%) | memAllocated 均值 / max (%) | 功耗均值 (W) | 温度均值 / max (°C) | smActive 均值 | 全程显存峰值 (GB) |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 96.4 / 100 | 92.9 / 93.2 | 199 | 45 / 57 | 21.09 | 31.87 |
| 1 | 96.6 / 100 | 93.0 / 93.2 | 203 | 45 / 57 | 21.18 | 31.87 |
| 2 | 97.0 / 100 | 92.9 / 93.2 | 191 | 43 / 55 | 21.27 | 31.87 |
| 3 | 96.7 / 100 | 92.9 / 93.3 | 214 | 43 / 55 | 21.05 | 31.89 |
| 4 | 96.9 / 100 | 93.0 / 93.2 | 188 | 44 / 56 | 21.22 | 31.87 |
| 5 | 97.0 / 100 | 92.9 / 93.2 | 206 | 45 / 57 | 21.01 | 31.87 |
| 6 | 96.9 / 100 | 92.9 / 93.2 | 202 | 45 / 57 | 21.38 | 31.86 |
| 7 | 96.9 / 100 | 92.9 / 93.2 | 212 | 44 / 56 | 20.84 | 31.87 |

详细分位数见 `data/gpu_stats_stable.json`。图表见 `figures/gpu_*.png`。

解读要点：

1. **Util 高但功耗仅 ~200 W / 575 W**：GPU 时间片很满，却未顶满功耗墙；与仿真+大 buffer+同步等待的混合负载相符（机制推测，非根因证明）。  
2. **memAllocated ~93%，峰值 ~31.9 GB**：接近 32 GB 卡上限；与 CUDA replay buffer 2.5M/卡直接相关。  
3. **smActive ~21%**：与 ~97% util 并存，说明 “GPU busy” ≠ “Tensor Core/SM 算力打满”。  
4. 训练日志未出现 OOM；结合接近满显存，**余量很小**。

### 7.2 主机资源

| 指标 | 稳定段 | 说明 |
| --- | --- | --- |
| `system.cpu` | 均值 ≈ 0.523，几乎无波动 | W&B 原始值；**口径可疑**（若为 0–100% 则过低；若为比例则约 52%）。不作强结论。 |
| `system.proc.memory.rssMB` | 均值 ≈ 4853 MB（W&B 进程） | 仅 wandb/主进程视角，**不是** 8 个训练进程总 RSS |
| `system.disk./.usagePercent` | ≈ 7.3% | 根分区；大 buffer 写在数据盘路径，不代表 checkpoint 盘压力全貌 |

完整主机 1 TiB 内存在训练期仍有大量 free（当前空闲快照，不代表训练峰值）。**八个 rank 的进程级内存峰值：未记录。**

### 7.3 能耗（估计值）

对 8 卡 `powerWatts` 做梯形积分（间隙 >120 s 跳过）：

- 约 **2.908×10^8 J ≈ 80.8 kWh**（`data/energy_estimate.json`）  
- **不是**电表计量；仅供量级参考。

---

## 8. 八卡负载均衡与潜在瓶颈

### 8.1 均衡性结论（有证据）

1. **八卡持续工作**：util 均值全部 >96%，P95 均为 100%。  
2. **无明显掉队卡**：util / memAllocated 卡间差异很小。  
3. **显存高度均衡**：各卡 ~93%。  
4. **接近显存上限**：峰值 ~31.9 GB；若把 buffer 加回 5.12M/卡，在本机 5090 上此前已复现过 OOM 风险。  
5. **同步健康**：最后 checkpoint 的 `distributed_sync` 显示 8 rank 参数校验和一致。

### 8.2 瓶颈判断（区分证据与假设）

| 判断 | 性质 |
| --- | --- |
| 训练未因 OOM/NCCL 崩溃而失败，而是预算耗尽正常停 | **已验证** |
| 显存是首要约束之一（93%+） | **强证据** |
| 非功耗墙瓶颈（~200 W ≪ 575 W） | **强证据** |
| 无 NVLink / peer access，梯度同步走 PCIe/网络栈 | **已验证无 peer access**；对吞吐的定量影响未测 |
| FPS 平台期说明算法已收敛 | **推测**；缺少任务 eval |
| CPU/数据管线是主瓶颈 | **证据不足**（system.cpu 口径不清；无 per-stage profiling） |

---

## 9. 性能基线统计表（供 H200×2 对比）

### 9.1 整体效率（本 Run）

| 指标 | 数值 | 口径 |
| --- | --- | --- |
| GPU 数量 / 型号 | 8 / RTX 5090 32GB | metadata + nvidia-smi |
| 计划 env steps | 192,000,000 | config |
| 完成 env steps | 191,741,952 | train_log |
| 完成比例 | 99.87% | 计算 |
| 训练时长（logger） | 49.910 h | duration minutes |
| W&B runtime | 49.975 h | _runtime |
| 全程平均吞吐 | 1067.2 env-steps/s | steps/duration |
| FPS 中位数 / 均值 | 1077.3 / 1065.6 | train_log |
| 稳定段 FPS（mid/late） | ≈1064.4–1064.5 | 阶段均值 |
| Optimizer steps | 374,336 | 最终 logger |
| Effective batch | 8192 | summary |
| GPU-hours | **399.28** | 8 × 49.910 |
| Env-steps / GPU-hour | **4.802×10^5** | steps / GPU-hours |

JSON：`data/performance_baseline.json`。

### 9.2 单卡效率

| 指标 | 数值 |
| --- | --- |
| 平均单卡吞吐（总吞吐/8） | ≈133.4 env-steps/s/卡 |
| 单卡 util 均值 | ≈96.8% |
| 单卡显存占用 | ≈93% allocated |
| 卡间 util 极差 | <1 个百分点 |

### 9.3 达到相同进度的耗时（本硬件）

| 进度 | 约耗时（按 logger 线性外推/插值） |
| --- | --- |
| 64M steps（约 1/3） | ≈16.6 h |
| 128M steps（约 2/3） | ≈33.3 h |
| 192M steps（满预算） | ≈49.9 h |
| 每 3.2M steps（checkpoint 间隔） | ≈0.83 h |

### 9.4 稳定性

- 正常结束，无中途 crash 重启并入本 Run。  
- FPS 波动小（P05–P95：972–1078）。  
- 显存无“泄漏式”持续爬升到 OOM；开训后迅速升到 ~93% 平台。  
- Checkpoint 时刻 FPS 偶发下降到 ~960，随后恢复。

### 9.5 与已有 H200×2 Run 的草稿对照（配置不同！）

来源：`u1igc4kn` / `data/h200_run_u1igc4kn.json`

| 项 | 本基线 8×5090 | H200×2 (`u1igc4kn`) | 是否同负载 |
| --- | --- | --- | --- |
| GPU | 8×5090 32GB | 2×H200 | 否 |
| world_size | 8 | 2 | 否 |
| envs/卡 | 1024 | 1024 | 单卡同，全局不同 |
| 全局并行 envs | 8192 | 2048 | **否** |
| buffer/卡 | 2.5M | 5.12M | **否** |
| effective batch | 8192 | 2048 | **否** |
| 完成 steps | 191.74M | 191.86M | 接近 |
| logger 时长 | 49.91 h | **7.94 h** | — |
| 末窗 FPS | 1077 | 1215 | — |
| optimizer steps | 0.374M | **1.499M** | 因并行度不同预期会变 |
| W&B runtime | 49.98 h | 64.43 h | H200 runtime≫logger，**可能含空转/恢复，需另查** |
| GPU-hours（用 logger） | 399.3 | 15.9 | 不可直接比效率 |
| Env-steps/GPU-hour（logger） | 4.80e5 | ≈1.21e7 | 配置不同，只作量级观察 |

---

## 10. 面向 H200×2 的公平对比方案

### 10.1 第一类：相同工作负载下的硬件效率比较（推荐主实验）

尽量固定：

- 同一 git commit（建议钉死 `18693b13…` 或后续明确 commit）  
- 同一 `FBcprAux` 超参与网络  
- 同一数据 pkl  
- **全局并行环境数 = 8192**（例如 H200×2 时每卡 4096，或保持每卡 1024 但承认全局不同并改用归一化——前者更接近同负载）  
- 每卡 batch=1024，`update_agent_every`/`num_agent_updates`/`num_seed_steps` 一致  
- buffer：**先对齐 2.5M/卡 @ CUDA**；若 H200 显存允许再单开“放大 buffer”实验  
- `compile=False`，`amp=False`  
- 关闭或同样关闭 online eval  
- 同一 `num_env_steps=192e6`

**主指标**

1. 完成 192M 全局 env steps 的墙钟时间  
2. 稳定段平均 FPS（env-steps/s）  
3. Env-steps / GPU-hour  
4. 稳定段 GPU util / memAllocated / power  

**辅助指标**

5. Optimizer steps 总数（用于检查更新密度是否被配置改变）  
6. 卡间 util/显存均衡  
7. 若开启 eval：tracking EMD / MPJPE（本次基线无）  
8. 训练稳定性（是否 OOM、是否重启）

### 10.2 第二类：各自硬件最优配置下的实际训练性能

允许 H200 提高 envs/卡、buffer、batch 或打开 compile/AMP，但必须单列，并同时报告：

- 最终吞吐与 GPU-hours  
- 样本数 / 更新次数是否变化  
- 模型指标是否仍可对齐  

### 10.3 归一化建议

若无法做到相同全局并行度，至少同时报告：

- 全局 env-steps / 秒  
- 每卡 env-steps / 秒  
- optimizer-steps / 秒  
- 完成固定全局 env-steps 的时间  
- 完成固定 optimizer-steps 的时间  

避免只比较末条 `FPS` summary。

### 10.4 预填对比表

| 指标 | 8×RTX 5090（本基线） | 2×H200（待填/草稿） |
| --- | --- | --- |
| Run ID | `1ci2ojfy` | `u1igc4kn`（草稿，非同负载） / 正式对照待跑 |
| Commit | `18693b13…` | 待确认 |
| 全局 envs | 8192 | 草稿 2048；正式建议 8192 |
| buffer/卡 | 2.5M | 草稿 5.12M；正式建议先 2.5M |
| 完成 env steps | 191,741,952 | 草稿 191,864,832 |
| 训练时长 (h) | 49.910 | 草稿 logger 7.94（runtime 64.4 需核实） |
| 平均吞吐 (steps/s) | 1067.2 | 草稿末窗 FPS 1215 |
| GPU-hours | 399.3 | 草稿（logger）15.9 |
| steps / GPU-hour | 4.80e5 | 草稿 ~1.21e7（不可直接比） |
| GPU util 均值 | ~96.8% | 待采集 |
| 显存占用 | ~93% / ~31.9GB peak | 待采集 |
| 平均功耗/卡 | ~200 W | 待采集 |
| 任务指标 | 无 online tracking eval | 待定 |
| 是否正常结束 | 是 | 草稿 finished |

---

## 11. 数据缺失、局限与待核实

1. W&B tag `4090*8` 错误，应以 5090 为准。  
2. 无 online tracking/goal/reward eval；`humanoidverse_tracking_eval.csv` 不属于本 Run。  
3. 最终权重文件落后最终步数约 2.76M global steps。  
4. 未实测 `load()` / 推理正确性。  
5. W&B 无实质模型 Artifact。  
6. `system.cpu` 数值口径不清。  
7. 缺少 8 个训练进程各自 RSS/峰值内存。  
8. 无 NCCL 详细 timeline / kernel profiler。  
9. 完整 CLI 一行未完整落盘。  
10. 训练时 git 是否 dirty：未记录。  
11. H200 Run 的 `_runtime` 与 `duration` 严重不一致，正式对比前必须核查是否 resume/空转。  
12. 能耗为功率积分估计，非电表值。

补采建议：同配置短跑开启 W&B 时记录 `nvidia-smi dmon`；H200 对照固定 commit 与全局 envs；结束后强制最终 checkpoint；必要时打开 tracking eval 但单独统计其对吞吐影响。

---

## 12. 附录

### 12.1 本目录结构

```
train_analysis/
  train_analisis-agent.md          # 原始分析要求
  UFO_FB_8GPU_Training_Report.md   # 本报告
  data/
    run_identity.json
    related_runs.json
    performance_baseline.json
    gpu_stats_stable.json
    host_stats_stable.json
    energy_estimate.json
    h200_run_u1igc4kn.json
    wandb_train_history.csv
    wandb_system_history.csv
    wandb_system_metrics_summary.json
  figures/
    train_*.png
    gpu_*.png
```

### 12.2 关键 W&B 指标原名

训练：`train/FPS`, `train/fb_loss`, `train/actor_loss`, `train/disc_loss`, `train/critic_loss`, `train/aux_critic_loss`, `train/Q_fb`, `train/Q_discriminator`, `train/mean_disc_reward`, `train/mean_aux_reward`, `train/torso_z_mean`, `train/torso_contact_force_contact_frac`, `train/distributed/*`, `train/duration [minutes]`

系统：`system.gpu.{0-7}.gpu|memoryAllocated|memoryAllocatedBytes|powerWatts|temp|smActive|pcie*|nvlink*`，`system.cpu`，`system.proc.memory.rssMB`

### 12.3 关键计算口径

- GPU-hours = `world_size × (duration_minutes/60)`  
- 平均吞吐 = `final_global_env_steps / (duration_minutes×60)`  
- 稳定段系统统计：去掉首尾各 600 s  
- 能耗：∑_gpu ∫ P(t) dt，梯形法，Δt>120s 跳过  

### 12.4 来源链接

- W&B Run：https://wandb.ai/1914708967-harbin-institute-of-technology/ufo-humanoid/runs/1ci2ojfy  
- 本地工作目录：`/data/atom9/code/UFO/runs/ufo_fb_8gpu/`  
- 本地 W&B run dir：`/data/atom9/code/UFO/_wandb/wandb/run-20261013_014204-1ci2ojfy/`  
- Git commit：`18693b13839c1295964306635c18c83c71dcc929`
