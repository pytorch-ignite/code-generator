import shutil
import tempfile
import unittest
from argparse import Namespace

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
from ignite.engine.engine import Engine
from ignite.handlers.checkpoint import Checkpoint
from ignite.handlers.early_stopping import EarlyStopping
from ignite.handlers.timing import Timer
from single_cg.handlers import get_handlers, get_logger
from torch import nn, optim


class TestHandlers(unittest.TestCase):
    """Testing handlers.py"""

    def setUp(self) -> None:
        self.tmp = tempfile.mkdtemp()
        return super().setUp()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)
        return super().tearDown()

    def test_get_handlers(self):
        train_engine = Engine(lambda e, b: b)
        config = Namespace(
            output_path=self.tmp,
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
        config = Namespace(logger_log_every_iters=1)
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


if __name__ == "__main__":
    unittest.main()
