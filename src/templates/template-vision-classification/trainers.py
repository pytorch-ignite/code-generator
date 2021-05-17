from typing import Any, Union

import torch
from ignite.engine import DeterministicEngine, Engine
from torch.cuda.amp import autocast
from torch.nn import Module
from torch.optim import Optimizer


def setup_trainer(
    config: Any,
    model: Module,
    optimizer: Optimizer,
    loss_fn: Module,
    device: Union[str, torch.device],
) -> Union[Engine, DeterministicEngine]:
    def train_function(engine: Union[Engine, DeterministicEngine], batch: Any):
        model.train()

        samples = batch[0].to(device, non_blocking=True)
        targets = batch[1].to(device, non_blocking=True)

        with autocast(config.use_amp):
            outputs = model(samples)
            loss = loss_fn(outputs, targets)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        train_loss = loss.item()
        engine.state.metrics = {
            "epoch": engine.state.epoch,
            "train_loss": train_loss,
        }
        return {"train_loss": train_loss}

    #::: if(it.deterministic) { :::#
    return DeterministicEngine(train_function)
    #::: } else { :::#
    return Engine(train_function)
    #::: } :::#


def setup_evaluator(
    config: Any,
    model: Module,
    device: Union[str, torch.device],
) -> Engine:
    @torch.no_grad()
    def eval_function(engine: Engine, batch: Any):
        model.eval()

        samples = batch[0].to(device, non_blocking=True)
        targets = batch[1].to(device, non_blocking=True)

        with autocast(config.use_amp):
            outputs = model(samples)

        return outputs, targets

    return Engine(eval_function)
