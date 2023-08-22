import os
from pprint import pformat
from typing import Any

import ignite.distributed as idist
from data import setup_data
from ignite.engine import Events
from ignite.handlers import PiecewiseLinear
from ignite.metrics import Accuracy, Loss
from ignite.utils import manual_seed
from models import TransformerModel
from torch import nn, optim
from trainers import setup_evaluator, setup_trainer
from utils import *

#::: if ((it.argparser == 'fire')) { :::#
import fire

#::: } :::#

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # remove tokenizer paralleism warning


def run(local_rank: int, config: Any):
    # make a certain seed
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    # create output folder and copy config file to output dir
    config.output_dir = setup_output_dir(config, rank)

    if rank == 0:
        save_config(config, config.output_dir)

    # donwload datasets and create dataloaders
    dataloader_train, dataloader_eval = setup_data(config)

    config.num_iters_per_epoch = len(dataloader_train)

    # model, optimizer, loss function, device
    device = idist.device()
    model = idist.auto_model(
        TransformerModel(
            config.model,
            config.model_dir,
            config.drop_out,
            config.n_fc,
            config.num_classes,
        )
    )

    config.lr *= idist.get_world_size()
    optimizer = idist.auto_optim(optim.AdamW(model.parameters(), lr=config.lr, weight_decay=config.weight_decay))
    loss_fn = nn.BCEWithLogitsLoss().to(device=device)

    le = config.num_iters_per_epoch
    milestones_values = [
        (0, 0.0),
        (le * config.num_warmup_epochs, config.lr),
        (le * config.max_epochs, 0.0),
    ]
    lr_scheduler = PiecewiseLinear(optimizer, param_name="lr", milestones_values=milestones_values)

    # setup metrics to attach to evaluator
    metrics = {
        "Accuracy": Accuracy(output_transform=thresholded_output_transform),
        "Loss": Loss(loss_fn),
    }

    # trainer and evaluator
    trainer = setup_trainer(config, model, optimizer, loss_fn, device, dataloader_train.sampler)
    evaluator = setup_evaluator(config, model, metrics, device)

    # setup engines logger with python logging
    # print training configurations
    logger = setup_logging(config)
    logger.info("Configuration: \n%s", pformat(config))
    trainer.logger = evaluator.logger = logger

    trainer.add_event_handler(Events.ITERATION_COMPLETED, lr_scheduler)

    #::: if (it.save_training || it.save_evaluation) { :::#

    # setup ignite handlers
    #::: if (it.save_training) { :::#
    to_save_train = {
        "model": model,
        "optimizer": optimizer,
        "trainer": trainer,
        "lr_scheduler": lr_scheduler,
    }
    #::: } else { :::#
    to_save_train = None
    #::: } :::#
    #::: if (it.save_evaluation) { :::#
    to_save_eval = {"model": model}
    #::: } else { :::#
    to_save_eval = None
    #::: } :::#
    ckpt_handler_train, ckpt_handler_eval = setup_handlers(trainer, evaluator, config, to_save_train, to_save_eval)
    #::: } else if (it.patience || it.terminate_on_nan || it.limit_sec) { :::#
    setup_handlers(trainer, evaluator, config)
    #::: } :::#

    #::: if (it.logger) { :::#

    # experiment tracking
    if rank == 0:
        exp_logger = setup_exp_logging(config, trainer, optimizer, evaluator)
    #::: } :::#

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

    #::: if (it.logger) { :::#

    # close logger
    if rank == 0:
        exp_logger.close()
    #::: } :::#

    #::: if (it.save_training || it.save_evaluation) { :::#

    # show last checkpoint names
    logger.info(
        "Last training checkpoint name - %s",
        ckpt_handler_train.last_checkpoint,
    )

    logger.info(
        "Last evaluation checkpoint name - %s",
        ckpt_handler_eval.last_checkpoint,
    )
    #::: } :::#


#::= from_template_common ::#
