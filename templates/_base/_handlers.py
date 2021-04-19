"""
Ignite handlers
"""
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, Union

from ignite.contrib.engines import common
from ignite.contrib.handlers.base_logger import BaseLogger
from ignite.contrib.handlers.param_scheduler import LRScheduler
from ignite.engine.engine import Engine
from ignite.engine.events import Events
from ignite.handlers import Checkpoint, EarlyStopping, TimeLimit, Timer
from torch.nn import Module
from torch.optim.optimizer import Optimizer
from torch.utils.data.distributed import DistributedSampler


def get_handlers(
    config: Any,
    model: Module,
    trainer: Engine,
    evaluator: Engine,
    metric_name: str,
    es_metric_name: str,
    train_sampler: Optional[DistributedSampler] = None,
    to_save: Optional[Mapping] = None,
    lr_scheduler: Optional[LRScheduler] = None,
    output_names: Optional[Iterable[str]] = None,
    **kwargs: Any,
) -> Union[Tuple[Checkpoint, EarlyStopping, Timer], Tuple[None, None, None]]:
    """Get best model, earlystopping, timer handlers.

    Parameters
    ----------
    config
        Config object for setting up handlers

    `config` has to contain
    - `output_dir`: output path to indicate where to_save objects are stored
    - `save_every_iters`: saving iteration interval
    - `n_saved`: number of best models to store
    - `log_every_iters`: logging interval for iteration progress bar and `GpuInfo` if true
    - `with_pbars`: show two progress bars
    - `with_pbar_on_iters`: show iteration-wise progress bar
    - `stop_on_nan`: Stop the training if engine output contains NaN/inf values
    - `clear_cuda_cache`: clear cuda cache every end of epoch
    - `with_gpu_stats`: show GPU information: used memory percentage, gpu utilization percentage values
    - `patience`: number of events to wait if no improvement and then stop the training
    - `limit_sec`: maximum time before training terminates in seconds

    model
        best model to save
    trainer
        the engine used for training
    evaluator
        the engine used for evaluation
    metric_name
        evaluation metric to save the best model
    es_metric_name
        evaluation metric to early stop the model
    train_sampler
        distributed training sampler to call `set_epoch`
    to_save
        objects to save during training
    lr_scheduler
        learning rate scheduler as native torch LRScheduler or ignite’s parameter scheduler
    output_names
        list of names associated with `trainer`'s process_function output dictionary
    kwargs
        keyword arguments passed to Checkpoint handler

    Returns
    -------
    best_model_handler, es_handler, timer_handler
    """

    best_model_handler, es_handler, timer_handler = None, None, None

    # https://pytorch.org/ignite/contrib/engines.html#ignite.contrib.engines.common.setup_common_training_handlers
    # kwargs can be passed to save the model based on training stats
    # like score_name, score_function
    common.setup_common_training_handlers(
        trainer=trainer,
        train_sampler=train_sampler,
        to_save=to_save,
        lr_scheduler=lr_scheduler,
        output_names=output_names,
        output_path=config.output_dir / 'checkpoints',
        save_every_iters=config.save_every_iters,
        n_saved=config.n_saved,
        log_every_iters=config.log_every_iters,
        with_pbars=config.with_pbars,
        with_pbar_on_iters=config.with_pbar_on_iters,
        stop_on_nan=config.stop_on_nan,
        clear_cuda_cache=config.clear_cuda_cache,
        with_gpu_stats=config.with_gpu_stats,
        **kwargs,
    )
    {% if save_best_model_by_val_score %}

    # https://pytorch.org/ignite/contrib/engines.html#ignite.contrib.engines.common.save_best_model_by_val_score
    best_model_handler = common.save_best_model_by_val_score(
        output_path=config.output_dir / 'checkpoints',
        evaluator=evaluator,
        model=model,
        metric_name=metric_name,
        n_saved=config.n_saved,
        trainer=trainer,
        tag='eval',
    )
    {% endif %}
    {% if add_early_stopping_by_val_score %}

    # https://pytorch.org/ignite/contrib/engines.html#ignite.contrib.engines.common.add_early_stopping_by_val_score
    es_handler = common.add_early_stopping_by_val_score(
        patience=config.patience,
        evaluator=evaluator,
        trainer=trainer,
        metric_name=es_metric_name,
    )
    {% endif %}
    {% if setup_timer %}

    # https://pytorch.org/ignite/handlers.html#ignite.handlers.Timer
    # measure the average time to process a single batch of samples
    # Events for that are - ITERATION_STARTED and ITERATION_COMPLETED
    # you can replace with the events you want to measure
    timer_handler = Timer(average=True)
    timer_handler.attach(
        engine=trainer,
        start=Events.EPOCH_STARTED,
        resume=Events.ITERATION_STARTED,
        pause=Events.ITERATION_COMPLETED,
        step=Events.ITERATION_COMPLETED,
    )
    {% endif %}
    {% if setup_timelimit %}

    # training will terminate if training time exceed `limit_sec`.
    trainer.add_event_handler(
        Events.ITERATION_COMPLETED, TimeLimit(limit_sec=config.limit_sec)
    )
    {% endif %}
    return best_model_handler, es_handler, timer_handler


def get_logger(
    config: Any,
    trainer: Engine,
    evaluator: Optional[Union[Engine, Dict[str, Engine]]] = None,
    optimizers: Optional[Union[Optimizer, Dict[str, Optimizer]]] = None,
    **kwargs: Any,
) -> Optional[BaseLogger]:
    """Get Ignite provided logger.

    Parameters
    ----------
    config
        Config object for setting up loggers

    `config` has to contain
    - `filepath`: logging path to output file
    - `logger_log_every_iters`: logging iteration interval for loggers

    trainer
        trainer engine
    evaluator
        evaluator engine
    optimizers
        optimizers to log optimizer parameters
    kwargs
        optional keyword arguments passed to the logger

    Returns
    -------
    logger_handler
        Ignite provided logger instance
    """

    {% if logger_deps == 'clearml' %}
    logger_handler = common.setup_clearml_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    {% elif logger_deps == 'mlflow' %}
    logger_handler = common.setup_mlflow_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    {% elif logger_deps == 'neptune-client' %}
    logger_handler = common.setup_neptune_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    {% elif logger_deps == 'polyaxon-client' %}
    logger_handler = common.setup_plx_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    {% elif logger_deps == 'tensorboard' %}
    logger_handler = common.setup_tb_logging(
        output_path=config.output_dir,
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    {% elif logger_deps == 'visdom' %}
    logger_handler = common.setup_visdom_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    {% elif logger_deps == 'wandb' %}
    logger_handler = common.setup_wandb_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluator,
        log_every_iters=config.logger_log_every_iters,
        **kwargs,
    )
    {% else %}
    logger_handler = None
    {% endif %}
    return logger_handler
