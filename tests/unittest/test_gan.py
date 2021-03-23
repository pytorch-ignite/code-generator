import sys
import unittest
from argparse import ArgumentParser

from torch import nn
from torch.utils.data import Dataset

sys.path.append("./tests/dist/")

from gan.datasets import get_datasets
from gan.models import Discriminator, Generator
from gan.utils import get_default_parser


class GANTester(unittest.TestCase):
    # test datasets.py
    def test_datasets(self):
        dataset, nc = get_datasets("cifar10", "/tmp/cifar10")

        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(nc, 3)

    # test models.py
    def test_models(self):
        model_G = Generator(100, 64, 3)
        model_D = Discriminator(3, 64)

        self.assertIsInstance(model_D, nn.Module)
        self.assertIsInstance(model_G, nn.Module)

    # test get_default_parser of utils.py
    def test_get_default_parser(self):
        parser = get_default_parser()
        self.assertIsInstance(parser, ArgumentParser)
        self.assertFalse(parser.add_help)


if __name__ == "__main__":
    unittest.main()
