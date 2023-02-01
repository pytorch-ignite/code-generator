from typing import Any, Dict, Union

import ignite.distributed as idist
import torch
from ignite.engine import DeterministicEngine, Engine, Events
from ignite.metrics.metric import Metric
from torch import nn
from torch.cuda.amp import autocast, GradScaler
from torch.optim.optimizer import Optimizer
from torch.utils.data import DistributedSampler, Sampler


def setup_trainer(
    config: Any,
    model: nn.Module,
    optimizer: Optimizer,
    loss_fn: nn.Module,
    device: Union[str, torch.device],
    train_sampler: Sampler,
) -> Union[Engine, DeterministicEngine]:

    scaler = GradScaler(enabled=config.use_amp)

    def train_function(engine: Union[Engine, DeterministicEngine], batch: Any):
        input_ids = batch["input_ids"].to(device, non_blocking=True, dtype=torch.long)
        attention_mask = batch["attention_mask"].to(
            device, non_blocking=True, dtype=torch.long
        )
        token_type_ids = batch["token_type_ids"].to(
            device, non_blocking=True, dtype=torch.long
        )
        labels = (
            batch["label"].view(-1, 1).to(device, non_blocking=True, dtype=torch.float)
        )

        model.train()

        with autocast(enabled=config.use_amp):
            y_pred = model(input_ids, attention_mask, token_type_ids)
            loss = loss_fn(y_pred, labels)

        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        metric = {"train_loss": loss.item()}
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
    model: nn.Module,
    metrics: Dict[str, Metric],
    device: Union[str, torch.device],
):
    @torch.no_grad()
    def evalutate_function(engine: Engine, batch: Any):
        model.eval()

        input_ids = batch["input_ids"].to(device, non_blocking=True, dtype=torch.long)
        attention_mask = batch["attention_mask"].to(
            device, non_blocking=True, dtype=torch.long
        )
        token_type_ids = batch["token_type_ids"].to(
            device, non_blocking=True, dtype=torch.long
        )
        labels = (
            batch["label"].view(-1, 1).to(device, non_blocking=True, dtype=torch.float)
        )

        with autocast(enabled=config.use_amp):
            output = model(input_ids, attention_mask, token_type_ids)

        return output, labels

    evaluator = Engine(evalutate_function)

    for name, metric in metrics.items():
        metric.attach(evaluator, name)

    return evaluator
