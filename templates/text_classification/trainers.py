from typing import Any, Tuple

import ignite.distributed as idist
import torch
from ignite.engine import Engine
from torch.cuda.amp import GradScaler, autocast


def create_trainer(config, model, optimizer, loss_fn, device):

    use_amp = config.use_amp
    scaler = GradScaler(enabled=use_amp)

    def train_step(engine, batch):

        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        token_type_ids = batch["token_type_ids"]
        labels = batch["label"].view(-1, 1)

        if input_ids.device != device:
            input_ids = input_ids.to(device, non_blocking=True, dtype=torch.long)
            attention_mask = attention_mask.to(device, non_blocking=True, dtype=torch.long)
            token_type_ids = token_type_ids.to(device, non_blocking=True, dtype=torch.long)
            labels = labels.to(device, non_blocking=True, dtype=torch.float)

        model.train()

        with autocast(enabled=use_amp):
            y_pred = model(input_ids, attention_mask, token_type_ids)
            loss = loss_fn(y_pred, labels)

        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        loss_value = loss.item()
        engine.state.metrics = {"epoch": engine.state.epoch, "train_loss": loss_value}
        return loss_value

    trainer = Engine(train_step)
    return trainer


def create_evaluator(config, model, loss_fn, device):
    use_amp = config.use_amp

    @torch.no_grad()
    def evaluate_step(engine, batch):
        model.eval()
        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]
        token_type_ids = batch["token_type_ids"]
        labels = batch["label"].view(-1, 1)

        if input_ids.device != device:
            input_ids = input_ids.to(device, non_blocking=True, dtype=torch.long)
            attention_mask = attention_mask.to(device, non_blocking=True, dtype=torch.long)
            token_type_ids = token_type_ids.to(device, non_blocking=True, dtype=torch.long)
            labels = labels.to(device, non_blocking=True, dtype=torch.float)

        with autocast(enabled=use_amp):
            outputs = model(input_ids, attention_mask, token_type_ids)
            loss = loss_fn(outputs, labels)

        loss_value = loss.item()
        engine.state.metrics = {"eval_loss": loss_value}
        return outputs, labels

    evaluator = Engine(evaluate_step)
    return evaluator


# function for creating engines which will be used in main.py
# any necessary arguments can be provided.
def create_trainers(config, model, optimizer, loss_fn, device) -> Tuple[Engine, Engine]:
    """Create Engines for training and evaluation.

    Returns
    -------
    trainer, evaluator
    """
    trainer = create_trainer(config, model, optimizer, loss_fn, device)
    evaluator = create_evaluator(config, model, loss_fn, device)
    return trainer, evaluator
