import os
import subprocess
from pathlib import Path


def select(root, preload):
    helper = Path("scripts/runtime_libraries.sh").resolve()
    return subprocess.check_output(
        ["bash", "-c", 'LD_PRELOAD="$3"; source "$1"; ufo_use_project_nccl "$2"; printf "%s" "$LD_PRELOAD"', "bash", str(helper), str(root), preload],
        env={k: v for k, v in os.environ.items() if k != "LD_PRELOAD"}, text=True,
    )


def test_project_nccl_replaces_only_nccl_preload(tmp_path):
    library = tmp_path / ".venv/lib/python3.10/site-packages/nvidia/nccl/lib/libnccl.so.2"
    library.parent.mkdir(parents=True)
    library.touch()
    assert select(tmp_path, "/opt/old/libnccl.so.2:/lib/x86_64-linux-gnu/libm.so.6") == \
        f"{library} /lib/x86_64-linux-gnu/libm.so.6"


def test_missing_local_environment_keeps_preloads(tmp_path):
    assert select(tmp_path, "/opt/old/libnccl.so.2") == "/opt/old/libnccl.so.2"
