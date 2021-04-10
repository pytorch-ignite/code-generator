import logging
import unittest
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock

import ignite.distributed as idist
import torch
from config import get_default_parser
from datasets import get_datasets
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
from ignite.contrib.handlers.param_scheduler import ParamScheduler
from ignite.engine import Engine
from ignite.handlers.checkpoint import Checkpoint
from ignite.handlers.early_stopping import EarlyStopping
from ignite.handlers.timing import Timer
from ignite.utils import setup_logger
from torch import nn, optim
from torch.optim.lr_scheduler import _LRScheduler
from torch.utils.data import Dataset
from trainers import (
    TrainEvents,
    create_trainers,
    evaluate_function,
    train_events_to_attr,
    train_function,
)
from utils import hash_checkpoint, initialize, log_metrics, resume_from, setup_logging, get_handlers, get_logger


class TestDataset(unittest.TestCase):
    def test_get_datasets(self):
        with TemporaryDirectory() as tmp:
            train_ds, eval_ds = get_datasets(tmp)
            assert isinstance(train_ds, Dataset)
            assert isinstance(eval_ds, Dataset)


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


class TestEngines(unittest.TestCase):
    """Testing for engines.py"""

    def setUp(self):
        self.model = nn.Linear(1, 1)
        self.optimizer = optim.Adam(self.model.parameters())
        self.device = idist.device()
        self.loss_fn = nn.MSELoss()
        self.batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    def test_train_fn(self):
        engine = Engine(lambda e, b: 1)
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED, backward)
        engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED, optim)
        config = Namespace(use_amp=False)
        output = train_function(config, engine, self.batch, self.model, self.loss_fn, self.optimizer, self.device)
        self.assertIsInstance(output, dict)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 1)
        self.assertEqual(engine.state.optim_step_completed, 1)
        self.assertEqual(backward.call_count, 1)
        self.assertEqual(optim.call_count, 1)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_train_fn_event_filter(self):
        config = Namespace(use_amp=False)
        engine = Engine(
            lambda e, b: train_function(config, e, b, self.model, self.loss_fn, self.optimizer, self.device)
        )
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(
            TrainEvents.BACKWARD_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), backward
        )
        engine.add_event_handler(
            TrainEvents.OPTIM_STEP_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), optim
        )
        engine.run([self.batch] * 5)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 5)
        self.assertEqual(engine.state.optim_step_completed, 5)
        self.assertEqual(backward.call_count, 3)
        self.assertEqual(optim.call_count, 3)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_train_fn_every(self):
        config = Namespace(use_amp=False)
        engine = Engine(
            lambda e, b: train_function(config, e, b, self.model, self.loss_fn, self.optimizer, self.device)
        )
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(every=2), backward)
        engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(every=2), optim)
        engine.run([self.batch] * 5)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 5)
        self.assertEqual(engine.state.optim_step_completed, 5)
        self.assertEqual(backward.call_count, 2)
        self.assertEqual(optim.call_count, 2)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_train_fn_once(self):
        config = Namespace(use_amp=False)
        engine = Engine(
            lambda e, b: train_function(config, e, b, self.model, self.loss_fn, self.optimizer, self.device)
        )
        engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
        backward = MagicMock()
        optim = MagicMock()
        engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(once=3), backward)
        engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(once=3), optim)
        engine.run([self.batch] * 5)
        self.assertTrue(hasattr(engine.state, "backward_completed"))
        self.assertTrue(hasattr(engine.state, "optim_step_completed"))
        self.assertEqual(engine.state.backward_completed, 5)
        self.assertEqual(engine.state.optim_step_completed, 5)
        self.assertEqual(backward.call_count, 1)
        self.assertEqual(optim.call_count, 1)
        self.assertTrue(backward.called)
        self.assertTrue(optim.called)

    def test_evaluate_fn(self):
        engine = Engine(lambda e, b: 1)
        config = Namespace(use_amp=False)
        output = evaluate_function(config, engine, self.batch, self.model, self.device)
        self.assertIsInstance(output, tuple)

    def test_create_trainers(self):
        train_engine, eval_engine = create_trainers(
            config=Namespace(use_amp=True),
            model=self.model,
            loss_fn=self.loss_fn,
            optimizer=self.optimizer,
            device=self.device,
        )
        self.assertIsInstance(train_engine, Engine)
        self.assertIsInstance(eval_engine, Engine)
        self.assertTrue(hasattr(train_engine.state, "backward_completed"))
        self.assertTrue(hasattr(train_engine.state, "optim_step_completed"))


class TestUtils(unittest.TestCase):
    """Testing utils.py"""

    def test_initialize(self):
        config = Namespace(
            model="squeezenet1_0",
            lr=1e-3,
            momentum=0.9,
            weight_decay=1e-4,
            num_iters_per_epoch=1,
            num_warmup_epochs=1,
            max_epochs=1,
        )
        model, optimizer, loss_fn, lr_scheduler = initialize(config)
        self.assertIsInstance(model, nn.Module)
        self.assertIsInstance(optimizer, optim.Optimizer)
        self.assertIsInstance(loss_fn, nn.Module)
        self.assertIsInstance(lr_scheduler, (_LRScheduler, ParamScheduler))

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
