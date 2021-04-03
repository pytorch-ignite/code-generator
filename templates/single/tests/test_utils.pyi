import logging
import unittest
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

import torch
from ignite.engine import Engine
from ignite.utils import setup_logger
from {{project_name}}.utils import (
    get_default_parser,
    hash_checkpoint,
    log_metrics,
    resume_from,
    setup_logging,
)


class TestUtils(unittest.TestCase):
    """Testing utils.py"""

    def test_get_default_parser(self):
        parser = get_default_parser()
        self.assertIsInstance(parser, ArgumentParser)
        self.assertFalse(parser.add_help)

    def test_log_metrics(self):
        engine = Engine(lambda e, b: None)
        engine.logger = setup_logger(format="%(message)s")
        engine.run(list(range(100)), max_epochs=2)
        with self.assertLogs() as log:
            log_metrics(engine, "train")
        self.assertEqual(log.output[0], "INFO:root:train [2/200]: {}")

    def test_setup_logging(self):
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            config = Namespace(verbose=True, filepath=tmp)
            logger = setup_logging(config)
            self.assertEqual(logger.level, logging.INFO)
            self.assertIsInstance(logger, logging.Logger)
            self.assertTrue(next(tmp.rglob("*.log")).is_file())

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
                "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth",
                f"{tmp}/squeezenet1_0.ckpt",
            )

            checkpoint = f"{tmp}/squeezenet1_0.ckpt"
            hashed_fp, sha_hash = hash_checkpoint(checkpoint, False, tmp)
            model.load_state_dict(torch.load(hashed_fp), True)
            self.assertEqual(sha_hash[:8], "b66bff10")
            self.assertEqual(hashed_fp.name, f"squeezenet1_0-{sha_hash[:8]}.pt")

            checkpoint = f"{tmp}/squeezenet1_0.ckptc"
            hashed_fp, sha_hash = hash_checkpoint(checkpoint, True, tmp)
            scripted_model = torch.jit.load(hashed_fp)
            self.assertEqual(hashed_fp.name, f"squeezenet1_0-{sha_hash[:8]}.ptc")

    def test_resume_from_url(self):
        logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO)
        with TemporaryDirectory() as tmp:
            checkpoint_fp = "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth"
            model = torch.hub.load("pytorch/vision", "squeezenet1_0")
            to_load = {"model": model}
            with self.assertLogs() as log:
                resume_from(to_load, checkpoint_fp, logger, model_dir=tmp)
            self.assertRegex(log.output[0], r"Successfully resumed from a checkpoint", "checkpoint fail to load")

    def test_resume_from_fp(self):
        logger = logging.getLogger()
        logging.basicConfig(level=logging.INFO)
        with TemporaryDirectory() as tmp:
            torch.hub.download_url_to_file(
                "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth",
                f"{tmp}/squeezenet1_0.pt",
            )
            checkpoint_fp = f"{tmp}/squeezenet1_0.pt"
            model = torch.hub.load("pytorch/vision", "squeezenet1_0")
            to_load = {"model": model}
            with self.assertLogs() as log:
                resume_from(to_load, checkpoint_fp, logger)
            self.assertRegex(log.output[0], r"Successfully resumed from a checkpoint", "checkpoint fail to load")

        with TemporaryDirectory() as tmp:
            torch.hub.download_url_to_file(
                "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth",
                f"{tmp}/squeezenet1_0.pt",
            )
            checkpoint_fp = Path(f"{tmp}/squeezenet1_0.pt")
            model = torch.hub.load("pytorch/vision", "squeezenet1_0")
            to_load = {"model": model}
            with self.assertLogs() as log:
                resume_from(to_load, checkpoint_fp, logger)
            self.assertRegex(log.output[0], r"Successfully resumed from a checkpoint", "checkpoint fail to load")

    def test_resume_from_error(self):
        with self.assertRaisesRegex(FileNotFoundError, r"Given \w+ does not exist"):
            resume_from({}, "abcdef/", None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
