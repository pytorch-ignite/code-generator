from pprint import pformat
from typing import Any

import ignite.distributed as idist
import torch
import torchvision.utils as vutils
from data import setup_data
from ignite.engine import Events
from ignite.utils import manual_seed
from models import Discriminator, Generator
from torch import nn, optim
from trainers import setup_evaluator, setup_trainer
from utils import *

#::: if ((it.argparser == 'fire')) { :::#
import fire

#::: } :::#


FAKE_IMG_FNAME = "fake_sample_epoch_{:04d}.png"
REAL_IMG_FNAME = "real_sample_epoch_{:04d}.png"


def run(local_rank: int, config: Any):
    # make a certain seed
    rank = idist.get_rank()
    manual_seed(config.seed + rank)

    # create output folder and copy config file to output dir
    config.output_dir = setup_output_dir(config, rank)

    if rank == 0:
        save_config(config, config.output_dir)

    # donwload datasets and create dataloaders
    dataloader_train, dataloader_eval, num_channels = setup_data(config)

    # model, optimizer, loss function, device
    device = idist.device()

    fixed_noise = torch.randn(
        config.train_batch_size // idist.get_world_size(),
        config.z_dim,
        1,
        1,
        device=device,
    )

    # networks
    model_g = idist.auto_model(Generator(config.z_dim, config.g_filters, num_channels))
    model_d = idist.auto_model(Discriminator(num_channels, config.d_filters))

    # loss
    loss_fn = nn.BCELoss().to(device=device)

    # optimizers
    optimizer_d = idist.auto_optim(optim.Adam(model_d.parameters(), lr=config.lr, betas=(0.5, 0.999)))
    optimizer_g = idist.auto_optim(optim.Adam(model_g.parameters(), lr=config.lr, betas=(0.5, 0.999)))

    # trainer and evaluator
    trainer = setup_trainer(
        config=config,
        model_g=model_g,
        model_d=model_d,
        optimizer_d=optimizer_d,
        optimizer_g=optimizer_g,
        loss_fn=loss_fn,
        device=device,
        train_sampler=dataloader_train.sampler,
    )
    evaluator = setup_evaluator(
        config=config,
        model_g=model_g,
        model_d=model_d,
        loss_fn=loss_fn,
        device=device,
    )

    # setup engines logger with python logging
    # print training configurations
    logger = setup_logging(config)
    logger.info("Configuration: \n%s", pformat(config))
    trainer.logger = evaluator.logger = logger

    #::: if (it.save_training || it.save_evaluation) { :::#

    # setup ignite handlers
    #::: if (it.save_training) { :::#
    to_save_train = {
        "model_d": model_d,
        "model_g": model_g,
        "optimizer_d": optimizer_d,
        "optimizer_g": optimizer_g,
        "trainer": trainer,
    }
    #::: } else { :::#
    to_save_train = None
    #::: } :::#
    #::: if (it.save_evaluation) { :::#
    to_save_eval = {"model_d": model_d, "model_g": model_g}
    #::: } else { :::#
    to_save_train = None
    #::: } :::#
    ckpt_handler_train, ckpt_handler_eval = setup_handlers(trainer, evaluator, config, to_save_train, to_save_eval)
    #::: } else if (it.patience || it.terminate_on_nan || it.limit_sec) { :::#
    setup_handlers(trainer, evaluator, config)
    #::: } :::#

    #::: if (it.logger) { :::#

    # experiment tracking
    if rank == 0:
        exp_logger = setup_exp_logging(
            config,
            trainer,
            {"optimizer_d": optimizer_d, "optimizer_g": optimizer_g},
            evaluator,
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

    # adding handlers using `trainer.on` decorator API
    @trainer.on(Events.EPOCH_COMPLETED)
    def save_fake_example(engine):
        fake = model_g(fixed_noise)
        path = config.output_dir / FAKE_IMG_FNAME.format(engine.state.epoch)
        vutils.save_image(fake.detach(), path, normalize=True)

    # adding handlers using `trainer.on` decorator API
    @trainer.on(Events.EPOCH_COMPLETED)
    def save_real_example(engine):
        img, y = engine.state.batch
        path = config.output_dir / REAL_IMG_FNAME.format(engine.state.epoch)
        vutils.save_image(img, path, normalize=True)

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
