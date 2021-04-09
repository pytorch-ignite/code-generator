from argparse import Namespace
from numbers import Number
from unittest.mock import MagicMock

import ignite.distributed as idist
import torch
from ignite.engine.engine import Engine
from torch import nn, optim
from trainers import (
    TrainEvents,
    evaluate_function,
    train_events_to_attr,
    train_function,
)


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    return model, optimizer, device, loss_fn, batch


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
    assert isinstance(output, Number)
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
    output = evaluate_function(config, engine, batch, model, loss_fn, device)
    assert isinstance(output, Number)
