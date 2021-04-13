import os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

import ignite
import ignite.distributed as idist
from ignite.contrib.handlers import PiecewiseLinear
from ignite.contrib.handlers.wandb_logger import WandBLogger
from ignite.engine import Events
from ignite.metrics import Accuracy, Loss
from ignite.utils import manual_seed

from config import DEFAULTS
from dataset import get_dataflow
from models import get_model
from trainers import create_trainers
from utils import (
    get_default_parser,
    thresholded_output_transform,
    setup_logging,
    log_basic_info,
    log_metrics,
    get_handlers,
    get_logger,
    resume_from,
)

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # remove tokenizer parallelism warning


def initialize(config):
    model = get_model(config.model, config.model_dir, config.dropout, config.n_fc, config.num_classes)

    config.learning_rate *= idist.get_world_size()
    # Adapt model for distributed settings if configured
    model = idist.auto_model(model)

    optimizer = optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
    optimizer = idist.auto_optim(optimizer)
    loss_fn = nn.BCEWithLogitsLoss()

    le = config.num_iters_per_epoch
    milestones_values = [
        (0, 0.0),
        (le * config.num_warmup_epochs, config.learning_rate),
        (le * config.max_epochs, 0.0),
    ]
    lr_scheduler = PiecewiseLinear(optimizer, param_name="lr", milestones_values=milestones_values)

    return model, optimizer, loss_fn, lr_scheduler


def run(local_rank, config):

    # ----------------------
    # Make a certain seed
    # ----------------------
    rank = idist.get_rank()
    manual_seed(config.seed + rank)
    device = idist.device()

    # -----------------------------
    # datasets and dataloaders
    # -----------------------------
    train_loader, test_loader = get_dataflow(config)

    # ------------------------------------------
    # model, optimizer, loss function, device
    # ------------------------------------------
    config.num_iters_per_epoch = len(train_loader)
    model, optimizer, loss_fn, lr_scheduler = initialize(config)

    # -----------------------------
    # train_engine and eval_engine
    # -----------------------------
    train_engine, eval_engine = create_trainers(
        config=config,
        model=model,
        optimizer=optimizer,
        loss_fn=loss_fn,
        device=device,
    )

    # ---------------------------------
    # attach metrics to eval_engine
    # ---------------------------------
    metrics = {
        "eval_accuracy": Accuracy(output_transform=thresholded_output_transform, device=device),
        "eval_loss": Loss(loss_fn, device=device),
    }

    for name, metric in metrics.items():
        metric.attach(eval_engine, name)

    # -------------------------------------------
    # update config with optimizer parameters
    # setup engines logger with python logging
    # print training configurations
    # -------------------------------------------
    config.__dict__.update(**optimizer.defaults)
    logger = setup_logging(config)
    log_basic_info(logger, config)
    train_engine.logger = logger
    eval_engine.logger = logger

    # -------------------------------------
    # ignite handlers and ignite loggers
    # -------------------------------------
    to_save = {"model": model, "optimizer": optimizer, "train_engine": train_engine, "lr_scheduler": lr_scheduler}
    best_model_handler, es_handler, timer_handler = get_handlers(
        config=config,
        model=model,
        train_engine=train_engine,
        eval_engine=eval_engine,
        metric_name="eval_accuracy",
        # TODO : replace with the metric name to save the best model
        # if you check `Save the best model by evaluation score` otherwise leave it None
        # metric must be in eval_engine.state.metrics.
        es_metric_name=None,
        # TODO : replace with the metric name to early stop
        # if you check `Early stop the training by evaluation score` otherwise leave it None
        # metric must be in eval_engine.state.metrics.
        to_save=to_save,
        lr_scheduler=lr_scheduler,
        output_names=None,
    )

    # setup ignite logger only on rank 0
    if rank == 0:
        logger_handler = get_logger(
            config=config, train_engine=train_engine, eval_engine=eval_engine, optimizers=optimizer
        )

    # -----------------------------------
    # resume from the saved checkpoints
    # -----------------------------------
    if config.resume_from:
        resume_from(to_load=to_save, checkpoint_fp=config.resume_from)

    # --------------------------------
    # print metrics to the stderr
    # with `add_event_handler` API
    # for training stats
    # --------------------------------
    train_engine.add_event_handler(Events.ITERATION_COMPLETED(every=config.log_every_iters), log_metrics, tag="train")

    # ---------------------------------------------
    # run evaluation at every training epoch end
    # with shortcut `on` decorator API and
    # print metrics to the stderr
    # again with `add_event_handler` API
    # for evaluation stats
    # ---------------------------------------------
    @train_engine.on(Events.EPOCH_COMPLETED(every=1))
    def _():
        eval_engine.run(test_loader, max_epochs=1)
        eval_engine.add_event_handler(Events.EPOCH_COMPLETED(every=1), log_metrics, tag="eval")

    # --------------------------------------------------
    # let's try run evaluation first as a sanity check
    # --------------------------------------------------
    @train_engine.on(Events.STARTED)
    def _():
        eval_engine.run(test_loader, max_epochs=1, epoch_length=2)
        eval_engine.state.max_epochs = None

    # ------------------------------------------
    # setup if done. let's run the training
    # ------------------------------------------
    train_engine.run(train_loader, max_epochs=config.max_epochs)

    # ------------------------------------------------------------
    # close the logger after the training completed / terminated
    # ------------------------------------------------------------
    if rank == 0:
        if isinstance(logger_handler, WandBLogger):
            # why handle differently for wandb ?
            # See : https://github.com/pytorch/ignite/issues/1894
            logger_handler.finish()
        elif logger_handler:
            logger_handler.close()

    # -----------------------------------------
    # where is my best and last checkpoint ?
    # -----------------------------------------
    logger.info("Last and best checkpoint: %s", best_model_handler.last_checkpoint)


def main():
    parser = ArgumentParser(parents=[get_default_parser(DEFAULTS)])
    config = parser.parse_args()
    manual_seed(config.seed)

    if config.output_dir:
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        name = f"{config.model}-backend-{idist.backend()}-{now}"
        path = Path(config.output_dir, name)
        path.mkdir(parents=True, exist_ok=True)
        config.output_dir = path

    with idist.Parallel(
        backend=config.backend,
        nproc_per_node=config.nproc_per_node,
        nnodes=config.nnodes,
        node_rank=config.node_rank,
        master_addr=config.master_addr,
        master_port=config.master_port,
    ) as parallel:
        parallel.run(run, config)


if __name__ == "__main__":
    main()
