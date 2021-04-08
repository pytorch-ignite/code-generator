import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path

import ignite.distributed as idist
import pytest
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
from models import Discriminator, Generator
from torch import nn, optim
from torch.utils.data import Dataset
from trainers import create_trainers, train_function
from utils import hash_checkpoint, resume_from, setup_logging


def setUp():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    return model, optimizer, device, loss_fn, batch


def test_get_datasets(tmp_path):
    dataset, nc = get_datasets("cifar10", tmp_path)

    assert isinstance(dataset, Dataset)
    assert nc == 3


def test_get_handlers(tmp_path):
    train_engine = Engine(lambda e, b: b)
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
        train_engine=train_engine,
        eval_engine=train_engine,
        metric_name="eval_loss",
        es_metric_name="eval_loss",
    )
    assert isinstance(bm_handler, (type(None), Checkpoint)), "Should be Checkpoint or None"
    assert isinstance(es_handler, (type(None), EarlyStopping)), "Should be EarlyStopping or None"
    assert isinstance(timer_handler, (type(None), Timer)), "Shoulde be Timer or None"


def test_get_logger(tmp_path):
    config = Namespace(output_dir=tmp_path, logger_log_every_iters=1)
    train_engine = Engine(lambda e, b: b)
    optimizer = optim.Adam(nn.Linear(1, 1).parameters())
    logger_handler = get_logger(
        config=config,
        train_engine=train_engine,
        eval_engine=train_engine,
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


def test_models():
    model_G = Generator(100, 64, 3)
    model_D = Discriminator(3, 64)

    assert isinstance(model_D, nn.Module)
    assert isinstance(model_G, nn.Module)


def test_train_fn():
    model, optimizer, device, loss_fn, batch = setUp()
    real_labels = torch.ones(2, device=device)
    fake_labels = torch.zeros(2, device=device)
    engine = Engine(lambda e, b: 1)
    config = Namespace(use_amp=False, batch_size=2, z_dim=100)
    output = train_function(
        config,
        engine,
        batch,
        model,
        model,
        loss_fn,
        optimizer,
        optimizer,
        device,
        real_labels,
        fake_labels,
    )
    assert isinstance(output, dict)


def test_create_trainers():
    model, optimizer, device, loss_fn, batch = setUp()
    real_labels = torch.ones(2, device=device)
    fake_labels = torch.zeros(2, device=device)
    train_engine = create_trainers(
        config=Namespace(use_amp=True),
        netD=model,
        netG=model,
        loss_fn=loss_fn,
        optimizerD=optimizer,
        optimizerG=optimizer,
        device=device,
        real_labels=real_labels,
        fake_labels=fake_labels,
    )
    assert isinstance(train_engine, Engine)


def test_get_default_parser():
    parser = get_default_parser()
    assert isinstance(parser, ArgumentParser)
    assert not parser.add_help


def test_setup_logging(tmp_path):
    config = Namespace(verbose=True, output_dir=tmp_path)
    logger = setup_logging(config)
    assert logger.level == logging.INFO
    assert isinstance(logger, logging.Logger)
    assert next(tmp_path.rglob("*.log")).is_file()


def test_hash_checkpoint(tmp_path):
    # download lightweight model
    model = torch.hub.load("pytorch/vision", "squeezenet1_0")
    # jit it
    scripted_model = torch.jit.script(model)
    # save jitted model : find a jitted checkpoint
    torch.jit.save(scripted_model, f"{tmp_path}/squeezenet1_0.ckptc")
    # download un-jitted model
    torch.hub.download_url_to_file(
        "https://download.pytorch.org/models/squeezenet1_0-b66bff10.pth",
        f"{tmp_path}/squeezenet1_0.ckpt",
    )

    checkpoint = f"{tmp_path}/squeezenet1_0.ckpt"
    hashed_fp, sha_hash = hash_checkpoint(checkpoint, False, tmp_path)
    model.load_state_dict(torch.load(hashed_fp), True)
    assert sha_hash[:8] == "b66bff10"
    assert hashed_fp.name == f"squeezenet1_0-{sha_hash[:8]}.pt"

    checkpoint = f"{tmp_path}/squeezenet1_0.ckptc"
    hashed_fp, sha_hash = hash_checkpoint(checkpoint, True, tmp_path)
    scripted_model = torch.jit.load(hashed_fp)
    assert hashed_fp.name == f"squeezenet1_0-{sha_hash[:8]}.ptc"


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
