#!/usr/bin/env bash
# New run only; never resumes, removes buffers, or stops other jobs.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"
PYTHON="${PYTHON:-${ROOT_DIR}/.venv/bin/python}"
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
# Validate data and write all provenance before spawning GPU workers.
"${PYTHON}" - <<'PY'
from humanoidverse.utils.motion_data.manifest import prepare_motion_manifest
m = prepare_motion_manifest('configs/data/astro_lafan_high_dynamic.yaml')
assert m.train_data_weights == [0.9, 0.1], m.train_data_weights
print('Validated motion sources:', list(zip(m.train_data_paths, m.train_data_weights)))
PY
mkdir -p "${RUN_DIR}"
git -c safe.directory="${ROOT_DIR}" rev-parse HEAD > "${RUN_DIR}/git_commit.txt"
git -c safe.directory="${ROOT_DIR}" diff --stat > "${RUN_DIR}/working_tree_diff_stat.txt"
cp configs/data/astro_lafan_high_dynamic.yaml "${RUN_DIR}/data_manifest.yaml"
cp humanoidverse/data/astro_high_dynamic/manifest.json "${RUN_DIR}/data_provenance.json"
args=("${PYTHON}" -m humanoidverse.train --agent fb --gpu-ids all
  --robot-config configs/robots/astro_p2_29dof.yaml
  --data-manifest configs/data/astro_lafan_high_dynamic.yaml
  --num-envs 4096 --num-env-steps 192000000 --buffer-size 5120000
  --num-agent-updates 64 --checkpoint-every-steps 3200000
  --use-swanlab --swanlab-run-name "${RUN_NAME}" --work-dir "${RUN_DIR}")
printf '%q ' "${args[@]}" > "${RUN_DIR}/command.txt"
printf '\n' >> "${RUN_DIR}/command.txt"
nohup "${args[@]}" > "${RUN_DIR}/launcher.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "${RUN_DIR}/launcher.pid"
echo "Started PID=$!, run=${RUN_DIR}"
echo "Log: ${RUN_DIR}/launcher.log"
