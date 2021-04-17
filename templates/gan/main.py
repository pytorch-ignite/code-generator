"""
main entrypoint training
"""
import warnings
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from typing import Any
from ignite.contrib.handlers.wandb_logger import WandBLogger

import torch
import ignite.distributed as idist
from ignite.engine.events import Events
from ignite.utils import manual_seed
from torchvision import utils as vutils

from datasets import get_datasets
from trainers import create_trainers
from utils import setup_logging, log_metrics, log_basic_info, initialize, resume_from, get_handlers, get_logger
from config import get_default_parser


FAKE_IMG_FNAME = "fake_sample_epoch_{:04d}.png"
REAL_IMG_FNAME = "real_sample_epoch_{:04d}.png"
LOGS_FNAME = "logs.tsv"
PLOT_FNAME = "plot.svg"


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

    train_dataset, num_channels = get_datasets(config.dataset, config.data_path)

    train_dataloader = idist.auto_dataloader(
        train_dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
        {% if use_distributed_training and not use_distributed_launcher %}
        persistent_workers=True,
        {% endif %}
    )

    # ------------------------------------------
    # model, optimizer, loss function, device
    # ------------------------------------------

    device = idist.device()
    netD, netG, optimizerD, optimizerG, loss_fn, lr_scheduler = initialize(config, num_channels)

    # -----------------------------
    # train_engine and eval_engine
    # -----------------------------
    ws = idist.get_world_size()
    real_labels = torch.ones(config.batch_size // ws, device=device)
    fake_labels = torch.zeros(config.batch_size // ws, device=device)
    fixed_noise = torch.randn(config.batch_size // ws, config.z_dim, 1, 1, device=device)

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
        eval_engine=None,
        metric_name=None,
        es_metric_name=None,
        to_save=to_save,
        lr_scheduler=lr_scheduler,
        output_names=["errD", "errG", "D_x", "D_G_z1", "D_G_z2"],
    )

    # setup ignite logger only on rank 0
    if rank == 0:
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
        path = config.output_dir / (FAKE_IMG_FNAME.format(engine.state.epoch))
        vutils.save_image(fake.detach(), path, normalize=True)

    # --------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # --------------------------------------------------
    @train_engine.on(Events.EPOCH_COMPLETED)
    def save_real_example(engine):
        img, y = engine.state.batch
        path = config.output_dir / (REAL_IMG_FNAME.format(engine.state.epoch))
        vutils.save_image(img, path, normalize=True)

    # -------------------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # -------------------------------------------------------------
    @train_engine.on(Events.EPOCH_COMPLETED)
    def print_times(engine):
        if not timer_handler:
            logger.info(f"Epoch {engine.state.epoch} done. Time per batch: {timer_handler.value():.3f}[s]")
            timer_handler.reset()

    @train_engine.on(Events.ITERATION_COMPLETED(every=config.log_every_iters))
    @idist.one_rank_only()
    def print_logs(engine):
        fname = config.output_dir / LOGS_FNAME
        columns = ["iteration", ] + list(engine.state.metrics.keys())
        values = [str(engine.state.iteration), ] + [str(round(value, 5)) for value in engine.state.metrics.values()]

        with open(fname, "a") as f:
            if f.tell() == 0:
                print("\t".join(columns), file=f)
            print("\t".join(values), file=f)
        message = f"[{engine.state.epoch}/{config.max_epochs}][{engine.state.iteration % len(train_dataloader)}/{len(train_dataloader)}]"
        for name, value in zip(columns, values):
            message += f" | {name}: {value}"

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
            df = pd.read_csv(config.output_dir / LOGS_FNAME, delimiter="\t", index_col="iteration")
            _ = df.plot(subplots=True, figsize=(20, 20))
            _ = plt.xlabel("Iteration number")
            fig = plt.gcf()
            path = config.output_dir / PLOT_FNAME

            fig.savefig(path)

    # --------------------------------
    # print metrics to the stderr
    # with `add_event_handler` API
    # for training stats
    # --------------------------------

    train_engine.add_event_handler(Events.ITERATION_COMPLETED(every=config.log_every_iters), log_metrics, tag="train")

    # ------------------------------------------
    # setup if done. let's run the training
    # ------------------------------------------

    train_engine.run(train_dataloader, max_epochs=config.max_epochs, epoch_length=config.epoch_length)

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
