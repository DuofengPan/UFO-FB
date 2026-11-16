# BONES-SEED G1 导入与基线评估

这套流程直接使用 BONES 已重定向的 G1 CSV，不经过 UMR，不重复重定向。转换入口为 `ufo.tools.bones_motion_import`；批量闭环评估和离线视频入口分别为 `ufo.tools.evaluate_motion_tracking`、`ufo.tools.render_tracking_samples`。

## 输入约定

- `Frame` 加 6 个根状态列及 29 个 `*_joint_dof` 关节列；按列名匹配，不依赖关节列顺序。
- 平移原单位 cm，转换为 m；根 Euler 与关节原单位 degree，转换为 rad。
- 根旋转为 **extrinsic XYZ**，即 `scipy.spatial.transform.Rotation.from_euler('xyz', ..., degrees=True)`。大写 `XYZ` 表示另一种约定，不能混用。
- 原始 120 Hz；不重采样、不平移根轨迹、不夹紧关节、不修正高度。MotionLib 在运行时按控制周期插值。
- 保留完整动作，并可额外生成 10 秒训练分段。尾段不足 1 秒时按现有通用分段规则舍弃；完整动作文件不丢帧。
- CLI 仅接受 `g1_29dof`。它复用 `RobotStateMotion → robot_state_to_ufo_motion`，并用 MuJoCo 与 UFO 两条 FK 路径比较每条最多 128 帧的身体位置和旋转。
- 遇到帧号跳变、重复/缺失列、非有限值、哈希不匹配、重复动作或已有输出，直接报错。关节越限仅记录；不在转换时悄悄改轨迹。

