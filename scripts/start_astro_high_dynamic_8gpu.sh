#!/usr/bin/env bash
# New run only; never resumes, removes buffers, or stops other jobs.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"
PYTHON="${PYTHON:-${ROOT_DIR}/.venv/bin/python}"
WAIT_FOR_GPUS=0
if [[ "${1:-}" == "--wait-for-gpus" ]]; then
  WAIT_FOR_GPUS=1
  shift
fi
if (($#)); then
  echo 'usage: scripts/start_astro_high_dynamic_8gpu.sh [--wait-for-gpus]' >&2
  exit 2
fi
RUN_NAME="${RUN_NAME:-astro_fb_scratch_lafan90_highdynamic10_8gpu_4096_u64_$(date -u +%Y%m%d_%H%M%S)_UTC}"
RUN_DIR="${ROOT_DIR}/runs/${RUN_NAME}"
if [[ -e "${RUN_DIR}" ]]; then
  echo "error: run exists; choose a new RUN_NAME: ${RUN_DIR}" >&2
  exit 1
fi
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export NCCL_NVLS_ENABLE=0
export PYTHONUNBUFFERED=1
export UFO_CACHE_DIR="${ROOT_DIR}/.cache"
export BFMZERO_MJLAB_CACHE_DIR="${ROOT_DIR}/.cache"
# Real startup with only ~9 GiB free failed during Warp graph capture. Require
# headroom on all eight GPUs; waiting never kills or resets another workload.
MIN_FREE_GPU_MIB="${MIN_FREE_GPU_MIB:-32768}"
MAX_GPU_WAIT_SECONDS="${MAX_GPU_WAIT_SECONDS:-86400}"
[[ "${MIN_FREE_GPU_MIB}" =~ ^[1-9][0-9]*$ && "${MAX_GPU_WAIT_SECONDS}" =~ ^[1-9][0-9]*$ ]] || {
  echo 'error: memory threshold and maximum wait must be positive integers' >&2
  exit 2
}
wait_started=${SECONDS}
while true; do
  free_memory="$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits)"
  if awk -v minimum="${MIN_FREE_GPU_MIB}" '
      NR <= 8 {if ($1 < minimum) insufficient=1}
      END {exit (NR < 8 || insufficient)}' <<< "${free_memory}"; then
    break
  fi
  if [[ "${WAIT_FOR_GPUS}" != 1 ]]; then
    echo "error: GPUs 0-7 must each have at least ${MIN_FREE_GPU_MIB} MiB free" >&2
    echo 'Use --wait-for-gpus to wait up to MAX_GPU_WAIT_SECONDS (default 24 h).' >&2
    exit 1
  fi
  if (( SECONDS - wait_started >= MAX_GPU_WAIT_SECONDS )); then
    echo 'error: timed out waiting for GPU memory; no training started' >&2
    exit 1
  fi
  echo "$(date -Is) Waiting for all 8 GPUs >= ${MIN_FREE_GPU_MIB} MiB free; current: $(tr '\n' ' ' <<< "${free_memory}")"
  sleep 60
done
# Validate data and write all provenance before spawning GPU workers.
"${PYTHON}" - <<'PY'
from humanoidverse.utils.motion_data.manifest import prepare_motion_manifest
m = prepare_motion_manifest('humanoidverse/data/robots/astro_p2/config/lafan_high_dynamic.yaml')
assert m.train_data_weights == [0.9, 0.1], m.train_data_weights
print('Validated motion sources:', list(zip(m.train_data_paths, m.train_data_weights)))
PY
mkdir -p "${RUN_DIR}"
git -c safe.directory="${ROOT_DIR}" rev-parse HEAD > "${RUN_DIR}/git_commit.txt"
git -c safe.directory="${ROOT_DIR}" diff --stat > "${RUN_DIR}/working_tree_diff_stat.txt"
cp humanoidverse/data/robots/astro_p2/config/lafan_high_dynamic.yaml "${RUN_DIR}/data_manifest.yaml"
cp humanoidverse/data/robots/astro_p2/motions/high_dynamic/manifest.json "${RUN_DIR}/data_provenance.json"
args=("${PYTHON}" -m humanoidverse.train --agent fb --gpu-ids all
  --robot-config humanoidverse/data/robots/astro_p2/config/robot.yaml
  --data-manifest humanoidverse/data/robots/astro_p2/config/lafan_high_dynamic.yaml
  --num-envs 4096 --num-env-steps 192000000 --buffer-size 5120000
  --num-agent-updates 64 --checkpoint-every-steps 3200000
  --use-swanlab --swanlab-run-name "${RUN_NAME}" --work-dir "${RUN_DIR}")
printf '%q ' "${args[@]}" > "${RUN_DIR}/command.txt"
printf '\n' >> "${RUN_DIR}/command.txt"
nohup "${args[@]}" > "${RUN_DIR}/launcher.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "${RUN_DIR}/launcher.pid"
echo "Started PID=$!, run=${RUN_DIR}"
echo "Log: ${RUN_DIR}/launcher.log"
