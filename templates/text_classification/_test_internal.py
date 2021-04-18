import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from unittest.mock import MagicMock

import pytest

import torch
from torch import nn, optim

from ignite.engine import Engine
from ignite.handlers.checkpoint import Checkpoint
from ignite.handlers.early_stopping import EarlyStopping
from ignite.handlers.timing import Timer
from ignite.utils import setup_logger
from ignite.contrib.handlers.base_logger import BaseLogger
from ignite.contrib.handlers import (
    ClearMLLogger,
    MLflowLogger,
    NeptuneLogger,
    PolyaxonLogger,
    TensorboardLogger,
    VisdomLogger,
    WandBLogger,
)

from test_all import set_up
from trainers import create_trainer, create_evaluator, create_trainers
from utils import get_default_parser, log_metrics, resume_from, setup_logging, get_handlers, get_logger


def test_get_handlers(tmp_path):
    trainer = Engine(lambda e, b: b)
    config = Namespace(
        output_dir=tmp_path,
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
        trainer=trainer,
        evaluator=trainer,
        metric_name="eval_loss",
        es_metric_name="eval_loss",
    )
    assert isinstance(bm_handler, (type(None), Checkpoint)), "Should be Checkpoint or None"
    assert isinstance(es_handler, (type(None), EarlyStopping)), "Should be EarlyStopping or None"
    assert isinstance(timer_handler, (type(None), Timer)), "Should be Timer or None"


def test_get_logger(tmp_path):
    config = Namespace(output_dir=tmp_path, logger_log_every_iters=1)
    trainer = Engine(lambda e, b: b)
    optimizer = optim.Adam(nn.Linear(1, 1).parameters())
    logger_handler = get_logger(
        config=config,
        trainer=trainer,
        evaluator=trainer,
        optimizers=optimizer,
    )
    types = (
        BaseLogger,
        ClearMLLogger,
        MLflowLogger,
        NeptuneLogger,
        PolyaxonLogger,
        TensorboardLogger,
        VisdomLogger,
        WandBLogger,
        type(None),
    )
    assert isinstance(logger_handler, types), "Should be Ignite provided loggers or None"


def test_create_trainer():
    config = Namespace(use_amp=False)
    model, optimizer, loss_fn, device = set_up()
    trainer = create_trainer(config, model, optimizer, loss_fn, device)
    assert isinstance(trainer, Engine)


def test_create_evaluator():
    config = Namespace(use_amp=False)
    model, _, loss_fn, device = set_up()
    evaluator = create_evaluator(config, model, loss_fn, device)
    assert isinstance(evaluator, Engine)


def test_create_trainers():
    config = Namespace(use_amp=False)
    model, optimizer, loss_fn, device = set_up()
    trainer, evaluator = create_trainers(config, model, optimizer, loss_fn, device)
    assert isinstance(trainer, Engine)
    assert isinstance(evaluator, Engine)


def test_get_default_parser():
    parser = get_default_parser({})
    assert isinstance(parser, ArgumentParser)
    assert not parser.add_help


def test_log_metrics(capsys):
    engine = Engine(lambda e, b: None)
    engine.logger = setup_logger(format="%(message)s")
    engine.run(list(range(100)), max_epochs=2)
    log_metrics(engine, "train")
    captured = capsys.readouterr()
    assert captured.err.split("\n")[-2] == "train [2/200]: {}"


def test_setup_logging(tmp_path):
    config = Namespace(verbose=True, output_dir=tmp_path)
    logger = setup_logging(config)
    assert logger.level == logging.INFO
    assert isinstance(logger, logging.Logger)
    assert next(tmp_path.rglob("*.log")).is_file()


def test_resume_from_url(tmp_path, caplog):
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    checkpoint_fp = "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth"
    model = torch.hub.load("pytorch/vision", "squeezenet1_0")
    to_load = {"model": model}
    with caplog.at_level(logging.INFO):
        resume_from(to_load, checkpoint_fp, logger, model_dir=tmp_path)
        assert "Successfully resumed from a checkpoint" in caplog.messages[0], "checkpoint fail to load"


def test_resume_from_fp(tmp_path, caplog):
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    torch.hub.download_url_to_file(
        "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth",
        f"{tmp_path}/squeezenet1_0.pt",
    )
    checkpoint_fp = f"{tmp_path}/squeezenet1_0.pt"
    model = torch.hub.load("pytorch/vision", "squeezenet1_0")
    to_load = {"model": model}
    with caplog.at_level(logging.INFO):
        resume_from(to_load, checkpoint_fp, logger)
        assert "Successfully resumed from a checkpoint" in caplog.messages[0], "checkpoint fail to load"

    torch.hub.download_url_to_file(
        "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth",
        f"{tmp_path}/squeezenet1_0.pt",
    )
    checkpoint_fp = Path(f"{tmp_path}/squeezenet1_0.pt")
    model = torch.hub.load("pytorch/vision", "squeezenet1_0")
    to_load = {"model": model}
    with caplog.at_level(logging.INFO):
        resume_from(to_load, checkpoint_fp, logger)
        assert "Successfully resumed from a checkpoint" in caplog.messages[0], "checkpoint fail to load"


def test_resume_from_error():
    with pytest.raises(FileNotFoundError, match=r"Given \w+ does not exist"):
        resume_from({}, "abcdef/", None)
