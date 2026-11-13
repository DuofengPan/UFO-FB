# Astro 固定姿态负载适应实验

## 本轮研究问题

在原始 Goal z 能无负载原地保持的前提下，先确认负载使同一个 z 失稳，再固定 Actor、Backward、归一化器和控制器，只用 CEM 搜索一个新的固定 z，检验能否恢复同一姿态的原地稳定。既有模型、训练 motion 和原始 Goal 不覆盖。

当前代码以 `exp/astro-1024-shared-bf16` 的 `cd1a0e7` 为基线，开发在 `feat/astro-payload-cem`。模型为 no-backflips 的 0cui9p7l，191995904 步。原先六项高动态数据修改属于已有工作，不进入本实验提交。

## 代码边界

- `ufo/experiments/payload/cem.py`：无仿真依赖的球面局部 CEM；目标函数接口为候选矩阵 → 每个候选的有限分数。
- `physics.py`：刚性附加载荷，通过平行轴定理合成质量、质心和完整惯量；保持原有 joint/body 数和 Actor 观察合同。显示几何不碰撞，不模拟松动物体或手部抓取。
- `tasks.py`：Astro 专用固定关节目标，FK 对齐脚底。没有改写任何训练 motion 帧或速度。
- `policy.py`：从完整 checkpoint 严格加载 Actor/Backward/归一化器，只推理，校验前后 state_dict 指纹。
- `rollout.py`：确定性批量闭环及姿态/稳定性指标，失败 sticky mask，全时长计分，不自动重置。
- `run.py`：命令行及写一次的原始 z 归档。原始 z 已存在时，检验归档哈希并复用原始数值，不因负载或批量大小重新编码。
- `report.py`：直接从逐种子 JSON 生成可离线打开的 HTML、CSV 和嵌入数据，无 CDN 或服务端依赖。

## 主实验与预检分开

初始预检六项：自然站立、双臂前举、浅蹲、中蹲、左/右单腿。后三项无负载就存在持续位移或支撑不稳，不能用来证明负载适应，因此从主实验排除，保留为诊断记录。

主实验只使用前三项。预筛先用种子 0/11、15 秒验证无负载，再测试 4/6 kg 近躯干负载、前向 12 cm 和更明显的偏心条件。前三项原 z 在 0–6 kg 近躯干及前向 12 cm 范围仍稳定，不把这些条件称为“负载后失稳”。

统一主负载确定为 **8 kg、waist_roll_link 局部坐标 [0.30, 0, 0.10] m、长方体尺寸 [0.16,0.12,0.12] m**。机器人原质量约 40.582583 kg。该负载让三个原始 z 都出现明显持续位移。负载选择只依据预筛种子，不使用正式验证结果选条件。

四组：无负载 z0、有负载 z0、有负载 z*、无负载 z*。邻近负载验证复用同一个 z*，不重搜。不能将“原来就不稳定的目标被修好”混入负载适应结论。

## 搜索与验证

- z 维数256，归一化范数16，最大相对球面夹角0.55 rad。
- CEM 128候选、16精英、20代；共同初始扰动种子0/11；每次10秒。每代保留原始 z、历史最佳以及均值候选；导出实际评估过的最佳，而不是未经评估的最终均值。
- 正式验证30秒，种子101/202/303/404/505，关节初始扰动std=0.015 rad。统计5次结果，不等同于5次独立CEM搜索。
- 从相同 YAML 中立站姿出发，高度0.645 m，速度零，清空 history/last_action；关闭 DR、push、观察噪声。没有直接复位到目标。
- 成功需全程存活，扣除最初2秒后，超过90%帧同时满足：关节MAE<0.18 rad，高度差<0.07 m，关键body局部误差<0.10 m，位移<0.15 m，倾角<20°，双脚接触且无非脚接触。
- score 越高越好，代价明确包含目标姿态、位移、速度、脚滑、倾角、饱和、非脚接触及动作变化。终止后每一步计100，不重置刷分。姿态误差统计仅存活帧，必须和全时长hold一起看。

## 复现命令

在 `/data/UFO-next`，无需额外安装包。当前容器缺Python开发头，推理使用FP32 eager（`run.py`设TORCH_COMPILE_DISABLE=1），没有修改系统或编译训练代码。

```bash
source scripts/runtime_libraries.sh
ufo_use_project_nccl "$PWD"
export PYTHONDONTWRITEBYTECODE=1
RUN=runs/astro_fb_1024_shared_bf16_8gpu_no_backflips_20261110_183440
DATA=/data/model-comparison-20261111/selected_motions.pkl
OUT=/data/astro-payload-cem-20261113/main

# OUT/original 与 tasks.json 首次生成后保留。新实验不要复用已完成搜索的OUT。
.venv/bin/python -m ufo.experiments.payload.run --run "$RUN" --out "$OUT" --data "$DATA" \
  --phase baseline --mass 0 --task 0 1 2 --horizon 15 --seeds 0 11

# 每个task可用独立GPU；运行前先确认空闲GPU及容器进程数限制。
.venv/bin/python -m ufo.experiments.payload.run --run "$RUN" --out "$OUT" --data "$DATA" \
  --phase search --mass 8 --offset .3 0 .1 --task 0 \
  --population 128 --elites 16 --iterations 20 --horizon 10 --seeds 0 11 --device cuda:0
# task 1、2 相同参数，分别在 cuda:1、cuda:2。

# 相同候选数与环境数配对评估原始/CEM；无负载检查语义保留。
.venv/bin/python -m ufo.experiments.payload.run --run "$RUN" --out "$OUT" --data "$DATA" \
  --phase validate --mass 8 --offset .3 0 .1 --horizon 30 --seeds 101 202 303 404 505
.venv/bin/python -m ufo.experiments.payload.run --run "$RUN" --out "$OUT" --data "$DATA" \
  --phase validate --mass 0 --horizon 30 --seeds 101 202 303 404 505

.venv/bin/python -m pytest -q tests/test_payload_cem.py
.venv/bin/python -m ufo.experiments.payload.report "$OUT" /path/to/offline-report
```

`--data`只为沿用原模型所需的motion库和环境初始化，不用于搜索奖励或选择目标；可用合法的小型同构Astro motion文件替代。新服务器必须另行拿到原 checkpoint、robot assets、motion pickle，并核对hash；Git代码本身不包含这些大模型与数据。

## 交付边界

z 是一行256个有限浮点数的CSV，可复用当前部署 UFO-FB Goal 读取逻辑，不需要新Actor或Backward。它只对本轮已验证条件有证据。部署连续切Goal不清空history，与本轮独立复位实验不同；本轮结果不能替代 C++ sim2sim 或真机验收。真机不要直接加载超出硬件负重与结构安装能力的仿真配置。
