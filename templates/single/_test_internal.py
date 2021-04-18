import logging
from argparse import ArgumentParser, Namespace
from numbers import Number
from pathlib import Path
from unittest.mock import MagicMock

import ignite.distributed as idist
import pytest
import torch
from config import get_default_parser

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
from ignite.utils import setup_logger
from torch import nn, optim
from trainers import (
    TrainEvents,
    create_trainers,
    evaluate_function,
    train_events_to_attr,
    train_function,
)
from utils import hash_checkpoint, log_metrics, resume_from, setup_logging, get_handlers, get_logger


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    batch = [torch.tensor([1.0]), torch.tensor([1.0])]

    return model, optimizer, device, loss_fn, batch


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
    assert isinstance(timer_handler, (type(None), Timer)), "Shoulde be Timer or None"


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


def test_train_fn():
    model, optimizer, device, loss_fn, batch = set_up()
    engine = Engine(lambda e, b: 1)
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED, backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED, optim)
    config = Namespace(use_amp=False)
    output = train_function(config, engine, batch, model, loss_fn, optimizer, device)
    assert isinstance(output, Number)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 1
    assert engine.state.optim_step_completed == 1
    assert backward.call_count == 1
    assert optim.call_count == 1
    assert backward.called
    assert optim.called


def test_train_fn_event_filter():
    model, optimizer, device, loss_fn, batch = set_up()
    config = Namespace(use_amp=False)
    engine = Engine(lambda e, b: train_function(config, e, b, model, loss_fn, optimizer, device))
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(event_filter=lambda _, x: (x % 2 == 0) or x == 3), optim)
    engine.run([batch] * 5)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 5
    assert engine.state.optim_step_completed == 5
    assert backward.call_count == 3
    assert optim.call_count == 3
    assert backward.called
    assert optim.called


def test_train_fn_every():
    model, optimizer, device, loss_fn, batch = set_up()

    config = Namespace(use_amp=False)
    engine = Engine(lambda e, b: train_function(config, e, b, model, loss_fn, optimizer, device))
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(every=2), backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(every=2), optim)
    engine.run([batch] * 5)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 5
    assert engine.state.optim_step_completed == 5
    assert backward.call_count == 2
    assert optim.call_count == 2
    assert backward.called
    assert optim.called


def test_train_fn_once():
    model, optimizer, device, loss_fn, batch = set_up()
    config = Namespace(use_amp=False)
    engine = Engine(lambda e, b: train_function(config, e, b, model, loss_fn, optimizer, device))
    engine.register_events(*TrainEvents, event_to_attr=train_events_to_attr)
    backward = MagicMock()
    optim = MagicMock()
    engine.add_event_handler(TrainEvents.BACKWARD_COMPLETED(once=3), backward)
    engine.add_event_handler(TrainEvents.OPTIM_STEP_COMPLETED(once=3), optim)
    engine.run([batch] * 5)
    assert hasattr(engine.state, "backward_completed")
    assert hasattr(engine.state, "optim_step_completed")
    assert engine.state.backward_completed == 5
    assert engine.state.optim_step_completed == 5
    assert backward.call_count == 1
    assert optim.call_count == 1
    assert backward.called
    assert optim.called


def test_evaluate_fn():
    model, optimizer, device, loss_fn, batch = set_up()
    engine = Engine(lambda e, b: 1)
    config = Namespace(use_amp=False)
    output = evaluate_function(config, engine, batch, model, loss_fn, device)
    assert isinstance(output, Number)


def test_create_trainers():
    model, optimizer, device, loss_fn, batch = set_up()
    trainer, evaluator = create_trainers(
        config=Namespace(use_amp=True),
        model=model,
        loss_fn=loss_fn,
        optimizer=optimizer,
        device=device,
    )
    assert isinstance(trainer, Engine)
    assert isinstance(evaluator, Engine)
    assert hasattr(trainer.state, "backward_completed")
    assert hasattr(trainer.state, "optim_step_completed")


def test_get_default_parser():
    parser = get_default_parser()
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
