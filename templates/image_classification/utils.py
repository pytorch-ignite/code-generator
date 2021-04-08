"""
utility functions which can be used in training
"""
import hashlib
import logging
import shutil
from logging import Logger
from pathlib import Path
from pprint import pformat
from typing import Any, Mapping, Optional, Tuple, Union
from ignite.contrib.handlers.param_scheduler import ParamScheduler

import ignite.distributed as idist
import torch
from ignite.engine import Engine
from ignite.handlers.checkpoint import Checkpoint
from ignite.utils import setup_logger
from ignite.contrib.handlers import PiecewiseLinear
from torch.nn import Module, CrossEntropyLoss
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim import Optimizer, SGD

from models import get_model
{% includes "_handlers.py" %}



def initialize(config: Optional[Any]) -> Tuple[Module, Optimizer, Module, Union[_LRScheduler, ParamScheduler]]:
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
    optimizer = SGD(
        model.parameters(),
        lr=config.lr,
        momentum=config.momentum,
        weight_decay=config.weight_decay,
        nesterov=True,
    )
    loss_fn = CrossEntropyLoss().to(idist.device())
    le = config.num_iters_per_epoch
    milestones_values = [
        (0, 0.0),
        (le * config.num_warmup_epochs, config.lr),
        (le * config.max_epochs, 0.0),
    ]
    lr_scheduler = PiecewiseLinear(optimizer, param_name="lr", milestones_values=milestones_values)
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
        `verbose` and `output_dir` attributes.

    Returns
    -------
    logger
        an instance of `Logger`
    """
    logger = setup_logger(
        level=logging.INFO if config.verbose else logging.WARNING,
        format="%(message)s",
        filepath=config.output_dir / "training-info.log",
    )
    return logger


def hash_checkpoint(
    checkpoint_fp: Union[str, Path],
    jitted: bool,
    output_path: Union[str, Path],
) -> Tuple[Path, str]:
    """Hash the checkpoint file to be used with `check_hash` of
    `torch.hub.load_state_dict_from_url`.

    Parameters
    ----------
    checkpoint_fp
        path to the checkpoint file.
    jitted
        indicate the checkpoint is already applied torch.jit or not.
    output_path
        path to store the hashed checkpoint file.

    Returns
    -------
    hashed_fp and sha_hash
        path to the hashed file and SHA hash
    """
    if isinstance(checkpoint_fp, str):
        checkpoint_fp = Path(checkpoint_fp)

    sha_hash = hashlib.sha256(checkpoint_fp.read_bytes()).hexdigest()
    ckpt_file_name = checkpoint_fp.stem

    if jitted:
        hashed_fp = "-".join((ckpt_file_name, sha_hash[:8])) + ".ptc"
    else:
        hashed_fp = "-".join((ckpt_file_name, sha_hash[:8])) + ".pt"

    if isinstance(output_path, str):
        output_path = Path(output_path)

    hashed_fp = output_path / hashed_fp
    shutil.move(checkpoint_fp, hashed_fp)
    print(f"Saved state dict into {hashed_fp} | SHA256: {sha_hash}")

    return hashed_fp, sha_hash


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
            checkpoint_fp, model_dir=model_dir, map_location="cpu", check_hash=True
        )
    else:
        if isinstance(checkpoint_fp, str):
            checkpoint_fp = Path(checkpoint_fp)

        if not checkpoint_fp.exists():
            raise FileNotFoundError(f"Given {str(checkpoint_fp)} does not exist.")
        checkpoint = torch.load(checkpoint_fp, map_location="cpu")

    Checkpoint.load_objects(to_load=to_load, checkpoint=checkpoint, strict=strict)
    logger.info("Successfully resumed from a checkpoint: %s", checkpoint_fp)
