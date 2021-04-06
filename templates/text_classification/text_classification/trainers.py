from pathlib import Path

import torch
from torch.cuda.amp import GradScaler, autocast

import ignite.distributed as idist
from ignite.contrib.engines import common
from ignite.engine import Engine
from ignite.handlers import Checkpoint

from utils import get_save_handler


def create_trainer(model, optimizer, criterion, lr_scheduler, train_sampler, config, logger):

    device = idist.device()

    # Setup Ignite trainer:
    # - let's define training step
    # - add other common handlers:
    #    - TerminateOnNan,
    #    - handler to setup learning rate scheduling,
    #    - ModelCheckpoint
    #    - RunningAverage` on `train_step` output
    #    - Two progress bars on epochs and optionally on iterations

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
            loss = criterion(y_pred, labels)

        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        return {
            "batch loss": loss.item(),
        }

    trainer = Engine(train_step)
    trainer.logger = logger

    to_save = {"trainer": trainer, "model": model, "optimizer": optimizer, "lr_scheduler": lr_scheduler}
    metric_names = [
        "batch loss",
    ]
    if config.log_every_iters == 0:
        # Disable logging training metrics:
        metric_names = None
        config.log_every_iters = 15

    common.setup_common_training_handlers(
        trainer=trainer,
        train_sampler=train_sampler,
        to_save=to_save,
        save_every_iters=config.checkpoint_every,
        save_handler=get_save_handler(config),
        lr_scheduler=lr_scheduler,
        output_names=metric_names,
        log_every_iters=config.log_every_iters,
        with_pbars=not config.with_clearml,
        clear_cuda_cache=False,
    )

    resume_from = config.resume_from
    if resume_from is not None:
        checkpoint_fp = Path(resume_from)
        assert checkpoint_fp.exists(), f"Checkpoint '{checkpoint_fp.as_posix()}' is not found"
        logger.info(f"Resume from a checkpoint: {checkpoint_fp.as_posix()}")
        checkpoint = torch.load(checkpoint_fp.as_posix(), map_location="cpu")
        Checkpoint.load_objects(to_load=to_save, checkpoint=checkpoint)

    return trainer


def create_evaluator(model, metrics, config, tag="val"):
    use_amp = config.use_amp
    device = idist.device()

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
            output = model(input_ids, attention_mask, token_type_ids)
        return output, labels

    evaluator = Engine(evaluate_step)

    for name, metric in metrics.items():
        metric.attach(evaluator, name)

    if idist.get_rank() == 0 and (not config.with_clearml):
        common.ProgressBar(desc=f"Evaluation ({tag})", persist=False).attach(evaluator)

    return evaluator
