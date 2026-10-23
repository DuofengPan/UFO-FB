#!/usr/bin/env bash
# Health snapshot for Astro 8-GPU LaFAN train. Exit 0=ok, 2=dead/needs restart, 3=OOM-risk.
set -euo pipefail
WORK=runs/ufo_fb_astro_lafan_8gpu
LOG="$WORK/train_stdout.log"
CONTAINER=atom9-isaacsim-vnc

docker exec "$CONTAINER" bash -lc "
set -euo pipefail
cd /root/code/UFO
nproc=\$(ps aux | grep -E '[s]pawn_main.*multiprocessing' | wc -l)
oom=\$(grep -c 'OutOfMemoryError' $LOG 2>/dev/null || true)
tb=\$(grep -c 'Traceback' $LOG 2>/dev/null || true)
mem=\$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr '\n' ' ')
util=\$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | tr '\n' ' ')
max_mem=0
for m in \$mem; do
  if [ \"\$m\" -gt \"\$max_mem\" ]; then max_mem=\$m; fi
done
headroom=\$((32607 - max_mem))
echo \"TIME=\$(date -Is) WORKERS=\$nproc MAX_MEM_MIB=\$max_mem HEADROOM_MIB=\$headroom OOM_HITS=\$oom TRACEBACKS=\$tb\"
echo \"MEM_ALL=\$mem\"
echo \"UTIL_ALL=\$util\"
# recent swanlab / progress hints
grep -E 'swanlab:|View run|global_env_steps|FPS' $LOG 2>/dev/null | tail -5 || true
if [ \"\$nproc\" -lt 6 ]; then
  echo STATUS=DEAD
  exit 2
fi
if [ \"\$max_mem\" -gt 30000 ]; then
  echo STATUS=OOM_RISK
  exit 3
fi
echo STATUS=OK
exit 0
"
