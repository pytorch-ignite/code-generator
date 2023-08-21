import os
from argparse import Namespace
from typing import Iterable

import ignite.distributed as idist
import pytest
import torch
import yaml
from data import setup_data
from models import Discriminator, Generator
from omegaconf import OmegaConf
from torch import nn, optim, Tensor
from torch.utils.data.dataloader import DataLoader
from trainers import setup_trainer
from utils import save_config


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    return model, optimizer, device, loss_fn, batch


@pytest.mark.skipif(os.getenv("RUN_SLOW_TESTS", 0) == 0, reason="Skip slow tests")
def test_setup_data():
    config = Namespace(data_path="~/data", train_batch_size=1, eval_batch_size=1, num_workers=0)
    dataloader_train, dataloader_eval, _ = setup_data(config)

    assert isinstance(dataloader_train, DataLoader)
    assert isinstance(dataloader_eval, DataLoader)
    train_batch = next(iter(dataloader_train))
    assert isinstance(train_batch, Iterable)
    assert isinstance(train_batch[0], Tensor)
    assert isinstance(train_batch[1], Tensor)
    assert train_batch[0].ndim == 4
    assert train_batch[1].ndim == 1
    eval_batch = next(iter(dataloader_eval))
    assert isinstance(eval_batch, Iterable)
    assert isinstance(eval_batch[0], Tensor)
    assert isinstance(eval_batch[1], Tensor)
    assert eval_batch[0].ndim == 4
    assert eval_batch[1].ndim == 1


def test_models():
    model_G = Generator(100, 64, 3)
    model_D = Discriminator(3, 64)
    x = torch.rand([1, 100, 32, 32])
    y = model_G(x)
    y.sum().backward()
    z = model_D(y)
    assert y.shape == torch.Size([1, 3, 560, 560])
    assert z.shape == torch.Size([1024])
    assert isinstance(model_D, nn.Module)
    assert isinstance(model_G, nn.Module)


def test_setup_trainer():
    model, optimizer, device, loss_fn, batch = set_up()
    config = Namespace(use_amp=False, train_batch_size=2, z_dim=100)
    trainer = setup_trainer(config, model, model, optimizer, optimizer, loss_fn, device, None)
    trainer.run([batch, batch])
    assert isinstance(trainer.state.output, dict)


#::= from_template_common ::#
