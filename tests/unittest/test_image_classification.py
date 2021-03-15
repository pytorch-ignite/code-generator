import sys
import unittest
from argparse import ArgumentParser

import ignite.distributed as idist
from hypothesis import given, settings
from hypothesis import strategies as st
from ignite.engine import Engine
from torch.nn import Module
from torch.utils.data import DataLoader, Dataset
from torch.utils.data._utils.collate import default_collate
from torch.utils.data.sampler import RandomSampler, SequentialSampler

sys.path.append("./tests/templates/dist/image_classification")

from datasets import get_data_loaders, get_datasets
from models import get_model
from utils import get_default_parser, log_metrics


class ImageClassiTester(unittest.TestCase):

    # test datasets.py
    @settings(deadline=None, derandomize=True)
    @given(st.integers(min_value=1, max_value=128), st.integers(min_value=0, max_value=2))
    def test_datasets(self, train_batch_size, num_workers):
        train_dataset, eval_dataset = get_datasets("./")

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
        self.assertIsInstance(model, Module)
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
            log_metrics(engine, "train", idist.device())
        self.assertEqual(log.output[0], "INFO:root:train [2/200]: {}")


if __name__ == "__main__":
    unittest.main()
