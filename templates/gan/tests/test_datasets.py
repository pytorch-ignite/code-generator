import unittest
from tempfile import TemporaryDirectory

from torch.utils.data import Dataset

from {{project_name}}.datasets import get_datasets


class TestDataset(unittest.TestCase):

    def test_get_datasets(self):
        with TemporaryDirectory() as tmp:
            dataset, nc = get_datasets("cifar10", tmp)

            self.assertIsInstance(dataset, Dataset)
            self.assertEqual(nc, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
