from typing import Any, Union

import ignite.distributed as idist
import torch
from ignite.engine import DeterministicEngine, Engine, Events
from torch.cuda.amp import autocast
from torch.nn import Module
from torch.optim import Optimizer
from torch.utils.data import DistributedSampler, Sampler


def setup_trainer(
    config: Any,
    model_g: Module,
    model_d: Module,
    optimizer_d: Optimizer,
    optimizer_g: Optimizer,
    loss_fn: Module,
    device: Union[str, torch.device],
    train_sampler: Sampler,
) -> Union[Engine, DeterministicEngine]:

    ws = idist.get_world_size()

    real_labels = torch.ones(config.train_batch_size // ws, device=device)
    fake_labels = torch.zeros(config.train_batch_size // ws, device=device)
    noise = torch.randn(
        config.train_batch_size // ws, config.z_dim, 1, 1, device=device
    )

    def train_function(engine: Union[Engine, DeterministicEngine], batch: Any):
        model_g.train()
        model_d.train()

        # unpack the batch. It comes from a dataset, so we have <images, labels> pairs. Discard labels.
        real = batch[0].to(device, non_blocking=True)

        # (1) Update D network: maximize log(D(x)) + log(1 - D(G(z)))
        model_d.zero_grad()

        # train with real
        with autocast(config.use_amp):
            outputs = model_d(real)
            errD_real = loss_fn(outputs, real_labels)

        D_x = outputs.mean().item()
        errD_real.backward()

        # get fake image from generator
        fake = model_g(noise)

        # train with fake
        with autocast(config.use_amp):
            outputs = model_d(fake.detach())
            errD_fake = loss_fn(outputs, fake_labels)

        D_G_z1 = outputs.mean().item()

        errD_fake.backward()

        errD = errD_real + errD_fake
        optimizer_d.step()

        # (2) Update G network: maximize log(D(G(z)))
        model_g.zero_grad()

        # Update generator. We want to make a step that will make it more likely that discriminator outputs "real"
        with autocast(config.use_amp):
            output = model_d(fake)
            errG = loss_fn(output, real_labels)

        D_G_z2 = output.mean().item()

        errG.backward()

        # gradient update
        optimizer_g.step()

        metrics = {
            "epoch": engine.state.epoch,
            "errD": errD.item(),
            "errG": errG.item(),
            "D_x": D_x,
            "D_G_z1": D_G_z1,
            "D_G_z2": D_G_z2,
        }
        engine.state.metrics = metrics

        return metrics

    #::: if(it.deterministic) { :::#
    trainer = DeterministicEngine(train_function)
    #::: } else { :::#
    trainer = Engine(train_function)
    #::: } :::#

    # set epoch for distributed sampler
    @trainer.on(Events.EPOCH_STARTED)
    def set_epoch():
        if idist.get_world_size() > 1 and isinstance(
            train_sampler, DistributedSampler
        ):
            train_sampler.set_epoch(trainer.state.epoch - 1)


def setup_evaluator(
    config: Any,
    model_g: Module,
    model_d: Module,
    loss_fn: Module,
    device: Union[str, torch.device],
) -> Engine:

    ws = idist.get_world_size()

    real_labels = torch.ones(config.eval_batch_size // ws, device=device)
    fake_labels = torch.zeros(config.eval_batch_size // ws, device=device)
    noise = torch.randn(
        config.eval_batch_size // ws, config.z_dim, 1, 1, device=device
    )

    @torch.no_grad()
    def eval_function(engine: Engine, batch: Any):
        model_g.eval()
        model_d.eval()

        # unpack the batch. It comes from a dataset, so we have <images, labels> pairs. Discard labels.
        real = batch[0].to(device, non_blocking=True)

        # train with real
        with autocast(config.use_amp):
            outputs = model_d(real)
            errD_real = loss_fn(outputs, real_labels)

        D_x = outputs.mean().item()

        # get fake image from generator
        fake = model_g(noise)

        # train with fake
        with autocast(config.use_amp):
            outputs = model_d(fake.detach())
            errD_fake = loss_fn(outputs, fake_labels)

        D_G_z1 = outputs.mean().item()

        errD = errD_real + errD_fake

        # Update generator. We want to make a step that will make it more likely that discriminator outputs "real"
        with autocast(config.use_amp):
            output = model_d(fake)
            errG = loss_fn(output, real_labels)

        D_G_z2 = output.mean().item()

        metrics = {
            "epoch": engine.state.epoch,
            "errD": errD.item(),
            "eval_loss": errD.item(),
            "errG": errG.item(),
            "D_x": D_x,
            "D_G_z1": D_G_z1,
            "D_G_z2": D_G_z2,
        }
        engine.state.metrics = metrics

        return metrics

    return Engine(eval_function)
