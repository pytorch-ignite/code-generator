"""
utility functions which can be used in training
"""
import hashlib
import logging
import os
import shutil
from datetime import datetime
from logging import Logger
from pathlib import Path
from pprint import pformat
from typing import Any, Optional, Tuple, Union

import ignite.distributed as idist
import torch
from ignite.engine import Engine
from ignite.utils import setup_logger
from torch.nn import Module
from torch.optim.optimizer import Optimizer
from torch.optim.lr_scheduler import _LRScheduler


{% include "_argparse.pyi" %}


def initialize(config: Optional[Any]) -> Tuple[Module, Optimizer, Module, _LRScheduler]:
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
    model = ...
    optimizer = ...
    loss_fn = ...
    lr_scheduler = ...
    model = idist.auto_model(model)
    optimizer = idist.auto_optim(optimizer)
    loss_fn = loss_fn.to(idist.device())

    return model, optimizer, loss_fn, lr_scheduler


def log_basic_info(logger: Logger, config: Any) -> None:
    """Logging about pytorch, ignite, configurations, gpu system
    distributed settings.

    Parameters
    ----------
    logger
        Logger instance for logging
    config
        config object to log
    """
    import ignite

    logger.info("- PyTorch version: %s", torch.__version__)
    logger.info("- Ignite version: %s", ignite.__version__)
    if torch.cuda.is_available():
        # explicitly import cudnn as
        # torch.backends.cudnn can not be pickled with hvd spawning procs
        from torch.backends import cudnn

        logger.info("- GPU device: %s", torch.cuda.get_device_name(idist.get_local_rank()))
        logger.info("- CUDA version: %s", torch.version.cuda)
        logger.info("- CUDNN version: %s", cudnn.version())

    logger.info("\n")
    logger.info("Configuration:")
    logger.info("%s", pformat(vars(config)))
    logger.info("\n")

    if idist.get_world_size() > 1:
        logger.info("\nDistributed setting:")
        logger.info("\tbackend: %s", idist.backend())
        logger.info("\tworld size: %s", idist.get_world_size())
        logger.info("\n")


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


def setup_logging(config: Any) -> Logger:
    """Setup logger with `ignite.utils.setup_logger()`.

    Parameters
    ----------
    config
        config object. config has to contain
        `verbose` and `filepath` attributes.

    Returns
    -------
    logger
        an instance of `Logger`
    """
    now = datetime.now().strftime("%Y%m%d-%X")
    logger = setup_logger(
        level=logging.INFO if config.verbose else logging.WARNING,
        format="%(message)s",
        filepath=config.filepath / f"{now}.log",
    )
    return logger


def hash_checkpoint(
    checkpoint: str,
    jitted: bool,
    output_path: Union[str, Path],
) -> Tuple[str, str]:
    """Hash the checkpoint file to be used with `check_hash` of
    `torch.hub.load_state_dict_from_url`.

    Parameters
    ----------
    checkpoint
        checkpoint file.
    jitted
        indicate the checkpoint is already applied torch.jit or not.
    output_path
        path to store the hashed checkpoint file.

    Returns
    -------
    filename and sha_hash
        the hashed filename and SHA hash
    """
    with open(checkpoint, "rb") as file:
        sha_hash = hashlib.sha256(file.read()).hexdigest()

    ckpt_file_name = os.path.splitext(checkpoint.split(os.sep)[-1])[0]
    if jitted:
        filename = "-".join((ckpt_file_name, sha_hash[:8])) + ".ptc"
    else:
        filename = "-".join((ckpt_file_name, sha_hash[:8])) + ".pt"

    if isinstance(output_path, str):
        output_path = Path(output_path)

    shutil.move(checkpoint, output_path / filename)
    print("Saved state dict into %s | SHA256: %s", filename, sha_hash)

    return filename, sha_hash
