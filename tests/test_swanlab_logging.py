from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np
import pytest

from ufo.training import swanlab_logging as logging


def config(**updates):
    values = dict(use_swanlab=True, distributed_rank=0, swanlab_project="ufo-humanoid",
                  swanlab_workspace="DuofengPan", swanlab_group="ufo_fb",
                  swanlab_run_name="astro-test", work_dir="runs/astro-test", model_dump=lambda: {"seed": 7})
    return SimpleNamespace(**(values | updates))


def test_only_rank_zero_initializes_and_uploads():
    sdk = Mock()
    with patch.dict("sys.modules", {"swanlab": sdk}), patch.object(logging.atexit, "register"), patch.object(logging.signal, "signal"):
        for cfg in (config(distributed_rank=1), config(use_swanlab=False)):
            logging.init_swanlab(cfg)
            logging.log_swanlab(cfg, {"loss": 1.0}, prefix="train", step=123)
        sdk.init.assert_not_called()
        sdk.log.assert_not_called()
        logging.init_swanlab(config())
        assert sdk.init.call_args.kwargs["experiment_name"] == "astro-test"
        assert sdk.init.call_args.kwargs["config"] == {"seed": 7}
        assert sdk.init.call_args.kwargs["logdir"] == "runs/astro-test/swanlog"
        logging.log_swanlab(config(), {"loss": np.float32(2.5), "mode": "manual", "steps": 8}, prefix="train", step=123)
        sdk.log.assert_called_once_with({"train/loss": 2.5, "train/steps": 8}, step=123)
        logging.log_swanlab(config(), {"emd": 0.8}, prefix="eval/ufo_tracking_eval", step=3200000)
        sdk.log.assert_called_with({"eval/ufo_tracking_eval/emd": 0.8}, step=3200000)


@pytest.mark.parametrize("state", ["success", "crashed", "aborted"])
def test_finish_status_and_idempotence(state):
    sdk = Mock()
    run = SimpleNamespace(alive=True)
    sdk.get_run.return_value = run
    sdk.finish.side_effect = lambda **_: setattr(run, "alive", False)
    with patch.dict("sys.modules", {"swanlab": sdk}):
        logging.finish_swanlab(state=state, error="test")
        logging.finish_swanlab(state=state, error="test")
    sdk.finish.assert_called_once_with(state=state, error="test")


def test_signal_finishes_as_aborted():
    sdk = Mock()
    with patch.dict("sys.modules", {"swanlab": sdk}), patch.object(logging.atexit, "register"), patch.object(logging.signal, "signal") as signals:
        logging.init_swanlab(config())
        handler = signals.call_args_list[0].args[1]
        with pytest.raises(SystemExit):
            handler(15, None)
    sdk.finish.assert_called_once_with(state="aborted", error="received signal 15")


@pytest.mark.parametrize("failure,state", [(None, "success"), (RuntimeError("test failure"), "crashed"),
                                          (KeyboardInterrupt(), "aborted")])
def test_training_entrypoint_finalizes_on_exit(tmp_path, failure, state):
    from ufo import train
    from ufo.training.config import TrainConfig

    with patch("sys.argv", ["ufo.train", "--robot-config", "configs/robots/astro_p2_29dof.yaml",
                            "--data-path", "/tmp/unused-data.pkl", "--use-swanlab"]):
        args = train.parse_args()
    trainer = Mock()
    trainer.train.side_effect = failure
    with patch.object(train, "_select_device_and_rank", return_value=("cpu", 0, 0, 1)), \
         patch.object(train, "_init_distributed"), patch.object(TrainConfig, "build", return_value=trainer), \
         patch.object(logging, "finish_swanlab") as finish:
        if failure is None:
            train.run_train(args, tmp_path)
        else:
            with pytest.raises(type(failure)):
                train.run_train(args, tmp_path)
    assert finish.call_args.kwargs["state"] == state
