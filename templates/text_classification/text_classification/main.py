import os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

import ignite
import ignite.distributed as idist
from ignite.contrib.handlers import PiecewiseLinear
from ignite.engine import Events
from ignite.handlers import Checkpoint, global_step_from_engine
from ignite.metrics import Accuracy, Loss
from ignite.utils import manual_seed, setup_logger

from config import DEFAULTS
from dataset import get_dataflow
from models import get_model
from trainers import create_trainer, create_evaluator
from handlers import get_handlers, get_logger
from utils import thresholded_output_transform, get_save_handler, get_default_parser

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # remove tokenizer parallelism warning


def initialize(config):
    model = get_model(config.model, config.model_dir, config.dropout, config.n_fc, config.num_classes)

    config.learning_rate *= idist.get_world_size()
    # Adapt model for distributed settings if configured
    model = idist.auto_model(model)

    optimizer = optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=config.weight_decay)
    optimizer = idist.auto_optim(optimizer)
    criterion = nn.BCEWithLogitsLoss()

    le = config.num_iters_per_epoch
    milestones_values = [
        (0, 0.0),
        (le * config.num_warmup_epochs, config.learning_rate),
        (le * config.num_epochs, 0.0),
    ]
    lr_scheduler = PiecewiseLinear(optimizer, param_name="lr", milestones_values=milestones_values)

    return model, optimizer, criterion, lr_scheduler


def log_metrics(logger, epoch, elapsed, tag, metrics):
    metrics_output = "\n".join([f"\t{k}: {v}" for k, v in metrics.items()])
    logger.info(f"\nEpoch {epoch} - Evaluation time (seconds): {elapsed:.2f} - {tag} metrics:\n {metrics_output}")


def log_basic_info(logger, config):
    logger.info(f"Train {config.model} on IMDB")
    logger.info(f"- PyTorch version: {torch.__version__}")
    logger.info(f"- Ignite version: {ignite.__version__}")
    if torch.cuda.is_available():
        # explicitly import cudnn as
        # torch.backends.cudnn can not be pickled with hvd spawning procs
        from torch.backends import cudnn

        logger.info(f"- GPU Device: {torch.cuda.get_device_name(idist.get_local_rank())}")
        logger.info(f"- CUDA version: {torch.version.cuda}")
        logger.info(f"- CUDNN version: {cudnn.version()}")

    logger.info("\n")
    logger.info("Configuration:")
    for key, value in vars(config).items():
        logger.info(f"\t{key}: {value}")
    logger.info("\n")

    if idist.get_world_size() > 1:
        logger.info("\nDistributed setting:")
        logger.info(f"\tbackend: {idist.backend()}")
        logger.info(f"\tworld size: {idist.get_world_size()}")
        logger.info("\n")


def run(local_rank, config):

    rank = idist.get_rank()
    manual_seed(config.seed + rank)
    device = idist.device()

    logger = setup_logger(name="IMDB-Training", distributed_rank=local_rank)

    log_basic_info(logger, config)

    output_path = config.output_path
    if rank == 0:

        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        folder_name = f"{config.model}_backend-{idist.backend()}-{idist.get_world_size()}_{now}"
        output_path = Path(output_path) / folder_name
        if not output_path.exists():
            output_path.mkdir(parents=True)
        config.output_path = output_path.as_posix()
        logger.info(f"Output path: {config.output_path}")

        # if "cuda" in device.type:
        #     config["cuda device name"] = torch.cuda.get_device_name(local_rank)

        if config.with_clearml:
            try:
                from clearml import Task
            except ImportError:
                # Backwards-compatibility for legacy Trains SDK
                from trains import Task

            task = Task.init("IMDB-Training", task_name=output_path.stem)
            task.connect_configuration(config)
            # Log hyper parameters
            hyper_params = [
                "model",
                "dropout",
                "n_fc",
                "batch_size",
                "max_length",
                "weight_decay",
                "num_epochs",
                "learning_rate",
                "num_warmup_epochs",
            ]
            task.connect({k: getattr(config, k) for k in hyper_params})

    # Setup dataflow, model, optimizer, criterion
    train_loader, test_loader = get_dataflow(config)

    config.num_iters_per_epoch = len(train_loader)
    model, optimizer, criterion, lr_scheduler = initialize(config)

    # Create trainer for current task
    trainer = create_trainer(model, optimizer, criterion, lr_scheduler, train_loader.sampler, config, logger)

    # Let's now setup evaluator engine to perform model's validation and compute metrics
    metrics = {
        "Accuracy": Accuracy(output_transform=thresholded_output_transform),
        "Loss": Loss(criterion),
    }

    # We define two evaluators as they wont have exactly similar roles:
    # - `evaluator` will save the best model based on validation score
    evaluator = create_evaluator(model, metrics, config, tag="val")
    train_evaluator = create_evaluator(model, metrics, config, tag="train")

    def run_validation(engine):
        epoch = trainer.state.epoch
        state = train_evaluator.run(train_loader)
        log_metrics(logger, epoch, state.times["COMPLETED"], "Train", state.metrics)
        state = evaluator.run(test_loader)
        log_metrics(logger, epoch, state.times["COMPLETED"], "Test", state.metrics)

    trainer.add_event_handler(
        Events.EPOCH_COMPLETED(every=config.validate_every) | Events.COMPLETED | Events.STARTED, run_validation
    )

    if rank == 0:
        # Setup TensorBoard logging on trainer and evaluators. Logged values are:
        #  - Training metrics, e.g. running average loss values
        #  - Learning rate
        #  - Evaluation train/test metrics
        evaluators = {"training": train_evaluator, "test": evaluator}
        logger_handler = get_logger(
            config=config, train_engine=trainer, eval_engine=evaluators, optimizers=optimizer,
        )

    # Store 2 best models by validation accuracy starting from num_epochs / 2:
    best_model_handler = Checkpoint(
        {"model": model},
        get_save_handler(config),
        filename_prefix="best",
        n_saved=2,
        global_step_transform=global_step_from_engine(trainer),
        score_name="test_accuracy",
        score_function=Checkpoint.get_default_score_fn("Accuracy"),
    )
    evaluator.add_event_handler(
        Events.COMPLETED(lambda *_: trainer.state.epoch > config.num_epochs // 2), best_model_handler
    )

    try:
        trainer.run(train_loader, max_epochs=config.num_epochs)
    except Exception as e:
        logger.exception("")
        raise e

    if rank == 0:
        logger_handler.close()


def main():
    parser = ArgumentParser(parents=[get_default_parser(DEFAULTS)])
    config = parser.parse_args()
    manual_seed(config.seed)

    with idist.Parallel(
        backend=config.backend,
        nproc_per_node=config.nproc_per_node,
        nnodes=config.nnodes,
        node_rank=config.node_rank,
        master_addr=config.master_addr,
        master_port=config.master_port,
    ) as parallel:
        parallel.run(run, config)


if __name__ == "__main__":
    main()
