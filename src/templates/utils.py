### imports ###
from logging import Logger
from pathlib import Path
from typing import Any, Mapping, Optional, Tuple, Union

import ignite.distributed as idist
import torch
from ignite.contrib.handlers import PiecewiseLinear
from ignite.contrib.handlers.param_scheduler import ParamScheduler
from ignite.engine import Engine
from ignite.handlers import Checkpoint
from ignite.utils import setup_logger
from models import get_model
from torch.nn import CrossEntropyLoss, Module
from torch.optim import Adam, Optimizer
from torch.optim.lr_scheduler import _LRScheduler


### checkpointing ###
def checkpointing(to_save_train: dict, to_save_eval: dict, config: Any):
    from ignite.handlers import DiskSaver, global_step_from_engine

    saver = DiskSaver(config.output_dir / "checkpoints", require_empty=False)
    ckpt_handler_train = Checkpoint(
        to_save_train,
        saver,
        filename_prefix=config.filename_prefix,
        n_saved=config.n_saved,
    )
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
    )
    return ckpt_handler_train, ckpt_handler_eval


### get_default_parser ###
def get_default_parser():
    import json
    from argparse import ArgumentParser

    with open("config.json", "r") as f:
        config = json.load(f)

    parser = ArgumentParser(add_help=False)
    for key, value in config.items():
        parser.add_argument(f"--{key}", default=value)

    return parser


### initialize ###
def initialize(
    config: Optional[Any],
) -> Tuple[Module, Optimizer, Module, Union[_LRScheduler, ParamScheduler]]:
    """Initializing model, optimizer, loss function, and lr scheduler
    with correct settings.

    Parameters
    ----------
    config:
        config object

    Returns
    -------
    model, optimizer, loss_fn, lr_scheduler
    """
    model = get_model(config.model)
    optimizer = Adam(model.parameters(), lr=config.lr)
    loss_fn = CrossEntropyLoss().to(idist.device())
    lr_scheduler = None
    model = idist.auto_model(model)
    optimizer = idist.auto_optim(optimizer)
    loss_fn = loss_fn.to(idist.device())

    return model, optimizer, loss_fn, lr_scheduler


### log_metrics ###
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


### resume_from ###
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


### setup_logging ###
def setup_logging(config: Any) -> Logger:
    """Setup logger with `ignite.utils.setup_logger()`.

    Parameters
    ----------
    config
        config object. config has to contain `output_dir` attribute.

    Returns
    -------
    logger
        an instance of `Logger`
    """
    green = "\033[32m"
    reset = "\033[0m"
    logger = setup_logger(
        name=f"{green}[ignite]{reset}",
        format="%(name)s: %(message)s",
        filepath=config.output_dir / "training-info.log",
    )
    return logger
