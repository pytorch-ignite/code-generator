import os
from argparse import Namespace
from numbers import Number
from typing import Iterable

import ignite.distributed as idist
import pytest
import torch
from datasets import get_datasets
from ignite.contrib.handlers.param_scheduler import ParamScheduler
from ignite.engine import Engine
from torch import nn, optim
from torch.functional import Tensor
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import Dataset
from trainers import evaluate_function
from utils import initialize


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    return model, optimizer, device, loss_fn, batch


@pytest.mark.skipif(os.getenv("RUN_SLOW_TESTS", 0) == 0, reason="Skip slow tests")
def test_get_datasets(tmp_path):
    train_ds, eval_ds = get_datasets(tmp_path)

    assert isinstance(train_ds, Dataset)
    assert isinstance(eval_ds, Dataset)
    train_batch = next(iter(train_ds))
    assert isinstance(train_batch, Iterable)
    assert isinstance(train_batch[0], Tensor)
    assert isinstance(train_batch[1], Number)
    assert train_batch[0].ndim == 3
    eval_batch = next(iter(eval_ds))
    assert isinstance(eval_batch, Iterable)
    assert isinstance(eval_batch[0], Tensor)
    assert isinstance(eval_batch[1], Number)
    assert eval_batch[0].ndim == 3


def test_evaluate_fn():
    model, _, device, _, batch = set_up()
    engine = Engine(lambda e, b: 1)
    config = Namespace(use_amp=False)
    output = evaluate_function(config, engine, batch, model, device)
    assert isinstance(output, tuple)


def test_initialize():
    config = Namespace(
        model="squeezenet1_0",
        lr=1e-3,
        momentum=0.9,
        weight_decay=1e-4,
        num_iters_per_epoch=1,
        num_warmup_epochs=1,
        max_epochs=1,
    )
    model, optimizer, loss_fn, lr_scheduler = initialize(config)
    assert isinstance(model, nn.Module)
    assert isinstance(optimizer, optim.Optimizer)
    assert isinstance(loss_fn, nn.Module)
    assert isinstance(lr_scheduler, (_LRScheduler, ParamScheduler))
