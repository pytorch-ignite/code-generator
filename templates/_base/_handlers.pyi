    from ignite.contrib.engines import common
    {% if setup_common_training_handlers %}
    common.setup_common_training_handlers(
        trainer=trainer,
        train_sampler=None,
        to_save=to_save,
        output_path=config.output_path,
        save_every_iters=config.save_every_iters,
        n_saved=config.n_saved,
        log_every_iters=config.log_every_iters,
        with_pbars=config.with_pbars,
        with_pbar_on_iters=config.with_pbar_on_iters,
        stop_on_nan=config.stop_on_nan,
        clear_cuda_cache=config.clear_cuda_cache,
        lr_scheduler=None,
        with_gpu_stats=False,
        output_names=None,
    )
    {% endif %}
    {% if logger == 'clearml' %}
    logger_handler = common.setup_clearml_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluators,
        log_every_iters=config.logger_log_every_iters,
    )
    {% elif logger == 'mlflow' %}
    logger_handler = common.setup_mlflow_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluators,
        log_every_iters=config.logger_log_every_iters,
    )
    {% elif logger == 'neptune-client' %}
    logger_handler = common.setup_neptune_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluators,
        log_every_iters=config.logger_log_every_iters,
    )
    {% elif logger == 'polyaxon' %}
    logger_handler = common.setup_polyaxon_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluators,
        log_every_iters=config.logger_log_every_iters,
    )
    {% elif logger == 'tensorboard' %}
    logger_handler = common.setup_tensorboard_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluators,
        log_every_iters=config.logger_log_every_iters,
    )
    {% elif logger == 'visdom' %}
    logger_handler = common.setup_visdom_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluators,
        log_every_iters=config.logger_log_every_iters,
    )
    {% elif logger == 'wandb' %}
    logger_handler = common.setup_wandb_logging(
        trainer=trainer,
        optimizers=optimizers,
        evaluators=evaluators,
        log_every_iters=config.logger_log_every_iters,
    )
    {% endif %}
