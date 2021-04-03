import unittest
from argparse import Namespace
from numbers import Number
from unittest.mock import MagicMock

import ignite.distributed as idist
import torch
from ignite.engine.engine import Engine
from {{project_name}}.trainers import create_trainers, train_function
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
        real_labels = torch.ones(2, device=self.device)
        fake_labels = torch.zeros(2, device=self.device)
        engine = Engine(lambda e, b: 1)
        config = Namespace(use_amp=False, batch_size=2, z_dim=100)
        output = train_function(
            config,
            engine,
            self.batch,
            self.model,
            self.model,
            self.loss_fn,
            self.optimizer,
            self.optimizer,
            self.device,
            real_labels,
            fake_labels,
        )
        self.assertIsInstance(output, dict)

    def test_create_trainers(self):
        real_labels = torch.ones(2, device=self.device)
        fake_labels = torch.zeros(2, device=self.device)
        train_engine = create_trainers(
            config=Namespace(use_amp=True),
            netD=self.model,
            netG=self.model,
            loss_fn=self.loss_fn,
            optimizerD=self.optimizer,
            optimizerG=self.optimizer,
            device=self.device,
            real_labels=real_labels,
            fake_labels=fake_labels,
        )
        self.assertIsInstance(train_engine, Engine)


if __name__ == "__main__":
    unittest.main(verbosity=2)
