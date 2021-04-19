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

from datasets import get_datasets
from trainers import create_trainers, TrainEvents
from utils import setup_logging, log_metrics, log_basic_info, initialize, resume_from, get_handlers, get_logger
from config import get_default_parser


def run(local_rank: int, config: Any, *args: Any, **kwargs: Any):
    """function to be run by idist.Parallel context manager."""

    # ----------------------
    # make a certain seed
    # ----------------------
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    # -----------------------
    # create output folder
    # -----------------------

    if rank == 0:
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        name = f"{config.dataset}-backend-{idist.backend()}-{now}"
        path = Path(config.output_dir, name)
        path.mkdir(parents=True, exist_ok=True)
        config.output_dir = path.as_posix()

    config.output_dir = Path(idist.broadcast(config.output_dir, src=0))

    # -----------------------------
    # datasets and dataloaders
    # -----------------------------
    # TODO : PLEASE provide your custom datasets and dataloaders configurations
    # we can use `idist.auto_dataloader` to handle distributed configurations
    # TODO : PLEASE replace `kwargs` with your desirable DataLoader arguments
    # See : https://pytorch.org/ignite/distributed.html#ignite.distributed.auto.auto_dataloader

    train_dataset, eval_dataset = get_datasets()

    train_dataloader = idist.auto_dataloader(train_dataset, **kwargs)
    eval_dataloader = idist.auto_dataloader(eval_dataset, **kwargs)

    # ------------------------------------------
    # model, optimizer, loss function, device
    # ------------------------------------------

    device = idist.device()
    model, optimizer, loss_fn, lr_scheduler = initialize()

    # -----------------------------
    # trainer and evaluator
    # -----------------------------

    trainer, evaluator = create_trainers(
        config=config,
        model=model,
        optimizer=optimizer,
        loss_fn=loss_fn,
        device=device,
    )

    # -------------------------------------------
    # update config with optimizer parameters
    # setup engines logger with python logging
    # print training configurations
    # -------------------------------------------

    config.__dict__.update(**optimizer.defaults)
    logger = setup_logging(config)
    log_basic_info(logger, config)
    trainer.logger = logger
    evaluator.logger = logger

    # -------------------------------------
    # ignite handlers and ignite loggers
    # -------------------------------------

    to_save = {"model": model, "optimizer": optimizer, "trainer": trainer, "lr_scheduler": lr_scheduler}
    best_model_handler, es_handler, timer_handler = get_handlers(
        config=config,
        model=model,
        trainer=trainer,
        evaluator=evaluator,
        metric_name=None,
        # TODO : replace with the metric name to save the best model
        # if you check `Save the best model by evaluation score` otherwise leave it None
        # metric must be in evaluator.state.metrics.
        es_metric_name=None,
        # TODO : replace with the metric name to early stop
        # if you check `Early stop the training by evaluation score` otherwise leave it None
        # metric must be in evaluator.state.metrics.
        to_save=to_save,
        lr_scheduler=lr_scheduler,
        output_names=None,
    )

    # setup ignite logger only on rank 0
    if rank == 0:
        logger_handler = get_logger(
            config=config, trainer=trainer, evaluator=evaluator, optimizers=optimizer
        )

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

    @trainer.on(TrainEvents.BACKWARD_COMPLETED(lambda _, ev: (ev % 100 == 0) or (ev == 1)))
    def _():
        # do something interesting
        pass

    # ----------------------------------------
    # here we will use `every` to trigger
    # every 100 iterations
    # ----------------------------------------

    @trainer.on(TrainEvents.OPTIM_STEP_COMPLETED(every=100))
    def _():
        # do something interesting
        pass

    # --------------------------------
    # print metrics to the stderr
    # with `add_event_handler` API
    # for training stats
    # --------------------------------

    trainer.add_event_handler(Events.ITERATION_COMPLETED(every=config.log_every_iters), log_metrics, tag="train")

    # ---------------------------------------------
    # run evaluation at every training epoch end
    # with shortcut `on` decorator API and
    # print metrics to the stderr
    # again with `add_event_handler` API
    # for evaluation stats
    # ---------------------------------------------

    @trainer.on(Events.EPOCH_COMPLETED(every=1))
    def _():
        evaluator.run(eval_dataloader, epoch_length=config.eval_epoch_length)
        log_metrics(evaluator, "eval")

    # --------------------------------------------------
    # let's try run evaluation first as a sanity check
    # --------------------------------------------------

    @trainer.on(Events.STARTED)
    def _():
        evaluator.run(eval_dataloader, epoch_length=2)
        evaluator.state.max_epochs = None

    # ------------------------------------------
    # setup if done. let's run the training
    # ------------------------------------------
    # TODO : PLEASE provide `max_epochs` parameters

    trainer.run(train_dataloader, max_epochs=config.max_epochs, epoch_length=config.train_epoch_length)

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

    if best_model_handler is not None:
        logger.info("Last and best checkpoint: %s", best_model_handler.last_checkpoint)


def main():
    parser = ArgumentParser(parents=[get_default_parser()])
    config = parser.parse_args()

    with idist.Parallel(
        backend=config.backend,
{% if use_distributed_training and not use_distributed_launcher %}
        nproc_per_node=config.nproc_per_node,
{% if nnodes > 1 and not use_distributed_launcher%}
        node_rank=config.node_rank,
        nnodes=config.nnodes,
        master_addr=config.master_addr,
        master_port=config.master_port,
{% endif %}
{% endif %}
    ) as parallel:
        parallel.run(run, config=config)


if __name__ == "__main__":
    main()
