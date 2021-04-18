from typing import Iterable
from argparse import Namespace
from numbers import Number

import torch
from torch import nn, optim
from torch.functional import Tensor
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import Dataset, DataLoader

import ignite.distributed as idist
from ignite.contrib.handlers.param_scheduler import ParamScheduler

from main import initialize
from dataset import get_dataset, get_dataflow


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    return model, optimizer, loss_fn, device


def test_initialize():
    config = Namespace(
        model="bert-base-uncased",
        model_dir="/tmp",
        dropout=0.3,
        n_fc=768,
        num_classes=1,
        learning_rate=1e-3,
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


def test_get_dataset(cache_dir, tokenizer_name, tokenizer_dir, max_length):
    train_ds, eval_ds = get_dataset(cache_dir, tokenizer_name, tokenizer_dir, max_length)
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


def test_get_dataflow():
    config = Namespace(
        data_dir="/tmp/data",
        model="bert-base-uncased",
        tokenizer_dir="/tmp/tokenizer",
        max_length=1,
        batch_size=1,
        num_workers=1,
    )
    train_loader, test_loader = get_dataflow(config)
    assert isinstance(train_loader, DataLoader)
    assert isinstance(test_loader, DataLoader)