格式依据：NVIDIA [ProtoMotions SEED G1 preparation](https://github.com/NVlabs/ProtoMotions/blob/main/docs/source/getting_started/seed_g1_csv_preparation.rst) 和 [转换实现](https://github.com/NVlabs/ProtoMotions/blob/main/data/scripts/convert_g1_csv_to_proto.py)。

选择 JSON 是记录列表，每条至少包含 `id`、相对 `--root` 的 `selected_path`、源 CSV 的 `source_sha256`，可附 `frames`。`id` 是主键；不要把 CSV 文件名、metadata 的 content_name 或行号当作完全等价的标签，少量原始描述与文件名存在差异。

## 通用命令

在项目根目录及其 Python 环境内执行。将下面的 `/path/to/bones-seed` 换成实际可见的数据目录；不需要下载整个数据集第二次。

```bash
python -m ufo.tools.bones_motion_import \
  --manifest /path/to/bones-seed/pilot_50/selected.json \
  --root /path/to/bones-seed \
  --robot-config configs/robots/g1_29dof.yaml \
  --output /path/to/bones-seed/pilot_50/g1_pilot50.pkl \
  --train-output /path/to/bones-seed/pilot_50/g1_pilot50_10s.pkl \
  --report /path/to/bones-seed/pilot_50/conversion_report.json
```

扩大到 1,000 条时，改成 `refined_1000/selected.json` 并指定新的输出路径即可。默认 fps 为 120，只有确认来源帧率变化时才使用 `--source-fps`。

使用匹配的 G1 模型进行无物体跟踪，而不是重新训练：

```bash
python -m ufo.tools.evaluate_motion_tracking \
  --model-folder model/official_g1_bones_eval/g1_policy \
  --data-path /path/to/bones-seed/pilot_50/g1_pilot50.pkl \
  --robot-config configs/robots/g1_29dof.yaml \
  --output runs/bones_pilot50_evaluation --device cuda:0

python -m ufo.tools.render_tracking_samples \
  --evaluation runs/bones_pilot50_evaluation \
  --robot-config configs/robots/g1_29dof.yaml --per-group 2
```

评估将所有动作并行为独立环境，按各自长度计算指标，关闭 DR 与观测噪声，使用参考首帧位置、速度初始化和确定性动作。保存实际闭环 qpos 和参考 qpos；视频回放这些结果，不再重复推理。左右相机同时跟随参考根位置，使根位移偏差可见。编码优先使用 PATH 的 ffmpeg，否则复用已安装的 `imageio_ffmpeg`。

初筛阈值可以通过 `--mae-threshold`、`--body-threshold`、`--hand-threshold`、`--root-threshold` 修改。默认关节 MAE < 0.3 rad、去根平移的身体平均误差 < 0.15 m、手腕平均误差 < 0.2 m、全局根平均误差 < 0.3 m，且无启发式跌倒。跌倒定义为骨盆高度 < 0.25 m 或躯干倾角 > 80°持续至少 0.2 s。它们是本次数据初筛规则，并非官方 benchmark；未通过表示现有模型跟踪不足，不能直接证明动作物理不可行。均值按动作等权，不按帧数加权。

## .22 的本次数据与路径

主机：`atom9-22`（172.16.9.22），项目 `/data/atom9/code/UFO-next`，执行环境 `atom9-ufo-vnc` 容器的 `/root/code/UFO-next/.venv/bin/python`。

- 外部数据根：`/data/atom9/datasets/bones-seed`，位于 UMR 外。
- 最终清单与交付：`/data/atom9/datasets/bones-seed/pilot_50/`。
- 实际转换、评估输出：`/data/atom9/code/UFO-next/runs/bones_seed_g1_pilot50_20261116/`；容器内为 `/root/code/UFO-next/runs/bones_seed_g1_pilot50_20261116/`。
- 容器没有挂载外部 datasets，故本次 `runs/.../input/` 用硬链接桥接所选 CSV，不重复占用 CSV 数据空间；外部交付的 PKL/报告也与实际运行文件硬链接。
- 首轮筛选草稿在 `runs/.../draft_v1/`，最终结果只看顶层 `evaluation/results.json`。
- 官方模型发布仓库 `xuewang/ufo-g1-policy`，固定 revision `da3727034a058eae588a16af142764ee34bdada4`，权重 SHA-256 `cbc057a257fa9093bfbb1477212f44f360bf3349a58a7275aee2ea666a63b6b5`；下载记录在 `model/official_g1_bones_eval/download_provenance.json`。

50条阶段仅做官方模型基线验证，未启用训练。后续人工查看后保留全部50条，并扩充为下述600条训练精选。当前7:3混合配置已准备，尚未启动新训练。


## 全部 50 条视频网页

本地查看页：`http://127.0.0.1:8765/`（本机启动静态HTTP服务期间可用，不要求在线发布）。网页上方为37条通过项，分割线下方为13条待复核项，支持搜索、类别筛选和误差排序。

服务器网页副本：`/data/atom9/datasets/bones-seed/pilot_50/web/index.html`。全部视频：`evaluation/videos_all/`，对应清单：`evaluation/all_videos.json`，完整解码与哈希校验：`evaluation/all_media_validation.json`。

使用已有轨迹生成所有视频，无需重新仿真：

```bash
python -m ufo.tools.render_tracking_samples --evaluation runs/bones_seed_g1_pilot50_20261116/evaluation --robot-config configs/robots/g1_29dof.yaml --all --camera-azimuth 45
```

未加 `--all` 时仍按原规则生成六条代表视频，原六条视频保留。全量视频写入独立目录，已有视频不会被静默覆盖。


## 600 条训练精选集

2026-11-16 从原1,000条保留600条，约73.91分钟、248个命名家族，pilot 50条全部保留。按同名家族覆盖与时序特征相似度精简392条，另排除8条明确上箱/外力拉动等依赖或非目标运动；原始1,000条未删除。不按官方模型的通过/失败标签删训练动作。

- 外部数据主体：`/data/atom9/datasets/bones-seed/curated_600/`。
- 完整600条：`ufo/g1_curated600_full.pkl`。
- 训练714段：`ufo/g1_curated600_10s.pkl`。
- 项目内数据：`ufo/data/robots/g1/motions/bones_seed/`，PKL通过Git LFS随分支版本管理；克隆后 `git lfs pull` 即可。原始外部CSV保留用于追溯。
- 默认混合清单：`configs/data/g1_lafan_bones_seed.yaml`，LaFAN 70% / BONES-SEED 30%来源采样权重。G1 CLI未指定数据时也使用它；单源BONES对照清单 `configs/data/g1_bones_seed_600.yaml` 仍保留。训练资源、步数和新工作目录在正式启动前确定。
- 原始120 Hz保持，无重定向、无重采样。714段训练数据与原始转换轨迹逐帧一致，短于1秒的尾段按通用分段规则累计舍弃1,186帧（约9.88秒）；完整600条不丢帧，每条均有训练片段。
- 转换FK和含31个扩展身体的实际MotionLib加载、首中末采样检查均通过。见外部目录 `conversion_report.json`、`dataset_validation.json`。这一步未启动训练。

筛选脚本：外部数据根 `tools/curate_diverse.py`。重新转换仍用 `python -m ufo.tools.bones_motion_import`，将manifest换成 `curated_600/selected.json`。G1 LaFAN官方完整40条及862个训练片段已补齐至 `ufo/data/robots/g1/motions/lafan/`，与BONES两份PKL一起纳入Git LFS。机器人XML、meshes及motions统一在 `ufo/data/robots/g1/`；四文件哈希与实际来源采样验证见 `motions/manifest.json`、`motions/validation.json`。优先级只调整每个来源内部的动作概率，来源总权重仍为7:3；1024个精确配额样本取717/307，不代表每一帧或每次短随机采样都严格7:3。
