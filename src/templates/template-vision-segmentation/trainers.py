from typing import Any, Dict, Union

import ignite.distributed as idist
import torch
from data import prepare_image_mask
from ignite.engine import DeterministicEngine, Engine, Events
from ignite.metrics import Metric
from torch.cuda.amp import autocast, GradScaler
from torch.nn import Module
from torch.optim import Optimizer
from torch.utils.data import DistributedSampler, Sampler
from utils import model_output_transform


def setup_trainer(
    config: Any,
    model: Module,
    optimizer: Optimizer,
    loss_fn: Module,
    device: Union[str, torch.device],
    train_sampler: Sampler,
) -> Union[Engine, DeterministicEngine]:
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

    #
    #::: if(it.deterministic) { :::#
    trainer = DeterministicEngine(train_function)
    #::: } else { :::#
    trainer = Engine(train_function)
    #::: } :::#

    # set epoch for distributed sampler
    @trainer.on(Events.EPOCH_STARTED)
    def set_epoch():
        if idist.get_world_size() > 1 and isinstance(train_sampler, DistributedSampler):
            train_sampler.set_epoch(trainer.state.epoch - 1)

    return trainer


def setup_evaluator(
    config: Any,
    model: Module,
    metrics: Dict[str, Metric],
    device: Union[str, torch.device],
) -> Engine:
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
