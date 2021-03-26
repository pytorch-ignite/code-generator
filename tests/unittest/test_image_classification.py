import os
import sys
import unittest
from argparse import ArgumentParser, Namespace

import ignite.distributed as idist
import torch
from common_utils import get_tmp_dir
from hypothesis import given, settings
from hypothesis import strategies as st
from ignite.engine import Engine
from ignite.handlers import Checkpoint
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset
from torch.utils.data._utils.collate import default_collate
from torch.utils.data.sampler import RandomSampler, SequentialSampler

sys.path.append("./tests/dist/image_classification")

from datasets import get_data_loaders, get_datasets
from models import get_model
from utils import (
    get_default_parser,
    initialize,
    log_metrics,
    setup_common_handlers,
    setup_exp_logging,
)


class ImageClassiTester(unittest.TestCase):
    # test datasets.py
    @settings(deadline=None, derandomize=True)
    @given(st.integers(min_value=1, max_value=4), st.integers(min_value=0, max_value=1))
    def test_datasets(self, train_batch_size, num_workers):
        train_dataset, eval_dataset = get_datasets("/tmp/cifar10")

        self.assertIsInstance(train_dataset, Dataset)
        self.assertIsInstance(eval_dataset, Dataset)
        self.assertTrue(train_dataset.train)
        self.assertFalse(eval_dataset.train)

        train_dataloader, eval_dataloader = get_data_loaders(
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            train_batch_size=train_batch_size,
            eval_batch_size=train_batch_size,
            num_workers=num_workers,
        )

        self.assertIsInstance(train_dataloader, DataLoader)
        self.assertIsInstance(eval_dataloader, DataLoader)
        self.assertIsInstance(train_dataloader.sampler, RandomSampler)
        self.assertIsInstance(eval_dataloader.sampler, SequentialSampler)
        self.assertEqual(train_dataloader.batch_sampler.batch_size, train_batch_size)
        self.assertEqual(train_dataloader.batch_sampler.batch_size, train_batch_size)
        self.assertEqual(eval_dataloader.batch_sampler.batch_size, train_batch_size)
        self.assertEqual(train_dataloader.collate_fn, default_collate)
        self.assertEqual(eval_dataloader.collate_fn, default_collate)
        self.assertEqual(train_dataloader.drop_last, False)
        self.assertEqual(eval_dataloader.drop_last, False)
        self.assertEqual(train_dataloader.num_workers, num_workers)
        self.assertEqual(eval_dataloader.num_workers, num_workers)
        if idist.device().type == "cpu":
            self.assertFalse(train_dataloader.pin_memory)
            self.assertFalse(eval_dataloader.pin_memory)
        else:
            self.assertTrue(train_dataloader.pin_memory)
            self.assertTrue(eval_dataloader.pin_memory)

    # test models.py
    @settings(deadline=None, derandomize=True)
    @given(st.sampled_from(["squeezenet1_0", "squeezenet1_1"]))
    def test_models(self, name):
        model = get_model(name)
        self.assertIsInstance(model, nn.Module)
        self.assertEqual(model.num_classes, 10)

    # test get_default_parser of utils.py
    def test_get_default_parser(self):
        parser = get_default_parser()
        self.assertIsInstance(parser, ArgumentParser)
        self.assertFalse(parser.add_help)

    # test log_metrics of utils.py
    def test_log_metrics(self):
        engine = Engine(lambda engine, batch: None)
        engine.run(list(range(100)), max_epochs=2)
        with self.assertLogs() as log:
            log_metrics(engine, "train", torch.device("cpu"))
        self.assertEqual(log.output[0], "INFO:ignite.engine.engine.Engine:train [2/0200]: {}")

    # test initialize of utils.py
    def test_initialize(self):
        config = Namespace(model_name="alexnet", lr=0.01)
        device, model, optimizer, loss_fn = initialize(config)
        self.assertIsInstance(device, torch.device)
        self.assertIsInstance(model, nn.Module)
        self.assertIsInstance(optimizer, optim.Optimizer)
        self.assertIsInstance(loss_fn, nn.Module)

    # test setup_common_handlers of utils.py
    def test_setup_common_handlers(self):
        data = [1, 2, 3]
        max_epochs = 3
        model = nn.Linear(1, 1)
        optimizer = optim.Adam(model.parameters())
        engine = Engine(lambda e, b: b)
        engine.state.metrics = {"eval_accuracy": 1}
        with get_tmp_dir() as tmpdir:
            config = Namespace(filepath=tmpdir, n_saved=2, save_every_iters=1)
            handler = setup_common_handlers(
                config=config,
                eval_engine=engine,
                train_engine=engine,
                model=model,
                optimizer=optimizer,
            )
            engine.run(data, max_epochs=max_epochs)
            self.assertIsInstance(handler, Checkpoint)
            self.assertTrue(os.path.isfile(f"{tmpdir}/training_checkpoint_{len(data) * max_epochs}.pt"))
            self.assertTrue(
                handler.last_checkpoint,
                f"{tmpdir}/best_model_3_eval_eval_accuracy=1.0000.pt",
            )

    # test setup_exp_logging of utils.py
    def test_setup_exp_logging(self):
        self.assertIsNone(setup_exp_logging(train_engine=None, config=None))


if __name__ == "__main__":
    unittest.main()
