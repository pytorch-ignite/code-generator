"""
main entrypoint training
"""
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Any
from ignite.contrib.handlers.wandb_logger import WandBLogger

import ignite.distributed as idist
from ignite.engine.events import Events
from ignite.utils import manual_seed
from ignite.metrics import Accuracy, Loss

from datasets import get_datasets
from trainers import create_trainers, TrainEvents
from handlers import get_handlers, get_logger
from utils import setup_logging, log_metrics, log_basic_info, initialize, resume_from
from config import get_default_parser


def run(local_rank: int, config: Any, *args: Any, **kwargs: Any):
    """function to be run by idist.Parallel context manager."""

    # -----------------------------
    # datasets and dataloaders
    # -----------------------------
    # TODO : PLEASE provide your custom datasets and dataloaders configurations
    # we can use `idist.auto_dataloader` to handle distributed configurations
    # TODO : PLEASE replace `kwargs` with your desirable DataLoader arguments
    # See : https://pytorch.org/ignite/distributed.html#ignite.distributed.auto.auto_dataloader

    train_dataset, eval_dataset = get_datasets(path=config.data_path)
    train_dataloader = idist.auto_dataloader(
        train_dataset,
        batch_size=config.train_batch_size,
        num_workers=config.num_workers,
        shuffle=True,
    )
    eval_dataloader = idist.auto_dataloader(
        eval_dataset,
        batch_size=config.eval_batch_size,
        num_workers=config.num_workers,
        shuffle=False,
    )

    # ------------------------------------------
    # model, optimizer, loss function, device
    # ------------------------------------------

    device = idist.device()
    config.num_iters_per_epoch = len(train_dataloader)
    model, optimizer, loss_fn, lr_scheduler = initialize(config=config)

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
    accuracy = Accuracy(device=device)
    metrics = {
        "eval_accuracy": accuracy,
        "eval_loss": Loss(loss_fn, device=device),
        "eval_error": (1.0 - accuracy) * 100,
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
    logger_handler = get_logger(config=config, train_engine=train_engine, eval_engine=eval_engine, optimizers=optimizer)

    # -----------------------------------
    # resume from the saved checkpoints
    # -----------------------------------

    if config.resume_from:
        resume_from(to_load=to_save, checkpoint_fp=config.resume_from)

    # --------------------------------------------
    # let's trigger custom events we registered
    # we will use a `event_filter` to trigger that
    # `event_filter` has to return boolean
    # whether this event should be executed
    # here will log the gradients on the 1st iteration
    # and every 100 iterations
    # --------------------------------------------

    @train_engine.on(TrainEvents.BACKWARD_COMPLETED(lambda _, ev: (ev % 100 == 0) or (ev == 1)))
    def _():
        # do something interesting
        pass

    # ----------------------------------------
    # here we will use `every` to trigger
    # every 100 iterations
    # ----------------------------------------

    @train_engine.on(TrainEvents.OPTIM_STEP_COMPLETED(every=100))
    def _():
        # do something interesting
        pass

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
        eval_engine.run(eval_dataloader, max_epochs=1)
        eval_engine.add_event_handler(Events.EPOCH_COMPLETED(every=1), log_metrics, tag="eval")

    # --------------------------------------------------
    # let's try run evaluation first as a sanity check
    # --------------------------------------------------

    @train_engine.on(Events.STARTED)
    def _():
        eval_engine.run(eval_dataloader, max_epochs=1, epoch_length=2)
        eval_engine.state.max_epochs = None

    # ------------------------------------------
    # setup if done. let's run the training
    # ------------------------------------------

    train_engine.run(train_dataloader, max_epochs=config.max_epochs)

    # ------------------------------------------------------------
    # close the logger after the training completed / terminated
    # ------------------------------------------------------------

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
    parser = ArgumentParser(parents=[get_default_parser()])
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
        parallel.run(run, config=config)


if __name__ == "__main__":
    main()
