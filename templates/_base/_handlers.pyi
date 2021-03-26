    from ignite.contrib.engines import common
    {% if setup_common_training_handlers %}
    common.setup_common_training_handlers(
        trainer=train_engine,
        train_sampler=None,
        to_save=to_save,
        output_path={{ output_path }},
        save_every_iters={{ save_every_iters }},
        n_saved={{ n_saved }},
        log_every_iters={{ log_every_iters }},
        with_pbars={{ with_pbars }},
        with_pbar_on_iters={{ with_pbar_on_iters }},
        stop_on_nan={{ stop_on_nan }},
        clear_cuda_cache={{ clear_cuda_cache }},
        lr_scheduler=None,
        with_gpu_stats=False,
        output_names=None,
    )
    {% endif %}
