# Astro FB：实际生效的网络层数

适用于本分支的 Astro FB 配置与 `start_astro_high_dynamic_5090_8gpu.sh`。
这里描述启动配置解析后实际构建的网络；当前没有因此启动训练。

**`hidden_layers: 6` 是残差主干的深度，不是包含 embedding、输出层在内的总层数。**
以下按 Linear / DenseParallel 计算线性层，不把 LayerNorm、激活函数和归一化另算为隐藏层。
本实现的每个 ResidualBlock 含一个线性层；路径深度沿残差块的变换支路计数。

## 配置与实现在哪里

- [Astro 主配置](../configs/robots/astro_p2_29dof.yaml)：`training.fb_agent_overrides.model.archi`。
- [配置合并](../ufo/agents/fb_cpr_aux/config.py)：`build_fb_agent()` 先读取默认值，再合并机器人覆盖值，最后应用显式的 CLI 网络宽度／共享 Critic 选择。
- [实际网络构造](../ufo/agents/common/networks.py)：`ResidualActor`、`ResidualForwardMap`、`BackwardMap`、`Discriminator`。
- [模型装配](../ufo/agents/fb_cpr_aux/model.py)：`FBcprAuxModel.__init__()`，分别构建 `_critic` 和 `_aux_critic`。
- [5090 启动配置](../scripts/start_astro_high_dynamic_5090_8gpu.sh)：显式传入 `--network-width 2048 --no-shared-critic`。

服务器仓库根目录是 `/data/atom9/code/UFO-next`，容器内是 `/root/code/UFO-next`。
通用 FB 默认配置中的 1024 宽度／SharedCritic 不代表 Astro 的最终配置。

## Actor

配置：`archi.actor.hidden_dim=2048`、`hidden_layers=6`、`embedding_layers=2`。
实现：`ResidualActor`。

```text
观测 465 维 ────────── 2 层 embedding ── 1024 维 ┐
观测 465 + z 256 维 ── 2 层 embedding ── 1024 维 ┘
                       拼接 2048 维 → 6 个残差块 → 输出 29 维动作
```

两条 embedding 分支各为 `输入 → 2048 → 1024`。汇合后主干为 6 个宽度 2048 的残差块，
最后一层映射到 29 维并应用 Tanh。

- 单条输入分支到输出的路径：`2 + 6 + 1 = 9` 个线性层。
- 两条分支和主干合计：`2×2 + 6 + 1 = 11` 个线性模块；它们不是顺序串联的 11 层。

## Forward

配置：`archi.f.hidden_dim=2048`、`hidden_layers=6`、`num_parallel=2`。
实现：`ResidualForwardMap`。

```text
观测 928 + z 256 维 ───── 6 层 embedding ── 1024 维 ┐
观测 928 + 动作 29 维 ─── 6 层 embedding ── 1024 维 ┘
                          拼接 2048 维 → 6 个残差块 → 输出 256 维
```

每条 embedding 分支内部为：输入 Block、4 个残差块、输出 Block，共 6 个线性层，
其中最后一个 Block 将宽度从 2048 降到 1024。

- 每个 ensemble 成员的单条输入路径：`6 + 6 + 1 = 13` 个线性层。
- 两条分支与主干合计：`6×2 + 6 + 1 = 19` 个线性模块，其中共有 14 个残差块（两条 embedding 各 4 个，加主干 6 个）。
- 共有 2 个 ensemble 成员，通过 DenseParallel 批量计算。

**这里 embedding 深度直接使用 `cfg.hidden_layers`。** 所以将 Forward 的
`hidden_layers` 从 6 改成其他值，会同时改变 embedding 和主干深度；新版没有独立的
Forward `embedding_layers` 配置。旧版残差 Forward 的实际行为也是如此。

## Critic 与 Aux Critic

配置：两者都使用 `archi.critic`，即宽度 2048、`hidden_layers=6`、`num_parallel=2`。
`archi.shared_critic=false`。

两组网络都使用 `ResidualForwardMap`：**每条 embedding 分支 6 层 → 主干 6 个残差块 → 1 维输出**。
每个成员的单路径深度为 13 个线性层，两条分支加主干合计 19 个线性模块。

- `_critic`：判别器奖励对应的 Q，含 2 个 ensemble 成员。
- `_aux_critic`：辅助奖励对应的 Q，另含 2 个 ensemble 成员。

两组网络分别实例化，参数互不共享。没有独立的 `archi.aux_critic` 字段；辅助 Critic
从同一份 Critic 架构配置另建一组。不是启用了 SharedCritic。

## Backward

配置：`archi.b.hidden_dim=256`、`hidden_layers=1`、`norm=true`。
实现：`BackwardMap`。

```text
观测 527 维 → Linear 256 + LayerNorm + Tanh → Linear 256 → 归一化
```

即 **1 个隐藏层 + 1 个输出层，总共 2 个线性层**，输出 latent 的维度为 256。

## Discriminator

配置：`archi.discriminator.hidden_dim=1024`、`hidden_layers=3`。
实现：`Discriminator`。

```text
观测 527 + z 256 维 → 1024 → 1024 → 1024 → 1
```

即 **3 个隐藏层 + 1 个输出层，总共 4 个线性层**。首个隐藏层使用 LayerNorm/Tanh，
后两个隐藏层使用 ReLU；logit 可转换为判别概率／奖励。

## 其余实际配置

- `z_dim=256`，`norm_z=true`。
- 观测字段：`state=64`、`privileged_state=463`、`last_action=29`、`history_actor=372`。
- Actor 使用 state / last_action / history_actor，共 465 维；Forward 和 Critic 另加 privileged_state，共 928 维。
- Backward / Discriminator 使用 state / privileged_state，共 527 维。
- `train.use_bf16_amp=false`；参数为 FP32，训练的高精度矩阵乘策略允许 TF32。
- 训练时创建的 target Forward、Backward、Critic、Aux Critic 与对应网络同构，不增加单个网络的层数。

层数已通过实际构造的模块统计核对，网络参数名与尺寸已与旧代码及旧 checkpoint 的结构头比对一致。
该说明不代表已完成八卡训练或长跑稳定性验证。
