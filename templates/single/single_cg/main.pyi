"""
main entrypoint training
"""
import logging
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import ignite.distributed as idist
from ignite.engine.events import Events
from ignite.utils import manual_seed

from single_cg.engines import create_engines
from single_cg.handlers import get_handlers, get_logger
from single_cg.utils import get_default_parser


def run(local_rank: int, config: Any, *args: Any, **kwargs: Any):
    """function to be run by idist.Parallel context manager."""

    # -----------------------------
    # datasets and dataloaders
    # -----------------------------
    # TODO : PLEASE provide your custom datasets and dataloaders configurations
    # we can use `idist.auto_dataloader` to handle distributed configurations
    # TODO : PLEASE replace `kwargs` with your desirable DataLoader arguments
    # See : https://pytorch.org/ignite/distributed.html#ignite.distributed.auto.auto_dataloader

    train_dataset = ...
    eval_dataset = ...
    train_dataloader = idist.auto_dataloader(train_dataset, **kwargs)
    eval_dataloader = idist.auto_dataloader(eval_dataset, **kwargs)

    # ------------------------------------------
    # model, optimizer, loss function, device
    # ------------------------------------------
    # we can use `idist.auto_model` to handle distributed configurations
    # for your model : https://pytorch.org/ignite/distributed.html#ignite.distributed.auto.auto_model
    # same also for optimizer, `idist.auto_optim` also handles distributed configurations
    # See : https://pytorch.org/ignite/distributed.html#ignite.distributed.auto.auto_model
    # TODO : PLEASE provide your custom model, optimizer, and loss function

    device = idist.device()
    model = ...
    optimizer = ...
    loss_fn = ...
    model = idist.auto_model(model=model, **kwargs)
    optimizer = idist.auto_optim(optimizer=optimizer)
    loss_fn = loss_fn.to(device)

    # -----------------------------
    # train_engine and eval_engine
    # -----------------------------

    train_engine, eval_engine = create_engines(
        config=config,
        model=model,
        optimizer=optimizer,
        loss_fn=loss_fn,
        device=device,
    )

    # -------------------------------------
    # ignite handlers and ignite loggers
    # -------------------------------------

    best_model_handler, es_handler, timer_handler = get_handlers()
    logger_handler = get_logger()

    # ---------------------------------------------
    # run evaluation at every training epoch end
    # ---------------------------------------------

    @train_engine.on(Events.EPOCH_COMPLETED(every=1))
    def _():
        # PLEASE provide `max_epochs` parameter
        eval_engine.run(eval_dataloader)

    # ------------------------------------------
    # setup if done. let's run the training
    # ------------------------------------------
    # TODO : PLEASE provide `max_epochs` parameters

    train_engine.run(train_dataloader)


def main():
    parser = ArgumentParser(parents=[get_default_parser()])
    config = parser.parse_args()
    manual_seed(config.seed)
    config.verbose = logging.INFO if config.verbose else logging.WARNING
    if config.filepath:
        path = Path(config.filepath)
        path.mkdir(parents=True, exist_ok=True)
        config.filepath = path
    if config.output_path:
        path = Path(config.output_path)
        path.mkdir(parents=True, exist_ok=True)
        config.output_path = path
    with idist.Parallel(
        backend=config.backend,
        nproc_per_node=config.nproc_per_node,
        nnodes=config.nnodes,
        node_rank=config.node_rank,
        master_addr=config.master_addr,
        master_port=config.master_port,
    ) as parallel:
        parallel.run(run, config=config)


if __name__ == "__main__":
    main()
