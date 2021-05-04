### imports ###
from typing import Any, Tuple

import torch
from ignite.engine import Engine
from torch.cuda.amp import autocast
from torch.optim.optimizer import Optimizer

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
) -> dict:
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
    training loss dict
    """

    model.train()

    samples = batch[0].to(device, non_blocking=True)
    targets = batch[1].to(device, non_blocking=True)

    with autocast(enabled=config.use_amp):
        outputs = model(samples)
        loss = loss_fn(outputs, targets)

    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    loss_value = loss.item()
    engine.state.metrics = {
        "epoch": engine.state.epoch,
        "train_loss": loss_value,
    }
    return {"train_loss": loss_value}


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
    device: torch.device,
) -> Tuple[torch.Tensor]:
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
    device
        device to use for training

    Returns
    -------
    outputs, targets
    """

    model.eval()

    samples = batch[0].to(device, non_blocking=True)
    targets = batch[1].to(device, non_blocking=True)

    with autocast(enabled=config.use_amp):
        outputs = model(samples)

    return outputs, targets


# function for creating engines which will be used in main.py
# any necessary arguments can be provided.
def create_trainers(
    config, model, optimizer, loss_fn, device
) -> Tuple[Engine, Engine]:
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
            device=device,
        )
    )
    evaluator = Engine(
        lambda e, b: evaluate_function(
            config=config, engine=e, batch=b, model=model, device=device
        )
    )
    return trainer, evaluator
