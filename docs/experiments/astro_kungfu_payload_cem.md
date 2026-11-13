# 功夫稳定 Goal：负载 CEM 实验

## 结果与边界

四个原始 z 无负载正式验证均5/5，通过预先固定主负载后均0/5，CEM后四项带载均5/5，最后一秒保持比例均100%。每项只有一次CEM搜索，5次是不同初始扰动验证，不是总体功夫动作成功率。

卸载后的优化z，只有南拳5/5，其余三项0/5。长拳在1kg邻近负载4/5，保留seed303失败。虎拳优化后全程均值左右膝约1.66/0.99rad，末帧约1.706/0.691rad、更偏弓步，只能声称预设低蹲条件恢复，不能称为标准对称深蹲。洪拳带载一次最大位移0.166m，短暂超过逐帧0.15m门槛但整体未达标时间不足10%；末秒保持均100%。

## 原始姿态筛选

70个功夫pickle，约6Hz抽帧，左右单腿与低蹲各设独立配额：355个几何候选（左83、右80、低蹲192）。不再把源动作低关节速度当成固定Goal的必要条件；没有修改源motion或速度。

无负载10秒、0/11共33个通过，同一原z30秒复验31个通过（左2、右1、低蹲28）。四个选例在0/11/23/37/59无负载30秒均5/5。负载选择只用0/11，正式101/202/303/404/505未用于选择目标、负载或搜索。

源帧保留原始关节角与根roll/pitch，去除世界平移/yaw、按脚底对齐地面。tasks.json记录源文件SHA256、零基帧、FPS、时间、36维qpos。低蹲源几何要求双膝各≥1.0rad、均角≥1.2、差≤0.6、root≤0.50m；并以闭环验证而非源几何判断稳定。

固定主负载（均刚性附加于waist_roll_link，尺寸[.16,.12,.12]m，完整合成质量/质心/惯量）：

- task0洪拳02，frame1201，约17.157s，左腿；4kg、局部[0,-.20,.10]m；邻近3kg。
- task1长拳01，frame277，约3.957s，右腿；2kg、[0,0,.10]m；邻近1kg。
- task2南拳01，frame901，约12.871s，低蹲/深蹲；6kg、[.30,0,.10]m；邻近4kg。
- task3虎拳，frame685，约9.786s，低蹲；12kg、[.30,0,.10]m；邻近8kg。原z在8kg仍保持，12kg出现姿态/高度/漂移组合退化，不等于跌倒。

四项负载不同，不能据此排序统一最大负重能力；本实验不模拟手部抓持或松动物体。

## 模型与方法

开发分支feat/astro-payload-cem，本轮起点1368a9924de56a8872c0ec7021e7d2c7ac531356；原基线exp/astro-1024-shared-bf16的cd1a0e7。
模型run为astro_fb_1024_shared_bf16_8gpu_no_backflips_20261110_183440，ID0cui9p7l，191995904步。Actor/Backward/normalizer指纹2bba2e92ab160615119ce269d2796d594885b98637e5d64e67eef5af1122a6de。

- 固定256维z、范数16，球面CEM 128候选/16精英/20代，10秒共同种子0/11，sigma.18，最大夹角.55rad，与上一轮相同预算。邻近负载复用同一z，不重搜。
- A无负载原z、B主负载原z、C主负载优化z、D无负载优化z，加邻近负载原z/优化z：24组、120次、每次30秒。只统计本轮，不并入旧数据。
- 同批候选×共同种子，从YAML中立站姿开始，关节扰动std.015rad，清零速度/history/action，DR/push/观察噪声关闭。FP32 eager、Actor mean动作；GPU物理有小幅波动，非逐位确定性。
- 成功需全程存活，前2秒后超过90%帧同时满足：全关节MAE<.18rad、高度差<.07m、关键body根局部误差<.10m、位移<.15m、绝对倾角<.35rad、指定支撑且无非脚接触。单腿还要求另一脚无接触、脚高差>.07m。
- 两项低蹲在搜索和A/B/C/D共同追加root≤.50m、左右膝均角≥1.05rad，不是每个膝各≥1.05。报告分别给出左右膝角；不准通过站高、伸膝换稳定。
- 失败sticky、不自动reset，后续每步代价100。保持/支撑/深度比例使用去前2秒后全时段，失败余段计0；状态与误差均值仅按存活帧。成功允许不足10%帧未达标，因此另存终帧和末秒保持/支撑/深度；总体通过不保证终态。
- 搜索后补齐完整根状态/关节速度/body非有限检查及末秒诊断，保留此前验证，再以未修改的z重跑全部正式组。本报告只用重跑数据；阈值、代价和分母不变。15项单元检查通过。

## 复现入口

通用入口是ufo/experiments/payload/run.py新增的--tasks-json，以及PoseEvaluator的批量FK/Backward、支撑/蹲深和尾段诊断。没有重训Actor或新增训练算法。

在/data/UFO-next：

```bash
source scripts/runtime_libraries.sh
ufo_use_project_nccl "$PWD"
export PYTHONDONTWRITEBYTECODE=1
RUN=runs/astro_fb_1024_shared_bf16_8gpu_no_backflips_20261110_183440
DATA=/data/model-comparison-20261111/selected_motions.pkl
ARCHIVE=docs/experiments/astro_kungfu_payload_cem_20261113
TASKS=$ARCHIVE/tasks.json
OUT=/data/kungfu-payload-cem-reproduce
mkdir -p "$OUT/original"
cp "$ARCHIVE"/original/*.csv "$OUT/original/"
cp "$TASKS" "$OUT/tasks.json"

# 以task2南拳为例；其余用上方固定质量/位置/索引替换。
.venv/bin/python -m ufo.experiments.payload.run \
  --run "$RUN" --out "$OUT" --data "$DATA" --tasks-json "$TASKS" \
  --phase search --task 2 --mass 6 --offset .3 0 .1 \
  --population 128 --elites 16 --iterations 20 --horizon 10 --seeds 0 11 --device cuda:0
for mass in 0 6 4; do
  .venv/bin/python -m ufo.experiments.payload.run \
    --run "$RUN" --out "$OUT" --data "$DATA" --tasks-json "$TASKS" \
    --phase validate --task 2 --mass "$mass" --offset .3 0 .1 \
    --horizon 30 --seeds 101 202 303 404 505 --device cuda:0
done
.venv/bin/python -m pytest tests/test_payload_cem.py tests/test_payload_goals.py -q
```

DATA只为环境初始化，不是搜索奖励或目标选择数据。Git不含大checkpoint和70个源pkl；换服务器需另取相同模型/资产并核验哈希。原z严格保留归档CSV，切勿用重新编码的近似值替换。

## 交付边界

旧报告原三任务24组/120次、旧8项功夫筛选、旧模型/motion/goal均保留。新增区独立给出源帧、配对表、邻近负载、CEM曲线、尾段指标、所有失败种子和真实seed101带载视频。

本轮未修改或启动真机，也未覆盖活跃部署配置。证据为冻结Python策略+MuJoCo闭环，不等于C++ sim2sim或真机负载验收。
