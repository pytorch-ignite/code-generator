from argparse import Namespace
from numbers import Number
from typing import Iterable
from unittest.mock import MagicMock

import ignite.distributed as idist
import torch
from datasets import get_datasets
from ignite.contrib.handlers.param_scheduler import ParamScheduler
from ignite.engine import Engine
from torch import nn, optim
from torch.functional import Tensor
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import Dataset
from trainers import (
    TrainEvents,
    evaluate_function,
    train_events_to_attr,
    train_function,
)
from utils import initialize


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    return model, optimizer, device, loss_fn, batch


def test_get_datasets(tmp_path):
    train_ds, eval_ds = get_datasets(tmp_path)
    assert isinstance(train_ds, Dataset)
    assert isinstance(eval_ds, Dataset)
    train_batch = next(iter(train_ds))
    assert isinstance(train_batch, Iterable)
    assert isinstance(train_batch[0], Tensor)
    assert isinstance(train_batch[1], Number)
    eval_batch = next(iter(eval_ds))
    assert isinstance(eval_batch, Iterable)
    assert isinstance(eval_batch[0], Tensor)
    assert isinstance(eval_batch[1], Number)


def test_train_fn():
    model, optimizer, device, loss_fn, batch = set_up()
    engine = Engine(lambda e, b: 1)
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED, backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED, optim)
    config = Namespace(use_amp=False)
    output = train_function(config, engine, batch, model, loss_fn, optimizer, device)
    assert isinstance(output, dict)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 1
    assert engine.state.optim_step_completed == 1
    assert backward.call_count == 1
    assert optim.call_count == 1
    assert backward.called
    assert optim.called


def test_train_fn_event_filter():
    model, optimizer, device, loss_fn, batch = set_up()
    config = Namespace(use_amp=False)
    engine = Engine(lambda e, b: train_function(config, e, b, model, loss_fn, optimizer, device))
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), optim)
    engine.run([batch] * 5)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 5
    assert engine.state.optim_step_completed == 5
    assert backward.call_count == 3
    assert optim.call_count == 3
    assert backward.called
    assert optim.called


def test_train_fn_every():
    model, optimizer, device, loss_fn, batch = set_up()

    config = Namespace(use_amp=False)
    engine = Engine(lambda e, b: train_function(config, e, b, model, loss_fn, optimizer, device))
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(every=2), backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(every=2), optim)
    engine.run([batch] * 5)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 5
    assert engine.state.optim_step_completed == 5
    assert backward.call_count == 2
    assert optim.call_count == 2
    assert backward.called
    assert optim.called


def test_train_fn_once():
    model, optimizer, device, loss_fn, batch = set_up()
    config = Namespace(use_amp=False)
    engine = Engine(lambda e, b: train_function(config, e, b, model, loss_fn, optimizer, device))
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(once=3), backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(once=3), optim)
    engine.run([batch] * 5)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 5
    assert engine.state.optim_step_completed == 5
    assert backward.call_count == 1
    assert optim.call_count == 1
    assert backward.called
    assert optim.called


def test_evaluate_fn():
    model, optimizer, device, loss_fn, batch = set_up()
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
