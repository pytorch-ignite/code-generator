import logging

#::: if ((it.argparser == 'argparse')) { :::#
from argparse import ArgumentParser

#::: } :::#
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Any, Mapping, Optional, Union

import ignite.distributed as idist
import torch
from ignite.contrib.engines import common
from ignite.engine import Engine

#::: if (it.save_training || it.save_evaluation || it.patience || it.terminate_on_nan || it.limit_sec) { :::#
from ignite.engine.events import Events

#::: } :::#
#::: if (it.save_training || it.save_evaluation) { :::#
from ignite.handlers import Checkpoint, DiskSaver, global_step_from_engine  # usort: skip

#::: } else { :::#
from ignite.handlers import Checkpoint

#::: } :::#
#::: if (it.patience) { :::#
from ignite.handlers.early_stopping import EarlyStopping

#::: } :::#
#::: if (it.terminate_on_nan) { :::#
from ignite.handlers.terminate_on_nan import TerminateOnNan

#::: } :::#
#::: if (it.limit_sec) { :::#
from ignite.handlers.time_limit import TimeLimit

#::: } :::#
from ignite.utils import setup_logger
from omegaconf import OmegaConf

#::: if ((it.argparser == 'fire')) { :::#


def setup_config(config_path, backend, **kwargs):
    config = OmegaConf.load(config_path)

    for k, v in kwargs.items():
        if k in config:
            print(f"Override parameter {k}: {config[k]} -> {v}")
        else:
            print(f"{k} parameter not in {config_path}")
        config[k] = v

    config.backend = backend

    return config


#::: } else { :::#


def get_default_parser():
    parser = ArgumentParser()
    parser.add_argument("config", type=Path, help="Config file path")
    parser.add_argument(
        "--backend",
        default=None,
        choices=["nccl", "gloo"],
        type=str,
        help="DDP backend",
    )
    return parser


def setup_config(parser=None):
    if parser is None:
        parser = get_default_parser()

    args = parser.parse_args()

    config_path = args.config

    config = OmegaConf.load(config_path)

    config.backend = args.backend

    return config


#::: } :::#


def log_metrics(engine: Engine, tag: str) -> None:
    """Log `engine.state.metrics` with given `engine` and `tag`.

    Parameters
    ----------
    engine
        instance of `Engine` which metrics to log.
    tag
        a string to add at the start of output.
    """
    metrics_format = "{0} [{1}/{2}]: {3}".format(tag, engine.state.epoch, engine.state.iteration, engine.state.metrics)
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
            raise FileNotFoundError(f"Given {str(checkpoint_fp)} does not exist.")
        checkpoint = torch.load(checkpoint_fp, map_location="cpu")

    Checkpoint.load_objects(to_load=to_load, checkpoint=checkpoint, strict=strict)
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


def save_config(config, output_dir):
    """Save configuration to config-lock.yaml for result reproducibility."""
    with open(f"{output_dir}/config-lock.yaml", "w") as f:
        OmegaConf.save(config, f)


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


#::: if (it.logger) { :::#


def setup_exp_logging(config, trainer, optimizers, evaluators):
    """Setup Experiment Tracking logger from Ignite."""

    #::: if (it.logger === 'clearml') { :::#
    logger = common.setup_clearml_logging(trainer, optimizers, evaluators, config.log_every_iters)
    #::: } else if (it.logger === 'mlflow') { :::#
    logger = common.setup_mlflow_logging(trainer, optimizers, evaluators, config.log_every_iters)
    #::: } else if (it.logger === 'neptune') { :::#
    logger = common.setup_neptune_logging(trainer, optimizers, evaluators, config.log_every_iters)
    #::: } else if (it.logger === 'polyaxon') { :::#
    logger = common.setup_plx_logging(trainer, optimizers, evaluators, config.log_every_iters)
    #::: } else if (it.logger === 'tensorboard') { :::#
    logger = common.setup_tb_logging(
        config.output_dir,
        trainer,
        optimizers,
        evaluators,
        config.log_every_iters,
    )
    #::: } else if (it.logger === 'visdom') { :::#
    logger = common.setup_visdom_logging(trainer, optimizers, evaluators, config.log_every_iters)
    #::: } else if (it.logger === 'wandb') { :::#
    logger = common.setup_wandb_logging(trainer, optimizers, evaluators, config.log_every_iters)
    #::: } :::#
    return logger


#::: } :::#
