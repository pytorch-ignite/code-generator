"""
`train_engine` and `eval_engine` like trainer and evaluator
"""
from typing import Any, Tuple
import torch
from ignite.engine import Engine
from torch.optim.optimizer import Optimizer

from single_cg.events import TrainEvents, train_events_to_attr


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

    loss.backward()
    engine.state.backward_completed += 1
    engine.fire_event(TrainEvents.BACKWARD_COMPLETED)

    optimizer.step()
    engine.state.optim_step_completed += 1
    engine.fire_event(TrainEvents.OPTIM_STEP_COMPLETED)

    optimizer.zero_grad()

    loss_value = loss.item()
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
    train_engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    return train_engine, eval_engine
