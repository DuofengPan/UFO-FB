# BONES-SEED G1 · 600条精选

- `g1_curated600_full.pkl`：600条完整动作，120 Hz，29关节，用于推理/评估。
- `g1_curated600_10s.pkl`：714个不超过10秒的训练片段，每条完整动作均有覆盖。
- `selected.json` / `DATA_LIST.md`：保留的数据ID、说明、原始CSV相对路径及哈希，便于人工筛查。
- `summary.json` / `REDUCTION.md`：从1,000条减至600条的规则和类别统计。
- `conversion_report.json` / `dataset_validation.json`：转换FK、逐帧一致性、实际MotionLib加载的历史证据。

两个 PKL 均通过 Git LFS 随代码版本管理，训练无需访问外部CSV。默认与LaFAN按
70% / 30%来源权重混合，配置见 `configs/data/g1_lafan_bones_seed.yaml`。
单源对照见 `configs/data/g1_bones_seed_600.yaml`。

来源为 [BONES-SEED](https://huggingface.co/datasets/bones-studio/seed) 已重定向的G1数据。
直接转换单位与根旋转约定，不重复重定向、不重采样、不夹紧关节或修正高度。
约73.91分钟、248个命名动作家族；保留前次人工查看的50条，不依据官方actor的
37通过/13未通过标签删动作。完整600条不丢帧，训练分段累计舍弃不足1秒的尾段
1,186帧（约9.88秒）。数据仍沿用上游数据集的使用条款和来源要求。

历史报告中的绝对路径记录当时的运行位置；当前统一入口是本目录的PKL和项目根下
的配置。原始CSV在 `.22:/data/atom9/datasets/bones-seed/` 保留，不纳入本次Git交付。
重新转换使用 `python -m ufo.tools.bones_motion_import`，详见 `docs/BONES_SEED.md`。
