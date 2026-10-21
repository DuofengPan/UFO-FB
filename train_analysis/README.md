# UFO-FB 八卡训练分析产物

对应要求文档：`train_analisis-agent.md`  
主报告：[`UFO_FB_8GPU_Training_Report.md`](./UFO_FB_8GPU_Training_Report.md)

## 目标实验

- W&B Run：[`1ci2ojfy`](https://wandb.ai/1914708967-harbin-institute-of-technology/ufo-humanoid/runs/1ci2ojfy)（`ufo_fb_8gpu`）
- 硬件实测：**8× RTX 5090**（W&B tag `4090*8` 有误，报告内已纠正）
- 本地训练目录：`../runs/ufo_fb_8gpu/`

## 目录说明

| 路径 | 内容 |
| --- | --- |
| `UFO_FB_8GPU_Training_Report.md` | 完整中文训练与性能基线报告 |
| `data/` | 从 W&B / 日志导出的 JSON/CSV |
| `figures/` | 训练指标与 GPU 系统指标图 |

## 快速结论

- 状态：Finished，完成 191.74M / 192M 全局环境步，约 49.9 h，GPU-hours ≈ 399
- 平均吞吐 ≈ 1067 env-steps/s；八卡 util ≈ 97%，显存 ≈ 93%
- 已有 H200×2 草稿 Run `u1igc4kn`，但 buffer / 全局并行度不同，不能直接当同负载对比
