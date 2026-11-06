# 此文档仅供参考.
# 当多卡训练出现问题时，可参考设置，但是不可以盲从！下面给出三种提示：
# 提示一：之前的故障记录。

本次故障排查主要涉及 **NCCL 通信路径、cuMem host 分配和非阻塞通信器卡死**。下面只总结启动环境，不规定训练任务或环境数量。

**这台 5090 的基础设置：**

```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export NCCL_P2P_DISABLE=1
export NCCL_CUMEM_HOST_ENABLE=0
export TORCH_NCCL_USE_COMM_NONBLOCKING=0
```

| 变量 | 对应之前的问题 |
|---|---|
| `CUDA_DEVICE_ORDER=PCI_BUS_ID` | 固定GPU枚举顺序，避免设备编号不一致 |
| `NCCL_P2P_DISABLE=1` | 禁用这套环境下有问题的P2P通信路径 |
| `NCCL_CUMEM_HOST_ENABLE=0` | 避开多NUMA/Docker下首次集合通信卡住的问题 |
| `TORCH_NCCL_USE_COMM_NONBLOCKING=0` | 避开此前PyTorch/NCCL非阻塞通信器随机卡死 |

**最容易配错的是 SHM，要按 GPU 数量设置，不是按4K/8K环境数：**

```bash
# 恰好两张GPU：关闭SHM
export NCCL_SHM_DISABLE=1

# 四张及以上GPU：保留SHM
export NCCL_SHM_DISABLE=0
```

你之前双卡 AMP terrain + VAE 验证需要关闭 SHM；四卡却需要保留。**不要让四卡任务继承双卡留下的 `NCCL_SHM_DISABLE=1`**，代码的 `setdefault` 不会纠正已有值。三卡没有单独验证。

如果要复现之前排查“跑几轮后卡住、600秒 watchdog 退出”时的附加设置：

```bash
export NCCL_ALGO=Ring
export NCCL_PROTO=Simple
export NCCL_DEBUG=INFO
export TORCH_DISTRIBUTED_DEBUG=DETAIL
```

这里要区分：**Ring + Simple 曾通过独立通信测试，但实际训练仍卡过；DEBUG 两项用于诊断，并非已证明的修复。** 它们不能保证中途不再退出。

5090 容器的 Python/Isaac 环境还需要：

```bash
source /root/miniforge3/etc/profile.d/conda.sh
conda activate isaaclab
source /root/isaacsim/setup_conda_env.sh
export ENV_SETUP=/root/isaacsim/setup_conda_env.sh
```

另外两点已经由项目入口处理：每个 worker 只看自己的GPU；先创建 PhysX 环境，再初始化 NCCL。不要另行提前初始化通信器。机器人直接加载预转换 USD，避免多进程同时转换资产。

这些是**你这套5090环境的历史配置与经验**，其他机器需结合其驱动、PyTorch/NCCL版本验证，不能当作所有多卡机器的通用参数。

# 提示二：之前的有效变量设定1（视情况）

CUDA_DEVICE_ORDER=PCI_BUS_ID
CUDA_VISIBLE_DEVICES=0,1  # 按对应卡组调整
NCCL_P2P_DISABLE=1
NCCL_SHM_DISABLE=1
NCCL_CUMEM_HOST_ENABLE=0
TORCH_NCCL_USE_COMM_NONBLOCKING=0
TORCH_NCCL_ASYNC_ERROR_HANDLING=1
OMP_NUM_THREADS=1

# 提示三：之前的有效变量设定2（视情况）
4卡以上NCCL_P2P_DISABLE=1
NCCL_SHM_DISABLE=0
NCCL_CUMEM_HOST_ENABLE=0
TORCH_NCCL_USE_COMM_NONBLOCKING=0
TORCH_NCCL_ASYNC_ERROR_HANDLING=1
OMP_NUM_THREADS=1
