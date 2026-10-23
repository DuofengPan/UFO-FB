#!/usr/bin/env bash
set -euo pipefail
cd /root/code/UFO
source /root/miniforge3/etc/profile.d/conda.sh
conda activate ufo
pkill -f 'humanoidverse.train' 2>/dev/null || true
pkill -f 'torchrunx' 2>/dev/null || true
sleep 3
mkdir -p runs/ufo_fb_astro_lafan_8gpu cache/tmp
export PYTHONPATH=/root/code/UFO
export UFO_CACHE_DIR=/root/code/UFO/cache
export BFMZERO_MJLAB_CACHE_DIR=/root/code/UFO/cache
export TMPDIR=/root/code/UFO/cache/tmp
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export NCCL_NVLS_ENABLE=0
export PYTHONUNBUFFERED=1
ts=$(date +%H%M%S)
if [[ -f runs/ufo_fb_astro_lafan_8gpu/train_stdout.log ]]; then
  mv -f runs/ufo_fb_astro_lafan_8gpu/train_stdout.log "runs/ufo_fb_astro_lafan_8gpu/train_stdout.log.bak.${ts}"
fi
nohup python -m humanoidverse.train \
  --agent fb \
  --gpu-ids all \
  --robot-config configs/robots/astro_p2_29dof.yaml \
  --data-manifest configs/data/astro_lafan.yaml \
  --num-envs 1024 \
  --buffer-size 2560000 \
  --use-swanlab \
  --swanlab-run-name ufo_fb_astro_lafan_8gpu \
  --work-dir runs/ufo_fb_astro_lafan_8gpu \
  > runs/ufo_fb_astro_lafan_8gpu/train_stdout.log 2>&1 &
echo "PID=$!"
sleep 5
ps -p $! -o pid,etime,cmd --no-headers || true
tail -5 runs/ufo_fb_astro_lafan_8gpu/train_stdout.log || true
