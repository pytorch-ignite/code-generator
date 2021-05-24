from typing import Any, Union

import torch
from data import prepare_image_mask
from ignite.engine import DeterministicEngine, Engine
from torch.cuda.amp import GradScaler, autocast
from torch.nn import Module
from torch.optim import Optimizer
from utils import model_output_transform


def setup_trainer(
    config: Any,
    model: Module,
    optimizer: Optimizer,
    loss_fn: Module,
    device: Union[str, torch.device],
):

    prepare_batch = prepare_image_mask
    scaler = GradScaler(enabled=config.use_amp)

    def train_function(engine: Engine, batch: Any):
        model.train()
        x, y = prepare_batch(batch, device, True)

        with autocast(config.use_amp):
            y_pred = model(x)
            y_pred = model_output_transform(y_pred)
            loss = loss_fn(y_pred, y) / config.accumulation_steps

        scaler.scale(loss).backward()
        if engine.state.iteration % config.accumulation_steps == 0:
            scaler.step(optimizer)
            scaler.update()
            optimizer.zero_grad()

        metric = {"epoch": engine.state.epoch, "train_loss": loss.item()}
        engine.state.metrics = metric
        return metric

    #::: if(it.deterministic) { :::#
    return DeterministicEngine(train_function)
    #::: } else { :::#
    return Engine(train_function)
    #::: } :::#


def setup_evaluator(
    config: Any, model: Module, metrics: dict, device: Union[str, torch.device]
):
    prepare_batch = prepare_image_mask

    @torch.no_grad()
    def evaluation_function(engine: Engine, batch: Any):
        model.eval()

        x, y = prepare_batch(batch, device, True)
        with autocast(config.use_amp):
            y_pred = model(x)
            y_pred = model_output_transform(y_pred)

        return y_pred, y

    evaluator = Engine(evaluation_function)

    for name, metric in metrics.items():
        metric.attach(evaluator, name)

    return evaluator
