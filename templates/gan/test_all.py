from argparse import Namespace
from numbers import Number
from typing import Iterable

import ignite.distributed as idist
import torch
from datasets import get_datasets
from ignite.engine import Engine
from models import Discriminator, Generator
from torch import nn, optim
from torch.functional import Tensor
from torch.utils.data import Dataset
from trainers import train_function


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    return model, optimizer, device, loss_fn, batch


def test_get_datasets(tmp_path):
    dataset, _ = get_datasets("cifar10", tmp_path)

    assert isinstance(dataset, Dataset)
    batch = next(iter(dataset))
    assert isinstance(batch, Iterable)
    assert isinstance(batch[0], Tensor)
    assert isinstance(batch[1], Number)
    assert batch[0].dim == 3


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


def test_train_fn():
    model, optimizer, device, loss_fn, batch = set_up()
    real_labels = torch.ones(2, device=device)
    fake_labels = torch.zeros(2, device=device)
    engine = Engine(lambda e, b: 1)
    config = Namespace(use_amp=False, batch_size=2, z_dim=100)
    output = train_function(
        config,
        engine,
        batch,
        model,
        model,
        loss_fn,
        optimizer,
        optimizer,
        device,
        real_labels,
        fake_labels,
    )
    assert isinstance(output, dict)
