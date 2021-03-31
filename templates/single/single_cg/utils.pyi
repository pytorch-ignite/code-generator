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
from typing import Any, Tuple, Union

from ignite.engine import Engine
from ignite.utils import setup_logger

{% include "_argparse.pyi" %}


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
        tag,
        engine.state.epoch,
        engine.state.iteration,
        engine.state.metrics
    )
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
