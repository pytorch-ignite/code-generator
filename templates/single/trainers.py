"""
`trainer` and `evaluator` like trainer and evaluator
"""
from typing import Any, Tuple

import torch
from ignite.engine import Engine
from torch.cuda.amp import autocast
from torch.optim.optimizer import Optimizer

{% include "_events.py" %}


# Edit below functions the way how the model will be training

# train_function is how the model will be learning with given batch
# below in the train_function, common parameters are provided
# you can add any additional parameters depending on the training
# NOTE : engine and batch parameters are needed to work with
# Ignite's Engine.
# TODO: Extend with your custom training.
def train_function(
    config: Any,
    engine: Engine,
    batch: Any,
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizer: Optimizer,
    device: torch.device,
):
    """Model training step.

    Parameters
    ----------
    config
        config object
    engine
        Engine instance
    batch
        batch in current iteration
    model
        nn.Module model
    loss_fn
        nn.Module loss
    optimizer
        torch optimizer
    device
        device to use for training

    Returns
    -------
    {INSERT HERE}
    """

    model.train()

    samples = batch[0].to(device, non_blocking=True)
    targets = batch[1].to(device, non_blocking=True)

    with autocast(enabled=config.use_amp):
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


# evaluate_function is how the model will be learning with given batch
# below in the evaluate_function, common parameters are provided
# you can add any additional parameters depending on the training
# NOTE : engine and batch parameters are needed to work with
# Ignite's Engine.
# TODO: Extend with your custom evaluation.
@torch.no_grad()
def evaluate_function(
    config: Any,
    engine: Engine,
    batch: Any,
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    device: torch.device,
):
    """Model evaluating step.

    Parameters
    ----------
    config
        config object
    engine
        Engine instance
    batch
        batch in current iteration
    model
        nn.Module model
    loss_fn
        nn.Module loss
    device
        device to use for training

    Returns
    -------
    {INSERT HERE}
    """

    model.eval()

    samples = batch[0].to(device, non_blocking=True)
    targets = batch[1].to(device, non_blocking=True)

    with autocast(enabled=config.use_amp):
        outputs = model(samples)
        loss = loss_fn(outputs, targets)

    loss_value = loss.item()
    engine.state.metrics = {"eval_loss": loss_value}
    return loss_value


# function for creating engines which will be used in main.py
# any necessary arguments can be provided.
def create_trainers(config, model, optimizer, loss_fn, device) -> Tuple[Engine, Engine]:
    """Create Engines for training and evaluation.

    Parameters
    ----------
    config
        config object
    model
        nn.Module model
    loss_fn
        nn.Module loss
    optimizer
        torch optimizer
    device
        device to use for training

    Returns
    -------
    trainer, evaluator
    """
    trainer = Engine(
        lambda e, b: train_function(
            config=config,
            engine=e,
            batch=b,
            model=model,
            loss_fn=loss_fn,
            optimizer=optimizer,
            device=device
        )
    )
    evaluator = Engine(
        lambda e, b: evaluate_function(
            config=config,
            engine=e,
            batch=b,
            model=model,
            device=device
        )
    )
    trainer.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    return trainer, evaluator
