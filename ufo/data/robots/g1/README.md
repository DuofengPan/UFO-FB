# Unitree G1 · 29 DoF

本目录沿用原有 G1 本体，不另建机器人副本。

```text
g1/
├── g1_29dof.xml                 # MuJoCo 机器人描述
├── meshes/                     # 原有机器人网格
├── goal_frames_lafan29dof.json  # 仅适用于 LaFAN 完整40条的目标帧索引
└── motions/
    ├── .gitattributes          # PKL 通过 Git LFS 版本管理
    ├── manifest.json           # 四个数据文件的来源、计数、SHA-256
    ├── validation.json         # 本次实际加载及来源采样验证
    ├── lafan/                 # 40条完整动作 + 862个10秒训练片段
    └── bones_seed/            # 600条完整动作 + 714个训练片段、筛选清单
```

机器人配置：`configs/robots/g1_29dof.yaml`。默认训练数据配置：
`configs/data/g1_lafan_bones_seed.yaml`，LaFAN / BONES-SEED 来源采样权重 **70% / 30%**。
来源内部仍按现有优先级调整；不按两个数据集的动作条数或帧数分配权重。
有限批次按整数配额取整，统计比例接近7:3。

在项目根目录执行：

```bash
git lfs install
git lfs pull
# 新训练示例，执行后才会启动训练；请使用新的工作目录并按机器配置资源参数。
./run_train.sh --robot g1 --agent fb \
  --data-manifest configs/data/g1_lafan_bones_seed.yaml \
  --gpu-ids all --work-dir runs/g1_lafan_bones_70_30
```

不指定数据时，G1 CLI 训练也使用上述混合清单；显式 `--data-path` 或
`--data-manifest` 可以覆盖。LaFAN 单源对照直接指定其训练 PKL；BONES 单源对照
用 `configs/data/g1_bones_seed_600.yaml`。RP1 和 Astro 的默认数据配置未变。

Git LFS 保存四个真实 PKL，克隆时需安装 LFS 并拉取对象，不能把约130字节的
指针当成数据。无需依赖 `.22` 的外部 datasets 目录；那里保留的原始CSV仅用于
追溯/重新筛选，不是训练依赖。未加入模型权重、replay buffer 或本地运行日志。

LaFAN 下载脚本仍可独立补齐并校验官方原文件：`bash scripts/download_data.sh g1_lafan`。
筛选、转换和官方模型闭环基线说明见 `docs/BONES_SEED.md`。
