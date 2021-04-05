import unittest
from argparse import Namespace
from numbers import Number
from unittest.mock import MagicMock

import ignite.distributed as idist
import torch
from ignite.engine.engine import Engine
from {{project_name}}.trainers import create_trainers, evaluate_function, train_function, TrainEvents, train_events_to_attr
from torch import nn, optim


class TestEngines(unittest.TestCase):
    """Testing for engines.py"""

    def setUp(self):
        self.model = nn.Linear(1, 1)
        self.optimizer = optim.Adam(self.model.parameters())
        self.device = idist.device()
        self.loss_fn = nn.MSELoss()
        self.batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    def test_train_fn(self):
        engine = Engine(lambda e, b: 1)
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED, backward)
        engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED, optim)
        config = Namespace(use_amp=False)
        output = train_function(config, engine, self.batch, self.model, self.loss_fn, self.optimizer, self.device)
        self.assertIsInstance(output, dict)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 1)
        self.assertEqual(engine.state.optim_step_completed, 1)
        self.assertEqual(backward.call_count, 1)
        self.assertEqual(optim.call_count, 1)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_train_fn_event_filter(self):
        config = Namespace(use_amp=False)
        engine = Engine(
            lambda e, b: train_function(config, e, b, self.model, self.loss_fn, self.optimizer, self.device)
        )
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(
            TrainEvents.BACKWARD_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), backward
        )
        engine.add_event_handler(
            TrainEvents.OPTIM_STEP_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), optim
        )
        engine.run([self.batch] * 5)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 5)
        self.assertEqual(engine.state.optim_step_completed, 5)
        self.assertEqual(backward.call_count, 3)
        self.assertEqual(optim.call_count, 3)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_train_fn_every(self):
        config = Namespace(use_amp=False)
        engine = Engine(
            lambda e, b: train_function(config, e, b, self.model, self.loss_fn, self.optimizer, self.device)
        )
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(every=2), backward)
        engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(every=2), optim)
        engine.run([self.batch] * 5)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 5)
        self.assertEqual(engine.state.optim_step_completed, 5)
        self.assertEqual(backward.call_count, 2)
        self.assertEqual(optim.call_count, 2)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_train_fn_once(self):
        config = Namespace(use_amp=False)
        engine = Engine(
            lambda e, b: train_function(config, e, b, self.model, self.loss_fn, self.optimizer, self.device)
        )
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(once=3), backward)
        engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(once=3), optim)
        engine.run([self.batch] * 5)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 5)
        self.assertEqual(engine.state.optim_step_completed, 5)
        self.assertEqual(backward.call_count, 1)
        self.assertEqual(optim.call_count, 1)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_evaluate_fn(self):
        engine = Engine(lambda e, b: 1)
        config = Namespace(use_amp=False)
        output = evaluate_function(config, engine, self.batch, self.model, self.device)
        self.assertIsInstance(output, tuple)

    def test_create_trainers(self):
        train_engine, eval_engine = create_trainers(
            config=Namespace(use_amp=True),
            model=self.model,
            loss_fn=self.loss_fn,
            optimizer=self.optimizer,
            device=self.device,
        )
        self.assertIsInstance(train_engine, Engine)
        self.assertIsInstance(eval_engine, Engine)
        self.assertTrue(hasattr(train_engine.state, "backward_completed"))
        self.assertTrue(hasattr(train_engine.state, "optim_step_completed"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
