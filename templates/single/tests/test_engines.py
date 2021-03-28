import unittest
from numbers import Number

import ignite.distributed as idist
import torch
from ignite.engine.engine import Engine
from single_cg.engines import create_engines, evaluate_fn, train_fn
from torch import nn, optim


class TestEngines(unittest.TestCase):
    """Testing for engines.py"""

    def setUp(self):
        self.model = nn.Linear(1, 1)
        self.optimizer = optim.Adam(self.model.parameters())
        self.device = idist.device()
        self.loss_fn = nn.MSELoss()
        self.batch = [torch.tensor([1.0]), torch.tensor([1.0])]
        self.engine = Engine(lambda e, b: b)

    def test_train_fn(self):
        output = train_fn(None, self.engine, self.batch, self.model, self.loss_fn, self.optimizer, self.device)
        self.assertIsInstance(output, Number)

    def test_evaluate_fn(self):
        output = evaluate_fn(None, self.engine, self.batch, self.model, self.loss_fn, self.device)
        self.assertIsInstance(output, Number)

    def test_create_engines(self):
        train_engine, eval_engine = create_engines(
            config=None,
            engine=self.engine,
            batch=self.batch,
            model=self.model,
            loss_fn=self.loss_fn,
            optimizer=self.optimizer,
            device=self.device,
        )
        self.assertIsInstance(train_engine, Engine)
        self.assertIsInstance(eval_engine, Engine)


if __name__ == "__main__":
    unittest.main()
