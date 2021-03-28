"""
`train_engine` and `eval_engine`
"""
from typing import Any, Tuple
import torch
from ignite.engine import Engine
from torch.optim.optimizer import Optimizer


# Edit below functions the way how the model will be training

# train_fn is how the model will be learning with given batch
# below in the train_fn, common parameters are provided
# you can add any additional parameters depending on the training
# NOTE : engine and batch parameters are needed to work with
# Ignite's Engine.
# TODO: Extend with your custom training.
def train_fn(
    config: Any,
    engine: Engine,
    batch: Any,
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizer: Optimizer,
    device: torch.device,
):
    """Training.

    Parameters
    ----------
    - config: config object
    - engine: Engine instance
    - batch: batch in current iteration
    - model: nn.Module model
    - loss_fn: nn.Module loss
    - optimizer: torch optimizer
    - device: device to use for training

    Returns
    -------
    {INSERT HERE}
    """

    model.train()

    samples = batch[0].to(device, non_blocking=True)
    targets = batch[1].to(device, non_blocking=True)

    outputs = model(samples)
    loss = loss_fn(outputs, targets)
    loss_value = loss.item()

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    engine.state.metrics = {"epoch": engine.state.epoch, "train_loss": loss_value}
    return loss_value


# evaluate_fn is how the model will be learning with given batch
# below in the evaluate_fn, common parameters are provided
# you can add any additional parameters depending on the training
# NOTE : engine and batch parameters are needed to work with
# Ignite's Engine.
# TODO: Extend with your custom evaluation.
@torch.no_grad()
def evaluate_fn(
    config: Any,
    engine: Engine,
    batch: Any,
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    device: torch.device,
):
    """Evaluating.

    Parameters
    ----------
    - config: config object
    - engine: Engine instance
    - batch: batch in current iteration
    - model: nn.Module model
    - loss_fn: nn.Module loss
    - device: device to use for training

    Returns
    -------
    {INSERT HERE}
    """

    model.eval()

    samples = batch[0].to(device, non_blocking=True)
    targets = batch[1].to(device, non_blocking=True)

    outputs = model(samples)
    loss = loss_fn(outputs, targets)
    loss_value = loss.item()

    engine.state.metrics = {"eval_loss": loss_value}
    return loss_value


# function for creating engines which will be used in main.py
# any necessary arguments can be provided.
def create_engines(**kwargs) -> Tuple[Engine, Engine]:
    """Create Engines for training and evaluation.

    Parameters
    ----------
    kwargs: keyword arguments passed to both train_fn and evaluate_fn

    Returns
    -------
    train_engine, eval_engine
    """
    train_engine = Engine(
        lambda e, b: train_fn(
            engine=e,
            batch=b,
            **kwargs,
        )
    )
    eval_engine = Engine(
        lambda e, b: evaluate_fn(
            engine=e,
            batch=b,
            **kwargs,
        )
    )
    return train_engine, eval_engine
