from typing import Iterable
from argparse import Namespace
from numbers import Number

import torch
from torch import nn, optim
from torch.functional import Tensor
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import Dataset

from ignite.contrib.handlers.param_scheduler import ParamScheduler


from dataset import get_dataset
from main import initialize


def test_get_dataset(cache_dir, tokenizer_name, tokenizer_dir, max_length):
    train_ds, eval_ds = get_dataset(cache_dir, tokenizer_name, tokenizer_dir, max_length)

    assert isinstance(train_ds, Dataset)
    assert isinstance(eval_ds, Dataset)
    train_batch = next(iter(train_ds))
    assert isinstance(train_batch, Iterable)
    assert isinstance(train_batch[0], Tensor)
    assert isinstance(train_batch[1], Number)
    assert train_batch[0].dim == 3
    eval_batch = next(iter(eval_ds))
    assert isinstance(eval_batch, Iterable)
    assert isinstance(eval_batch[0], Tensor)
    assert isinstance(eval_batch[1], Number)
    assert eval_batch[0].dim == 3


def test_initialize():
    config = Namespace(
        model="bert-base-uncased",
        model_dir=r"\tmp",
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
