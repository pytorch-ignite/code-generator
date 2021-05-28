import logging
from argparse import ArgumentParser
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Any, Mapping, Optional, Union

import ignite.distributed as idist
import torch
import yaml
from ignite.contrib.engines import common
from ignite.engine import Engine
from ignite.engine.events import Events
from ignite.handlers import Checkpoint, DiskSaver, global_step_from_engine
from ignite.handlers.early_stopping import EarlyStopping
from ignite.handlers.terminate_on_nan import TerminateOnNan
from ignite.handlers.time_limit import TimeLimit
from ignite.utils import setup_logger


def setup_parser():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f.read())

    parser = ArgumentParser()
    parser.add_argument("--backend", default=None, type=str)
    for k, v in config.items():
        if isinstance(v, bool):
            parser.add_argument(f"--{k}", action="store_true")
        else:
            parser.add_argument(f"--{k}", default=v, type=type(v))

    return parser


def log_metrics(engine: Engine, tag: str) -> None:
    """Log `engine.state.metrics` with given `engine` and `tag`.

    Parameters
    ----------
    engine
        instance of `Engine` which metrics to log.
    tag
        a string to add at the start of output.
    """
    metrics_format = "{0} [{1}/{2}]: {3}".format(
        tag, engine.state.epoch, engine.state.iteration, engine.state.metrics
    )
    engine.logger.info(metrics_format)


def resume_from(
    to_load: Mapping,
    checkpoint_fp: Union[str, Path],
    logger: Logger,
    strict: bool = True,
    model_dir: Optional[str] = None,
) -> None:
    """Loads state dict from a checkpoint file to resume the training.

    Parameters
    ----------
    to_load
        a dictionary with objects, e.g. {“model”: model, “optimizer”: optimizer, ...}
    checkpoint_fp
        path to the checkpoint file
    logger
        to log info about resuming from a checkpoint
    strict
        whether to strictly enforce that the keys in `state_dict` match the keys
        returned by this module’s `state_dict()` function. Default: True
    model_dir
        directory in which to save the object
    """
    if isinstance(checkpoint_fp, str) and checkpoint_fp.startswith("https://"):
        checkpoint = torch.hub.load_state_dict_from_url(
            checkpoint_fp,
            model_dir=model_dir,
            map_location="cpu",
            check_hash=True,
        )
    else:
        if isinstance(checkpoint_fp, str):
            checkpoint_fp = Path(checkpoint_fp)

        if not checkpoint_fp.exists():
            raise FileNotFoundError(
                f"Given {str(checkpoint_fp)} does not exist."
            )
        checkpoint = torch.load(checkpoint_fp, map_location="cpu")

    Checkpoint.load_objects(
        to_load=to_load, checkpoint=checkpoint, strict=strict
    )
    logger.info("Successfully resumed from a checkpoint: %s", checkpoint_fp)


def setup_output_dir(config: Any, rank: int) -> Path:
    """Create output folder."""
    if rank == 0:
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        name = f"{now}-backend-{config.backend}-lr-{config.lr}"
        path = Path(config.output_dir, name)
        path.mkdir(parents=True, exist_ok=True)
        config.output_dir = path.as_posix()

    return Path(idist.broadcast(config.output_dir, src=0))


def setup_logging(config: Any) -> Logger:
    """Setup logger with `ignite.utils.setup_logger()`.

    Parameters
    ----------
    config
        config object. config has to contain `verbose` and `output_dir` attribute.

    Returns
    -------
    logger
        an instance of `Logger`
    """
    green = "\033[32m"
    reset = "\033[0m"
    logger = setup_logger(
        name=f"{green}[ignite]{reset}",
        level=logging.DEBUG if config.debug else logging.INFO,
        format="%(name)s: %(message)s",
        filepath=config.output_dir / "training-info.log",
    )
    return logger


