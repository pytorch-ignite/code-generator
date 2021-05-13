from argparse import ArgumentParser
from pprint import pformat
from typing import Any

import ignite.distributed as idist
from data import setup_data
from ignite.engine import Events
from ignite.metrics import Accuracy, Loss
from ignite.utils import manual_seed
from model import Net
from torch import nn, optim
from torch.utils.data.distributed import DistributedSampler
from trainers import setup_evaluator, setup_trainer
from utils import *


def run(local_rank: int, config: Any):

    # make a certain seed
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    # create output folder
    config.output_dir = setup_output_dir(config, rank)

    # donwload datasets and create dataloaders
    dataloader_train, dataloader_eval = setup_data(config)

    # model, optimizer, loss function, device
    device = idist.device()
    model = idist.auto_model(Net())
    optimizer = idist.auto_optim(optim.Adam(model.parameters(), lr=config.lr))
    loss_fn = nn.CrossEntropyLoss().to(device=device)

    # trainer and evaluator
    trainer = setup_trainer(config, model, optimizer, loss_fn, device)
    evaluator = setup_evaluator(config, model, loss_fn, device)

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
    trainer.logger = evaluator.logger = logger

    # set epoch for distributed sampler
    if idist.get_world_size() > 1 and isinstance(
        dataloader_train.sampler, DistributedSampler
    ):
        dataloader_train.sampler.set_epoch(trainer.state.epoch - 1)

    # setup ignite handlers
    #::: if (it.save_model || it.save_optimizer || it.save_lr_scheduler || it.save_trainer || it.save_evaluator || it.patience || it.terminate_on_nan || it.timer || it.limit_sec) { :::#
    to_save_train = None
    to_save_eval = {"model": model}
    setup_handlers(trainer, evaluator, config, to_save_train, to_save_eval)
    #::: } :::#

    # experiment tracking
    if rank == 0:
        exp_logger = setup_exp_logging(config, trainer, optimizer, evaluator)

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
        evaluator.run(dataloader_eval, epoch_length=config.eval_epoch_length)
        log_metrics(evaluator, "eval")

    # let's try run evaluation first as a sanity check
    @trainer.on(Events.STARTED)
    def _():
        evaluator.run(dataloader_eval, epoch_length=config.eval_epoch_length)

    # setup if done. let's run the training
    trainer.run(
        dataloader_train,
        max_epochs=config.max_epochs,
        epoch_length=config.train_epoch_length,
    )

    if rank == 0:
        from ignite.contrib.handlers.wandb_logger import WandBLogger

        if isinstance(exp_logger, WandBLogger):
            # why handle differently for wandb?
            # See: https://github.com/pytorch/ignite/issues/1894
            exp_logger.finish()
        elif exp_logger:
            exp_logger.close()


# main #
def main():
    parser = ArgumentParser(parents=[get_default_parser()])
    config = parser.parse_args()

    with idist.Parallel(backend=config.backend) as parallel:
        parallel.run(run, config=config)


if __name__ == "__main__":
    main()
