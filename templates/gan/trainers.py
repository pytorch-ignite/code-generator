"""
`train_engine` and `eval_engine` like trainer and evaluator
"""
from typing import Any

import torch
from ignite.engine import Engine
from torch.cuda.amp import autocast
from torch.optim.optimizer import Optimizer


# Edit below functions the way how the model will be training

# train_function is how the model will be learning with given batch
# below in the train_function, common parameters are provided
# you can add any additional parameters depending on the training
# NOTE : engine and batch parameters are needed to work with
# Ignite's Engine.
# TODO: Extend with your custom training.
def train_function(
    config: Any,
    engine: Engine,
    batch: Any,
    netD: torch.nn.Module,
    netG: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizerD: Optimizer,
    optimizerG: Optimizer,
    device: torch.device,
    real_labels: torch.Tensor,
    fake_labels: torch.Tensor,
):
    """Model training step.

    Parameters
    ----------
    config
        config object
    engine
        Engine instance
    batch
        batch in current iteration
    netD
        discriminator model
    netG
        generator model
    loss_fn
        nn.Module loss
    optimizerD
        discriminator optimizer
    optimizerG
        generator optimizer
    device
        device to use for training
    real_labels
        real label tensor
    fake_labels
        fake label tensor

    Returns
    -------
    dictionary of loss and output of generator and discriminator
    Keys:
    - errD
    - errG
    - D_x
    - D_G_z1
    - D_G_z2
    """
    # unpack the batch. It comes from a dataset, so we have <images, labels> pairs. Discard labels.
    real = batch[0].to(device, non_blocking=True)

    netD.train()
    netG.train()

    # -----------------------------------------------------------
    # (1) Update D network: maximize log(D(x)) + log(1 - D(G(z)))
    netD.zero_grad()

    # train with real
    with autocast(config.use_amp):
        output = netD(real)
        errD_real = loss_fn(output, real_labels)
    D_x = output.mean().item()

    errD_real.backward()

    # get fake image from generator
    noise = torch.randn(config.batch_size, config.z_dim, 1, 1, device=device)
    fake = netG(noise)

    # train with fake
    with autocast(config.use_amp):
        output = netD(fake.detach())
        errD_fake = loss_fn(output, fake_labels)
    D_G_z1 = output.mean().item()

    errD_fake.backward()

    # gradient update
    errD = errD_real + errD_fake
    optimizerD.step()

    # -----------------------------------------------------------
    # (2) Update G network: maximize log(D(G(z)))
    netG.zero_grad()

    # Update generator. We want to make a step that will make it more likely that discriminator outputs "real"
    output = netD(fake)
    errG = loss_fn(output, real_labels)
    D_G_z2 = output.mean().item()

    errG.backward()

    # gradient update
    optimizerG.step()

    return {"errD": errD.item(), "errG": errG.item(), "D_x": D_x, "D_G_z1": D_G_z1, "D_G_z2": D_G_z2}


# function for creating engines which will be used in main.py
# any necessary arguments can be provided.
def create_trainers(**kwargs) -> Engine:
    """Create Engines for training and evaluation.

    Parameters
    ----------
    kwargs: keyword arguments passed to both train_function and evaluate_function

    Returns
    -------
    train_engine
    """
    train_engine = Engine(
        lambda e, b: train_function(
            engine=e,
            batch=b,
            **kwargs,
        )
    )
    return train_engine
