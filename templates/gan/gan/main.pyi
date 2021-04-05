"""
main entrypoint training
"""
import warnings
from argparse import ArgumentParser
from pathlib import Path
from typing import Any
from ignite.contrib.handlers.wandb_logger import WandBLogger

import torch
import ignite.distributed as idist
from ignite.engine.events import Events
from ignite.utils import manual_seed
from torchvision import utils as vutils

from {{project_name}}.datasets import get_datasets
from {{project_name}}.trainers import create_trainers
from {{project_name}}.handlers import get_handlers, get_logger
from {{project_name}}.utils import setup_logging, log_metrics, log_basic_info, initialize, resume_from
from {{project_name}}.config import get_default_parser


PRINT_FREQ = 100
FAKE_IMG_FNAME = "fake_sample_epoch_{:04d}.png"
REAL_IMG_FNAME = "real_sample_epoch_{:04d}.png"
LOGS_FNAME = "logs.tsv"
PLOT_FNAME = "plot.svg"
SAMPLES_FNAME = "samples.svg"
CKPT_PREFIX = "networks"


def run(local_rank: int, config: Any, *args: Any, **kwargs: Any):
    """function to be run by idist.Parallel context manager."""

    # -----------------------------
    # datasets and dataloaders
    # -----------------------------

    train_dataset, num_channels = get_datasets(config.dataset, config.data_path)
    train_dataloader = idist.auto_dataloader(
        train_dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers
    )

    # ------------------------------------------
    # model, optimizer, loss function, device
    # ------------------------------------------

    device = idist.device()
    netD, netG, optimizerD, optimizerG, loss_fn, lr_scheduler = initialize(config, num_channels)

    # -----------------------------
    # train_engine and eval_engine
    # -----------------------------
    real_labels = torch.ones(config.batch_size, device=device)
    fake_labels = torch.zeros(config.batch_size, device=device)
    fixed_noise = torch.randn(config.batch_size, config.z_dim, 1, 1, device=device)

    train_engine = create_trainers(
        config=config,
        netD=netD,
        netG=netG,
        optimizerD=optimizerD,
        optimizerG=optimizerG,
        loss_fn=loss_fn,
        device=device,
        real_labels=real_labels,
        fake_labels=fake_labels,
    )

    # -------------------------------------------
    # update config with optimizer parameters
    # setup engines logger with python logging
    # print training configurations
    # -------------------------------------------

    logger = setup_logging(config)
    log_basic_info(logger, config)
    train_engine.logger = logger

    # -------------------------------------
    # ignite handlers and ignite loggers
    # -------------------------------------

    to_save = {'netD': netD, 'netG': netG, 'optimizerD': optimizerD, 'optimizerG': optimizerG, 'trainer': train_engine}
    optimizers = {'optimizerD': optimizerD, 'optimizerG': optimizerG}
    best_model_handler, es_handler, timer_handler = get_handlers(
        config=config,
        model={'netD', netD, 'netG', netG},
        train_engine=train_engine,
        to_save=to_save,
        lr_scheduler=lr_scheduler,
        output_names=["errD", "errG", "D_x", "D_G_z1", "D_G_z2"],
    )
    logger_handler = get_logger(config=config, train_engine=train_engine, optimizers=optimizers)

    # -----------------------------------
    # resume from the saved checkpoints
    # -----------------------------------

    if config.resume_from:
        resume_from(to_load=to_save, checkpoint_fp=config.resume_from)

    # --------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # --------------------------------------------------

    @train_engine.on(Events.EPOCH_COMPLETED)
    def save_fake_example(engine):
        fake = netG(fixed_noise)
        path = config.filepath / (FAKE_IMG_FNAME.format(engine.state.epoch))
        vutils.save_image(fake.detach(), path, normalize=True)

    # --------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # --------------------------------------------------
    @train_engine.on(Events.EPOCH_COMPLETED)
    def save_real_example(engine):
        img, y = engine.state.batch
        path = config.filepath / (REAL_IMG_FNAME.format(engine.state.epoch))
        vutils.save_image(img, path, normalize=True)

    # -------------------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # -------------------------------------------------------------
    @train_engine.on(Events.EPOCH_COMPLETED)
    def print_times(engine):
        if not timer_handler:
            logger.info(f"Epoch {engine.state.epoch} done. Time per batch: {timer_handler.value():.3f}[s]")
            timer_handler.reset()

    # -------------------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # -------------------------------------------------------------
    @train_engine.on(Events.EPOCH_COMPLETED)
    def create_plots(engine):
        try:
            import matplotlib as mpl

            mpl.use("agg")

            import matplotlib.pyplot as plt
            import pandas as pd

        except ImportError:
            warnings.warn("Loss plots will not be generated -- pandas or matplotlib not found")

        else:
            df = pd.read_csv(config.filepath / LOGS_FNAME, delimiter="\t", index_col="iteration")
            _ = df.plot(subplots=True, figsize=(20, 20))
            _ = plt.xlabel("Iteration number")
            fig = plt.gcf()
            path = config.filepath / PLOT_FNAME

            fig.savefig(path)

    # --------------------------------
    # print metrics to the stderr
    # with `add_event_handler` API
    # for training stats
    # --------------------------------

    train_engine.add_event_handler(Events.ITERATION_COMPLETED(config.log_every_iters), log_metrics, tag="train")

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

    if config.filepath:
        path = Path(config.filepath)
        path.mkdir(parents=True, exist_ok=True)
        config.filepath = path

    if config.output_path:
        path = Path(config.output_path)
        path.mkdir(parents=True, exist_ok=True)
        config.output_path = path

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
