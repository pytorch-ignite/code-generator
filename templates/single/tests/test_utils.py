import logging
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from argparse import ArgumentParser, Namespace

import torch
from ignite.engine import Engine

from single_cg.utils import get_default_parser, log_metrics, setup_logging, hash_checkpoint


class TestUtils(unittest.TestCase):

    # test get_default_parser of utils.py
    def test_get_default_parser(self):
        parser = get_default_parser()
        self.assertIsInstance(parser, ArgumentParser)
        self.assertFalse(parser.add_help)

    # test log_metrics of utils.py
    def test_log_metrics(self):
        engine = Engine(lambda e, b: None)
        engine.run(list(range(100)), max_epochs=2)
        with self.assertLogs() as log:
            log_metrics(engine, "train")
        self.assertEqual(log.output[0], "INFO:ignite.engine.engine.Engine:train [2/200]: {}")

    # test setup_logging of utils.py
    def test_setup_logging(self):
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            config = Namespace(verbose=True, filepath=tmp)
            logger = setup_logging(config)
            self.assertEqual(logger.level, logging.INFO)
            self.assertIsInstance(logger, logging.Logger)
            self.assertTrue(next(tmp.rglob("*.log")).is_file())

    # test hash_checkpoint of utils.py
    def test_hash_checkpoint(self):
        with TemporaryDirectory() as tmp:
            # download lightweight model
            model = torch.hub.load("pytorch/vision", "squeezenet1_0")
            # jit it
            scripted_model = torch.jit.script(model)
            # save jitted model : find a jitted checkpoint
            torch.jit.save(scripted_model, f"{tmp}/squeezenet1_0.ckptc")
            # download un-jitted model
            torch.hub.download_url_to_file(
                "https://download.pytorch.org/models/squeezenet1_0-a815701f.pth",
                f"{tmp}/squeezenet1_0.ckpt",
            )

            checkpoint = f"{tmp}/squeezenet1_0.ckpt"
            filename, sha_hash = hash_checkpoint(checkpoint, False, tmp)
            model.load_state_dict(torch.load(f"{tmp}/{filename}"), True)
            self.assertEqual(sha_hash[:8], "a815701f")
            self.assertEqual(filename, f"squeezenet1_0-{sha_hash[:8]}.pt")

            checkpoint = f"{tmp}/squeezenet1_0.ckptc"
            filename, sha_hash = hash_checkpoint(checkpoint, True, tmp)
            scripted_model = torch.jit.load(f"{tmp}/{filename}")
            self.assertEqual(filename, f"squeezenet1_0-{sha_hash[:8]}.ptc")


if __name__ == "__main__":
    unittest.main()
