### imports ###
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from pprint import pformat
from typing import Any

import ignite.distributed as idist
from datasets import get_datasets
from ignite.engine.events import Events
from ignite.metrics import Accuracy, Loss
from ignite.utils import manual_seed
from trainers import create_trainers
from utils import (get_default_parser, initialize, log_metrics, resume_from,
                   setup_logging)


### run ###
def run(local_rank: int, config: Any):

    # make a certain seed
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    # create output folder
    if rank == 0:
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        name = f"{config.model}-backend-{idist.backend()}-{now}"
        path = Path(config.output_dir, name)
        path.mkdir(parents=True, exist_ok=True)
        config.output_dir = path.as_posix()

    config.output_dir = Path(idist.broadcast(config.output_dir, src=0))

    # datasets and dataloaders
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

    # model, optimizer, loss function, device
    device = idist.device()
    model, optimizer, loss_fn, lr_scheduler = initialize(config=config)

    # trainer and evaluator
    trainer, evaluator = create_trainers(
        config=config,
        model=model,
        optimizer=optimizer,
        loss_fn=loss_fn,
        device=device,
    )

    # attach metrics to evaluator
    accuracy = Accuracy(device=device)
    metrics = {
        "eval_accuracy": accuracy,
        "eval_loss": Loss(loss_fn, device=device),
        "eval_error": (1.0 - accuracy) * 100,
    }
    for name, metric in metrics.items():
        metric.attach(evaluator, name)

    # setup engines logger with python logging
    # print training configurations
    logger = setup_logging(config)
    logger.info("Configuration: %s", pformat(vars(config)))
    trainer.logger = logger
    evaluator.logger = logger

    # ignite handlers and ignite loggers
    ### checkpointing ###
    from utils import checkpointing

    to_save_train = {}
    to_save_eval = {"model": model}
    ckpt_handler_train, ckpt_handler_eval = checkpointing(
        to_save_train, to_save_eval, config
    )
    trainer.add_event_handler(
        Events.ITERATION_COMPLETED(every=config.log_every_iters),
        ckpt_handler_train,
    )
    evaluator.add_event_handler(
        Events.EPOCH_COMPLETED(every=1), ckpt_handler_eval
    )

    ### exp_logger ###
    # setup experiment tracking logger only on rank 0
    if rank == 0:
        pass

    # resume from the saved checkpoints
    if config.resume_from:
        resume_from(to_load=to_save_train, checkpoint_fp=config.resume_from)

    # print metrics to the stderr
    # with `add_event_handler` API
    # for training stats
    trainer.add_event_handler(
        Events.ITERATION_COMPLETED(every=config.log_every_iters),
        log_metrics,
        tag="train",
    )

    # run evaluation at every training epoch end
    # with shortcut `on` decorator API and
    # print metrics to the stderr
    # again with `add_event_handler` API
    # for evaluation stats
    @trainer.on(Events.EPOCH_COMPLETED(every=1))
    def _():
        evaluator.run(eval_dataloader, epoch_length=config.eval_epoch_length)
        log_metrics(evaluator, "eval")

    # let's try run evaluation first as a sanity check
    @trainer.on(Events.STARTED)
    def _():
        evaluator.run(eval_dataloader, epoch_length=config.eval_epoch_length)

    # setup if done. let's run the training
    trainer.run(
        train_dataloader,
        max_epochs=config.max_epochs,
        epoch_length=config.train_epoch_length,
    )

    # close the logger after the training completed / terminated
    # if rank == 0:
    #     from ignite.contrib.handlers.wandb_logger import WandBLogger

    #     if isinstance(logger_handler, WandBLogger):
    #         # why handle differently for wandb ?
    #         # See : https://github.com/pytorch/ignite/issues/1894
    #         logger_handler.finish()
    #     elif logger_handler:
    #         logger_handler.close()


### main ###
def main():
    parser = ArgumentParser(parents=[get_default_parser()])
    config = parser.parse_args()

    with idist.Parallel(backend=config.backend) as parallel:
        parallel.run(run, config=config)


if __name__ == "__main__":
    main()
