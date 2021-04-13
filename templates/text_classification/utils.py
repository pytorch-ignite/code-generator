from typing import Any, Mapping, Optional, Tuple, Union
from pathlib import Path
from pprint import pformat
from argparse import ArgumentParser
import logging

import torch

import ignite
from ignite.engine import Engine
import ignite.distributed as idist
from ignite.handlers.checkpoint import Checkpoint
from ignite.utils import setup_logger
{% include "_handlers.py" %}


def thresholded_output_transform(output):
    y_pred, y = output
    return torch.round(torch.sigmoid(y_pred)), y


def setup_logging(config: Any) -> logging.Logger:
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
    green = "\033[32m"
    reset = "\033[0m"
    logger = setup_logger(
        name=f"{green}[ignite]{reset}",
        level=logging.INFO if config.verbose else logging.WARNING,
        format="%(name)s: %(message)s",
        filepath=config.output_dir / "training-info.log",
    )
    return logger


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


def log_basic_info(logger: logging.Logger, config: Any) -> None:
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

    logger.info("PyTorch version: %s", torch.__version__)
    logger.info("Ignite version: %s", ignite.__version__)
    if torch.cuda.is_available():
        # explicitly import cudnn as
        # torch.backends.cudnn can not be pickled with hvd spawning procs
        from torch.backends import cudnn

        logger.info("GPU device: %s", torch.cuda.get_device_name(idist.get_local_rank()))
        logger.info("CUDA version: %s", torch.version.cuda)
        logger.info("CUDNN version: %s", cudnn.version())

    logger.info("Configuration: %s", pformat(vars(config)))

    if idist.get_world_size() > 1:
        logger.info("distributed configuration: %s", idist.model_name())
        logger.info("backend: %s", idist.backend())
        logger.info("device: %s", idist.device().type)
        logger.info("hostname: %s", idist.hostname())
        logger.info("world size: %s", idist.get_world_size())
        logger.info("rank: %s", idist.get_rank())
        logger.info("local rank: %s", idist.get_local_rank())
        logger.info("num processes per node: %s", idist.get_nproc_per_node())
        logger.info("num nodes: %s", idist.get_nnodes())
        logger.info("node rank: %s", idist.get_node_rank())


def get_default_parser(defaults):
    parser = ArgumentParser(add_help=False)

    for key, value in defaults.items():
        parser.add_argument(f"--{key}", **value)

    return parser


def resume_from(
    to_load: Mapping,
    checkpoint_fp: Union[str, Path],
    logger: logging.Logger,
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
