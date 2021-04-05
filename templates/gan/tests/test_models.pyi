import unittest

from torch import nn

from {{project_name}}.models import Discriminator, Generator


class TestModels(unittest.TestCase):

    def test_models(self):
        model_G = Generator(100, 64, 3)
        model_D = Discriminator(3, 64)

        self.assertIsInstance(model_D, nn.Module)
        self.assertIsInstance(model_G, nn.Module)


if __name__ == "__main__":
    unittest.main(verbosity=2)
