"""Optional rank-zero SwanLab logging; credentials stay in the SDK login store."""

import atexit
import signal
from numbers import Real
from pathlib import Path

import numpy as np


def scalar_metrics(metrics):
    return {key: value.item() if isinstance(value, np.generic) else value
            for key, value in metrics.items() if isinstance(value, Real)}


def init_swanlab(cfg):
    if not cfg.use_swanlab or cfg.distributed_rank != 0:
        return
    import swanlab

    swanlab.init(
        project=cfg.swanlab_project,
        workspace=cfg.swanlab_workspace,
        group=cfg.swanlab_group,
        experiment_name=cfg.swanlab_run_name or Path(cfg.work_dir).name,
        config=cfg.model_dump(),
        logdir=str(Path(cfg.work_dir) / "swanlog"),
    )
    atexit.register(lambda: finish_swanlab(state="aborted", error="process exited without explicit finish"))

    def abort(signum, _frame):
        finish_swanlab(state="aborted", error=f"received signal {signum}")
        raise SystemExit(128 + signum)

    signal.signal(signal.SIGTERM, abort)
    signal.signal(signal.SIGINT, abort)


def log_swanlab(cfg, metrics, *, prefix, step):
    if getattr(cfg, "use_swanlab", False) and cfg.distributed_rank == 0:
        import swanlab

        payload = {f"{prefix}/{key}": value for key, value in scalar_metrics(metrics).items()}
        if payload:
            swanlab.log(payload, step=step)


def finish_swanlab(*, state="success", error=None):
    try:
        import swanlab

        if swanlab.has_run():
            run = swanlab.get_run()
            if run is not None and getattr(run, "alive", True):
                swanlab.finish(state=state, error=error)
    except Exception as exc:
        print(f"WARNING: swanlab.finish failed: {exc}", flush=True)
