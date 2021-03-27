import logging
import os
import warnings
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import ignite.distributed as idist
import torch
import torch.nn as nn
import torch.optim as optim
from datasets import get_datasets
from fn import update
from ignite.contrib.handlers import ProgressBar
from ignite.engine import Engine, Events
from ignite.handlers import ModelCheckpoint, Timer
from ignite.metrics import RunningAverage
from ignite.utils import manual_seed
from models import Discriminator, Generator
from torchvision import utils as vutils
from utils import get_default_parser

PRINT_FREQ = 100
FAKE_IMG_FNAME = "fake_sample_epoch_{:04d}.png"
REAL_IMG_FNAME = "real_sample_epoch_{:04d}.png"
LOGS_FNAME = "logs.tsv"
PLOT_FNAME = "plot.svg"
SAMPLES_FNAME = "samples.svg"
CKPT_PREFIX = "networks"


def run(
    local_rank: int,
    config: Any,
    *args: Any,
    **kwargs: Any
):

    # -----------------------------
    # datasets and dataloaders
    # -----------------------------
    {% block datasets_and_dataloaders %}
    dataset, num_channels = get_datasets(config.dataset, config.data_path)
    loader = idist.auto_dataloader(dataset, batch_size=config.batch_size, shuffle=True, num_workers=config.num_workers, drop_last=True)
    {% endblock %}

    # ------------------------------------------
    # models, optimizers, loss function, device
    # ------------------------------------------
    {% block model_optimizer_loss %}
    device = idist.device()
    netG = idist.auto_model(Generator(config.z_dim, config.g_filters, num_channels))
    netD = idist.auto_model(Discriminator(num_channels, config.d_filters))
    bce = nn.BCELoss()
    optimizerG = optim.Adam(netG.parameters(), lr=config.lr, betas=(config.beta_1, 0.999))
    optimizerD = optim.Adam(netD.parameters(), lr=config.lr, betas=(config.beta_1, 0.999))
    {% endblock %}

    # --------------------------
    # load pre-trained models
    # --------------------------
    {% block pretrained %}
    if config.saved_G:
        netG.load_state_dict(torch.load(config.saved_G))

    if config.saved_D:
        netD.load_state_dict(torch.load(config.saved_D))
    {% endblock %}

    # ------
    # misc
    # ------
    real_labels = torch.ones(config.batch_size, device=device)
    fake_labels = torch.zeros(config.batch_size, device=device)
    fixed_noise = torch.randn(config.batch_size, config.z_dim, 1, 1, device=device)

    # ----------------
    # ignite objects
    # ----------------
    trainer = Engine(update(netD, netG, device, optimizerD, optimizerG, bce, config, real_labels, fake_labels))
    checkpoint_handler = ModelCheckpoint(config.filepath, CKPT_PREFIX, n_saved=config.n_saved, require_empty=False)
    timer = Timer(average=True)

    # attach running average metrics
    monitoring_metrics = ["errD", "errG", "D_x", "D_G_z1", "D_G_z2"]
    RunningAverage(alpha=config.alpha, output_transform=lambda x: x["errD"]).attach(trainer, "errD")
    RunningAverage(alpha=config.alpha, output_transform=lambda x: x["errG"]).attach(trainer, "errG")
    RunningAverage(alpha=config.alpha, output_transform=lambda x: x["D_x"]).attach(trainer, "D_x")
    RunningAverage(alpha=config.alpha, output_transform=lambda x: x["D_G_z1"]).attach(trainer, "D_G_z1")
    RunningAverage(alpha=config.alpha, output_transform=lambda x: x["D_G_z2"]).attach(trainer, "D_G_z2")

    # attach ignite handlers
    to_save = {'netD': netD, 'netG': netG, 'optimizerD': optimizerD, 'optimizerG': optimizerG, 'trainer': trainer}
    optimizers = {'optimizerD': optimizerD, 'optimizerG': optimizerG}
    evaluators = None
    {% include "_handlers.pyi" %}

    # attach progress bar
    pbar = ProgressBar()
    pbar.attach(trainer, metric_names=monitoring_metrics)

    @trainer.on(Events.ITERATION_COMPLETED(every=config.log_train))
    def print_logs(engine):
        fname = config.filepath / LOGS_FNAME
        columns = ["iteration",] + list(engine.state.metrics.keys())
        values = [str(engine.state.iteration),] + [str(round(value, 5)) for value in engine.state.metrics.values()]

        with open(fname, "a") as f:
            if f.tell() == 0:
                print("\t".join(columns), file=f)
            print("\t".join(values), file=f)
        message = f"[{engine.state.epoch}/{config.max_epochs}][{engine.state.iteration % len(loader)}/{len(loader)}]"
        for name, value in zip(columns, values):
            message += f" | {name}: {value}"

        pbar.log_message(message)

    # --------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # --------------------------------------------------
    @trainer.on(Events.EPOCH_COMPLETED)
    def save_fake_example(engine):
        fake = netG(fixed_noise)
        path = config.filepath / (FAKE_IMG_FNAME.format(engine.state.epoch))
        vutils.save_image(fake.detach(), path, normalize=True)

    # --------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # --------------------------------------------------
    @trainer.on(Events.EPOCH_COMPLETED)
    def save_real_example(engine):
        img, y = engine.state.batch
        path = config.filepath / (REAL_IMG_FNAME.format(engine.state.epoch))
        vutils.save_image(img, path, normalize=True)

    # -------------------------------------------------------------
    # adding handlers using `trainer.add_event_handler` method API
    # -------------------------------------------------------------
    trainer.add_event_handler(
        event_name=Events.EPOCH_COMPLETED, handler=checkpoint_handler, to_save={"netG": netG, "netD": netD}
    )

    # -------------------------------------------------------------
    # automatically adding handlers via a special `attach` method of `Timer` handler
    # -------------------------------------------------------------
    timer.attach(
        trainer,
        start=Events.EPOCH_STARTED,
        resume=Events.ITERATION_STARTED,
        pause=Events.ITERATION_COMPLETED,
        step=Events.ITERATION_COMPLETED,
    )

    # -------------------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # -------------------------------------------------------------
    @trainer.on(Events.EPOCH_COMPLETED)
    def print_times(engine):
        pbar.log_message(f"Epoch {engine.state.epoch} done. Time per batch: {timer.value():.3f}[s]")
        timer.reset()

    # -------------------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # -------------------------------------------------------------
    @trainer.on(Events.EPOCH_COMPLETED)
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

    # -------------------------------------------------------------
    # adding handlers using `trainer.on` decorator API
    # -------------------------------------------------------------
    @trainer.on(Events.EXCEPTION_RAISED)
    def handle_exception(engine, e):
        if isinstance(e, KeyboardInterrupt) and (engine.state.iteration > 1):
            engine.terminate()
            warnings.warn("KeyboardInterrupt caught. Exiting gracefully.")

            create_plots(engine)
            checkpoint_handler(engine, {"netG_exception": netG, "netD_exception": netD})

        else:
            raise e

    # ---------------------------------------------
    # Setup is done. Now let's run the training
    # ---------------------------------------------
    trainer.run(loader, max_epochs=config.max_epochs, epoch_length=config.epoch_length)


{% block main_fn %}
def main():
    parser = ArgumentParser(parents=[get_default_parser()])
    config = parser.parse_args()
    manual_seed(config.seed)
    config.verbose = logging.INFO if config.verbose else logging.WARNING
    if config.filepath:
        path = Path(config.filepath)
        path.mkdir(parents=True, exist_ok=True)
        config.filepath = path
    with idist.Parallel(
        backend=idist.backend(),
        nproc_per_node=config.nproc_per_node,
        nnodes=config.nnodes,
        node_rank=config.node_rank,
        master_addr=config.master_addr,
        master_port=config.master_port
    ) as parallel:
        parallel.run(run, config=config)
{% endblock %}

{% block entrypoint %}
if __name__ == "__main__":
    main()
{% endblock %}
