from functools import partial
from pprint import pformat
from typing import Any, cast

import ignite.distributed as idist
from data import denormalize, setup_data
from ignite.engine import Events
from ignite.handlers import LRScheduler
from ignite.metrics import ConfusionMatrix, IoU, mIoU
from ignite.utils import manual_seed
from models import setup_model
from torch import nn, optim
from torch.optim.lr_scheduler import LambdaLR
from trainers import setup_evaluator, setup_trainer

from vis import predictions_gt_images_handler
from utils import *

#::: if ((it.argparser == 'fire')) { :::#
import fire

#::: } :::#


try:
    from torch.optim.lr_scheduler import LRScheduler as PyTorchLRScheduler
except ImportError:
    from torch.optim.lr_scheduler import _LRScheduler as PyTorchLRScheduler


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
    le = len(dataloader_train)

    # model, optimizer, loss function, device
    device = idist.device()
    model = idist.auto_model(setup_model(config))
    optimizer = idist.auto_optim(
        optim.SGD(
            model.parameters(),
            lr=1.0,
            momentum=0.9,
            weight_decay=5e-4,
            nesterov=False,
        )
    )
    loss_fn = nn.CrossEntropyLoss().to(device=device)
    lr_scheduler = LambdaLR(
        optimizer,
        lr_lambda=[
            partial(
                lambda_lr_scheduler,
                lr0=config.lr,
                n=config.max_epochs * le,
                a=0.9,
            )
        ],
    )

    # setup metrics
    cm_metric = ConfusionMatrix(num_classes=config.num_classes)
    metrics = {"IoU": IoU(cm_metric), "mIoU_bg": mIoU(cm_metric)}

    # trainer and evaluator
    trainer = setup_trainer(config, model, optimizer, loss_fn, device, dataloader_train.sampler)
    evaluator = setup_evaluator(config, model, metrics, device)

    # setup engines logger with python logging
    # print training configurations
    logger = setup_logging(config)
    logger.info("Configuration: \n%s", pformat(config))
    trainer.logger = evaluator.logger = logger

    if isinstance(lr_scheduler, PyTorchLRScheduler):
        trainer.add_event_handler(
            Events.ITERATION_COMPLETED,
            lambda engine: cast(PyTorchLRScheduler, lr_scheduler).step(),
        )
    elif isinstance(lr_scheduler, LRScheduler):
        trainer.add_event_handler(Events.ITERATION_COMPLETED, lr_scheduler)
    else:
        trainer.add_event_handler(Events.ITERATION_STARTED, lr_scheduler)

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

        # Log validation predictions as images
        # We define a custom event filter to log less frequently the images (to reduce storage size)
        # - we plot images with masks of the middle validation batch
        # - once every 3 validations and
        # - at the end of the training
        def custom_event_filter(_, val_iteration):
            c1 = val_iteration == len(dataloader_eval) // 2
            c2 = trainer.state.epoch % 3 == 0
            c2 |= trainer.state.epoch == config.max_epochs
            return c1 and c2

        # Image denormalization function to plot predictions with images
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)
        img_denormalize = partial(denormalize, mean=mean, std=std)

        exp_logger.attach(
            evaluator,
            log_handler=predictions_gt_images_handler(
                img_denormalize_fn=img_denormalize,
                n_images=15,
                another_engine=trainer,
                prefix_tag="validation",
            ),
            event_name=Events.ITERATION_COMPLETED(event_filter=custom_event_filter),
        )

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