#::: if (it.save_training || it.save_evaluation || it.patience || it.terminate_on_nan || it.limit_sec) { :::#
def setup_handlers(
    trainer: Engine,
    evaluator: Engine,
    config: Any,
    to_save_train: Optional[dict] = None,
    to_save_eval: Optional[dict] = None,
):
    """Setup Ignite handlers."""

    ckpt_handler_train = ckpt_handler_eval = None
    #::: if (it.save_training || it.save_evaluation) { :::#
    # checkpointing
    saver = DiskSaver(config.output_dir / "checkpoints", require_empty=False)
    #::: if (it.save_training) { :::#
    ckpt_handler_train = Checkpoint(
        to_save_train,
        saver,
        filename_prefix=config.filename_prefix,
        n_saved=config.n_saved,
    )
    trainer.add_event_handler(
        Events.ITERATION_COMPLETED(every=config.save_every_iters),
        ckpt_handler_train,
    )
    #::: } :::#
    #::: if (it.save_evaluation) { :::#
    global_step_transform = None
    if to_save_train.get("trainer", None) is not None:
        global_step_transform = global_step_from_engine(
            to_save_train["trainer"]
        )
    ckpt_handler_eval = Checkpoint(
        to_save_eval,
        saver,
        filename_prefix="best",
        n_saved=config.n_saved,
        global_step_transform=global_step_transform,
        score_name="eval_accuracy",
        score_function=Checkpoint.get_default_score_fn("Accuracy"),
    )
    evaluator.add_event_handler(
        Events.EPOCH_COMPLETED(every=1), ckpt_handler_eval
    )
    #::: } :::#
    #::: } :::#

    #::: if (it.patience) { :::#
    # early stopping
    def score_fn(engine: Engine):
        return engine.state.metrics["Accuracy"]

    es = EarlyStopping(config.patience, score_fn, trainer)
    evaluator.add_event_handler(Events.EPOCH_COMPLETED, es)
    #::: } :::#

    #::: if (it.terminate_on_nan) { :::#
    # terminate on nan
    trainer.add_event_handler(Events.ITERATION_COMPLETED, TerminateOnNan())
    #::: } :::#

    #::: if (it.limit_sec) { :::#
    # time limit
    trainer.add_event_handler(
        Events.ITERATION_COMPLETED, TimeLimit(config.limit_sec)
    )
    #::: } :::#
    #::: if (it.save_training || it.save_evaluation) { :::#
    return ckpt_handler_train, ckpt_handler_eval
    #::: } :::#


#::: } :::#

#::: if (it.logger) { :::#


def setup_exp_logging(config, trainer, optimizers, evaluators):
    """Setup Experiment Tracking logger from Ignite."""

    #::: if (it.logger === 'clearml') { :::#
    logger = common.setup_clearml_logging(
        trainer, optimizers, evaluators, config.log_every_iters
    )
    #::: } else if (it.logger === 'mlflow') { :::#
    logger = common.setup_mlflow_logging(
        trainer, optimizers, evaluators, config.log_every_iters
    )
    #::: } else if (it.logger === 'neptune') { :::#
    logger = common.setup_neptune_logging(
        trainer, optimizers, evaluators, config.log_every_iters
    )
    #::: } else if (it.logger === 'polyaxon') { :::#
    logger = common.setup_plx_logging(
        trainer, optimizers, evaluators, config.log_every_iters
    )
    #::: } else if (it.logger === 'tensorboard') { :::#
    logger = common.setup_tb_logging(
        config.output_dir,
        trainer,
        optimizers,
        evaluators,
        config.log_every_iters,
    )
    #::: } else if (it.logger === 'visdom') { :::#
    logger = common.setup_visdom_logging(
        trainer, optimizers, evaluators, config.log_every_iters
    )
    #::: } else if (it.logger === 'wandb') { :::#
    logger = common.setup_wandb_logging(
        trainer, optimizers, evaluators, config.log_every_iters
    )
    #::: } :::#
    return logger


#::: } :::#


def thresholded_output_transform(output):
    y_pred, y = output
    return torch.round(torch.sigmoid(y_pred)), y
