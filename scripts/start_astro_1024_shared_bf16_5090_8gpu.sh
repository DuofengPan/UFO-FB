#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
source "$ROOT_DIR/scripts/runtime_libraries.sh"
ufo_use_project_nccl "$ROOT_DIR"
PYTHON="${PYTHON:-${ROOT_DIR}/.venv/bin/python}"
RUN_NAME="${RUN_NAME:-astro_fb_1024_shared_bf16_5090_8gpu_formal_$(date +%Y%m%d_%H%M%S)}"
RUN_DIR="${ROOT_DIR}/runs/${RUN_NAME}"
dry_run=0
if [[ "${1:-}" == --dry-run && "$#" == 1 ]]; then
  dry_run=1
elif (( $# )); then
  echo 'Usage: bash scripts/start_astro_1024_shared_bf16_5090_8gpu.sh [--dry-run]' >&2
  exit 2
fi
[[ -x "$PYTHON" ]] || { echo "Missing interpreter: $PYTHON; run uv sync --locked --group dev" >&2; exit 1; }
[[ ! -e "$RUN_DIR" ]] || { echo "Run directory exists; choose a new RUN_NAME: $RUN_DIR" >&2; exit 1; }
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0,1,2,3,4,5,6,7}"
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export NCCL_P2P_DISABLE=1
export NCCL_SHM_DISABLE=0
export NCCL_CUMEM_HOST_ENABLE=0
export TORCH_NCCL_USE_COMM_NONBLOCKING=0
export TORCH_NCCL_ASYNC_ERROR_HANDLING=1
export NCCL_NVLS_ENABLE=0
export OMP_NUM_THREADS=1
export UFO_RELEASE_TORCH_CACHE_AFTER_UPDATES=1
export PYTHONUNBUFFERED=1
export SWANLAB_WORKSPACE="${SWANLAB_WORKSPACE:-DuofengPan}"
export UFO_CACHE_DIR="${UFO_CACHE_DIR:-/var/tmp/ufo-cache}"
export TMPDIR="${TMPDIR:-/var/tmp/ufo-tmp}"
export TORCHINDUCTOR_CACHE_DIR="${TORCHINDUCTOR_CACHE_DIR:-/var/tmp/ufo-torchinductor}"
export TRITON_CACHE_DIR="${TRITON_CACHE_DIR:-/var/tmp/ufo-triton}"
mkdir -p "$UFO_CACHE_DIR" "$TMPDIR" "$TORCHINDUCTOR_CACHE_DIR" "$TRITON_CACHE_DIR"
args=("$PYTHON" -m ufo.train --agent fb --gpu-ids all
  --robot-config configs/robots/astro_p2_29dof.yaml
  --data-manifest configs/data/astro_lafan_high_dynamic.yaml
  --network-width 1024 --shared-critic --bf16-amp
  --num-envs 1024 --num-env-steps 192000000 --buffer-size 2560000 --replay-device cpu
  --num-agent-updates 16 --checkpoint-every-steps 3200000 --buffer-every-steps 16000000
  --use-swanlab --swanlab-run-name "$RUN_NAME" --work-dir "$RUN_DIR")
"$PYTHON" - <<'PY'
from ufo.motion.manifest import prepare_motion_manifest
from ufo.tools.robot_config import load_robot_training_spec
from ufo.agents.fb_cpr_aux.config import build_fb_agent
m = prepare_motion_manifest('configs/data/astro_lafan_high_dynamic.yaml')
assert m.train_data_weights == [0.9, 0.1]
r = load_robot_training_spec('configs/robots/astro_p2_29dof.yaml')
a = build_fb_agent(device='cpu', overrides=r.fb_agent_overrides, network_width=1024, shared_critic=True, use_bf16_amp=True)
assert a.model.archi.shared_critic and a.train.use_bf16_amp
assert all(getattr(a.model.archi, k).hidden_dim == 1024 for k in ('actor', 'f', 'critic'))
assert a.train.batch_size == 1024
print('Validated Astro 1024/shared/BF16 and 90/10 source weights.')
PY
if (( dry_run )); then
  printf '%q ' "${args[@]}"
  printf '\n'
  exit 0
fi
MIN_FREE_GPU_MIB="${MIN_FREE_GPU_MIB:-28000}"
[[ "$MIN_FREE_GPU_MIB" =~ ^[1-9][0-9]*$ ]] || { echo 'Invalid memory threshold' >&2; exit 2; }
"$PYTHON" - "$MIN_FREE_GPU_MIB" <<'PY'
import sys
import torch
minimum = int(sys.argv[1]) * 1024 * 1024
if torch.cuda.device_count() != 8:
    raise SystemExit('Exactly eight visible GPUs are required')
for gpu in range(8):
    free, _ = torch.cuda.mem_get_info(gpu)
    if free < minimum:
        raise SystemExit(f'GPU {gpu}: insufficient free memory; no training started')
PY
mkdir -p "$RUN_DIR"
git rev-parse HEAD > "$RUN_DIR/git_commit.txt"
git diff --binary > "$RUN_DIR/local_changes.patch"
git status --short > "$RUN_DIR/working_tree_status.txt"
cp configs/robots/astro_p2_29dof.yaml "$RUN_DIR/robot_config.yaml"
cp configs/data/astro_lafan_high_dynamic.yaml "$RUN_DIR/data_manifest.yaml"
cp ufo/data/robots/astro_p2/motions/high_dynamic/manifest.json "$RUN_DIR/data_provenance.json"
printf '%q ' "${args[@]}" > "$RUN_DIR/command.txt"
printf '\n' >> "$RUN_DIR/command.txt"
nohup "${args[@]}" > "$RUN_DIR/launcher.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$RUN_DIR/launcher.pid"
echo "Started PID=$!, run=$RUN_DIR"
