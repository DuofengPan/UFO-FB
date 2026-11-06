#!/usr/bin/env bash
# Keep a container's global NCCL preload from overriding this checkout's lockfile.
ufo_use_project_nccl() {
  local library="$1/.venv/lib/python3.10/site-packages/nvidia/nccl/lib/libnccl.so.2"
  [[ -f "$library" ]] || return 0
  local entry preload="${LD_PRELOAD:-}"
  local -a existing=() selected=("$library")
  read -r -a existing <<< "${preload//:/ }"
  for entry in "${existing[@]}"; do
    case "${entry##*/}" in
      libnccl.so*) ;;
      *) selected+=("$entry") ;;
    esac
  done
  export LD_PRELOAD="${selected[*]}"
}
