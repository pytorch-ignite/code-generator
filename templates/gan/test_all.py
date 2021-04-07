import logging
import unittest
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

import ignite.distributed as idist
import torch
from config import get_default_parser
from datasets import get_datasets
from handlers import get_handlers, get_logger
from ignite.contrib.handlers import (
    ClearMLLogger,
    MLflowLogger,
    NeptuneLogger,
    PolyaxonLogger,
    TensorboardLogger,
    VisdomLogger,
    WandBLogger,
)
from ignite.contrib.handlers.base_logger import BaseLogger
from ignite.engine import Engine
from ignite.handlers.checkpoint import Checkpoint
from ignite.handlers.early_stopping import EarlyStopping
from ignite.handlers.timing import Timer
from ignite.utils import setup_logger
from models import Discriminator, Generator
from torch import nn, optim
from torch.utils.data import Dataset
from trainers import create_trainers, train_function
from utils import hash_checkpoint, log_metrics, resume_from, setup_logging


class TestDataset(unittest.TestCase):
    def test_get_datasets(self):
        with TemporaryDirectory() as tmp:
            dataset, nc = get_datasets("cifar10", tmp)

            self.assertIsInstance(dataset, Dataset)
            self.assertEqual(nc, 3)


class TestHandlers(unittest.TestCase):
    """Testing handlers.py"""

    def test_get_handlers(self):
        train_engine = Engine(lambda e, b: b)
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            config = Namespace(
                output_dir=tmp,
                save_every_iters=1,
                n_saved=2,
                log_every_iters=1,
                with_pbars=False,
                with_pbar_on_iters=False,
                stop_on_nan=False,
                clear_cuda_cache=False,
                with_gpu_stats=False,
                patience=1,
                limit_sec=30,
            )
            bm_handler, es_handler, timer_handler = get_handlers(
                config=config,
                model=nn.Linear(1, 1),
                train_engine=train_engine,
                eval_engine=train_engine,
                metric_name="eval_loss",
                es_metric_name="eval_loss",
            )
            self.assertIsInstance(bm_handler, (type(None), Checkpoint), "Should be Checkpoint or None")
            self.assertIsInstance(es_handler, (type(None), EarlyStopping), "Should be EarlyStopping or None")
            self.assertIsInstance(timer_handler, (type(None), Timer), "Shoulde be Timer or None")

    def test_get_logger(self):
        with TemporaryDirectory() as tmp:
            config = Namespace(output_dir=tmp, logger_log_every_iters=1)
            train_engine = Engine(lambda e, b: b)
            optimizer = optim.Adam(nn.Linear(1, 1).parameters())
            logger_handler = get_logger(
                config=config,
                train_engine=train_engine,
                eval_engine=train_engine,
                optimizers=optimizer,
            )
            self.assertIsInstance(
                logger_handler,
                (
                    BaseLogger,
                    ClearMLLogger,
                    MLflowLogger,
                    NeptuneLogger,
                    PolyaxonLogger,
                    TensorboardLogger,
                    VisdomLogger,
                    WandBLogger,
                    type(None),
                ),
                "Should be Ignite provided loggers or None",
            )


class TestModels(unittest.TestCase):
    def test_models(self):
        model_G = Generator(100, 64, 3)
        model_D = Discriminator(3, 64)

        self.assertIsInstance(model_D, nn.Module)
        self.assertIsInstance(model_G, nn.Module)


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
            config = Namespace(verbose=True, output_dir=tmp)
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
