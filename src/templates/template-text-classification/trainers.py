from typing import Any, Dict, Union

import torch
from ignite.engine import DeterministicEngine, Engine
from ignite.metrics.metric import Metric
from torch import nn
from torch.cuda.amp import GradScaler, autocast
from torch.optim.optimizer import Optimizer


def setup_trainer(
    config: Any,
    model: nn.Module,
    optimizer: Optimizer,
    loss_fn: nn.Module,
    device: Union[str, torch.device],
) -> Union[Engine, DeterministicEngine]:

    scaler = GradScaler(enabled=config.use_amp)

    def train_function(engine: Union[Engine, DeterministicEngine], batch: Any):
        input_ids = batch["input_ids"].to(
            device, non_blocking=True, dtype=torch.long
        )
        attention_mask = batch["attention_mask"].to(
            device, non_blocking=True, dtype=torch.long
        )
        token_type_ids = batch["token_type_ids"].to(
            device, non_blocking=True, dtype=torch.long
        )
        labels = (
            batch["label"]
            .view(-1, 1)
            .to(device, non_blocking=True, dtype=torch.float)
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

    #::: if(it.deterministic) { :::#
    return DeterministicEngine(train_function)
    #::: } else { :::#
    return Engine(train_function)
    #::: } :::#


def setup_evaluator(
    config: Any,
    model: nn.Module,
    metrics: Dict[str, Metric],
    device: Union[str, torch.device],
):
    @torch.no_grad()
    def evalutate_function(engine: Engine, batch: Any):
        model.eval()

        input_ids = batch["input_ids"].to(
            device, non_blocking=True, dtype=torch.long
        )
        attention_mask = batch["attention_mask"].to(
            device, non_blocking=True, dtype=torch.long
        )
        token_type_ids = batch["token_type_ids"].to(
            device, non_blocking=True, dtype=torch.long
        )
        labels = (
            batch["label"]
            .view(-1, 1)
            .to(device, non_blocking=True, dtype=torch.float)
        )

        with autocast(enabled=config.use_amp):
            output = model(input_ids, attention_mask, token_type_ids)

        return output, labels

    evaluator = Engine(evalutate_function)

    for name, metric in metrics.items():
        metric.attach(evaluator, name)

    return evaluator
