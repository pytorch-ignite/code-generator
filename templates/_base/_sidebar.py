import streamlit as st


def distributed_options(config):
    # distributed configs
    config["nproc_per_node"] = None
    config["nnodes"] = None
    config["node_rank"] = None
    config["master_addr"] = None
    config["master_port"] = None

    st.markdown("## Distributed Training Options")
    if st.checkbox("Use distributed training"):
        config["nproc_per_node"] = st.number_input(
            "Number of processes to launch on each node (nproc_per_node)", min_value=1
        )
        config["nnodes"] = st.number_input("Number of nodes to use for distributed training (nnodes)", min_value=1)
        if config["nnodes"] > 1:
            st.info(
                "The following options are only supported by torch.distributed,"
                " namely 'gloo' and 'nccl' backends. For other backends,"
                " please specify spawn_kwargs in main.py"
            )
            config["node_rank"] = st.number_input(
                "Rank of the node for multi-node distributed training (node_rank)",
                min_value=0,
            )
            if config["node_rank"] > (config["nnodes"] - 1):
                st.error(f"node_rank should be between 0 and {config['nnodes'] - 1}")
            config["master_addr"] = st.text_input(
                "Master node TCP/IP address for torch native backends (master_addr)",
                value="'127.0.0.1'",
            )
            st.warning("Please include single quote in master_addr.")
            config["master_port"] = st.text_input(
                "Master node port for torch native backends (master_port)", value=8080
            )
    st.markdown("---")


def ignite_handlers_options(config):
    st.markdown("## Ignite Handlers Options")

    _setup_common_training_handlers_options(config)
    _save_best_model_by_val_score_options(config)
    _add_early_stopping_by_val_score_options(config)

    config["setup_timer"] = st.checkbox("Use Timer handler", value=False)
    st.markdown("---")

    config["setup_timelimit"] = st.checkbox("Use TimeLimit handler", value=False)
    if config["setup_timelimit"]:
        config["limit_sec"] = st.number_input(
            "Maximum time before training terminates in seconds. (limit_sec)", min_value=1, value=28800
        )
    st.markdown("---")

    if config["with_pbars"]:
        config["handler_deps"] = "tqdm"
    if config["with_gpu_stats"]:
        config["handler_deps"] += "\npynvml"


def ignite_loggers_options(config):
    st.markdown("## Ignite Loggers Options")
    config["filepath"] = st.text_input(
        "Logging file path (filepath)",
        "./logs",
        help="This option will be used by both python logging and ignite loggers if possible",
    )
    if st.checkbox("Use experiment tracking system ?", value=True):
        config["logger_deps"] = st.selectbox(
            "Select experiment eracking system",
            ["ClearML", "MLflow", "Neptune", "Polyaxon", "TensorBoard", "Visdom", "WandB"],
            index=4,
        ).lower()
        # for logger requirement
        if config["logger_deps"] in ("neptune", "polyaxon"):
            config["logger_deps"] += "-client"
        config["logger_log_every_iters"] = st.number_input(
            "Logging interval for experiment tracking system (logger_log_every_iters)",
            min_value=1,
            value=100,
            help="This logging interval is iteration based.",
        )
    st.markdown("---")


def _setup_common_training_handlers_options(config):
    config["output_path"] = st.text_input(
        "Output path to indicate where to_save objects are stored (output_path)",
        value="./logs",
    )
    config["save_every_iters"] = st.number_input(
        "Saving iteration interval (save_every_iters)", min_value=1, value=1000
    )
    config["n_saved"] = st.number_input("Number of best models to store (n_saved)", min_value=1, value=2)
    config["log_every_iters"] = st.number_input(
        "Logging interval for iteration progress bar and GpuInfo if true (log_every_iters)",
        min_value=1,
        value=100,
        help="Setting to a lower value can cause `tqdm` to fluch quickly for fast trainings",
    )
    config["with_pbars"] = st.checkbox(
        "Show two progress bars (with_pbars)",
        value=True,
        help=(
            "This option will enable two progress bars - one for epoch,"
            " one for iteration if `with_pbar_on_iters` is `False`,"
            " only epoch-wise progress bar will be enabled."
        ),
    )
    config["with_pbar_on_iters"] = st.checkbox(
        "Show iteration-wise progress bar (with_pbar_on_iters)",
        value=True,
        help="This option has no effect if `with_pbars` is `False`",
    )
    config["stop_on_nan"] = st.checkbox(
        "Stop the training if engine output contains NaN/inf values (stop_on_nan)", value=True
    )
    config["clear_cuda_cache"] = st.checkbox(
        "Clear cuda cache every end of epoch (clear_cuda_cache)",
        value=True,
        help="This is calling `torch.cuda.empty_cache()` every end of epoch",
    )
    config["with_gpu_stats"] = st.checkbox(
        "Show GPU information: used memory percentage, gpu utilization percentage values (with_gpu_stats)",
        value=False,
        help="This option attaches `GpuInfo` metric to the trainer. This requires `pynvml` package to be installed.",
    )
    st.markdown("---")


def _save_best_model_by_val_score_options(config):
    config["save_best_model_by_val_score"] = st.checkbox(
        "Save the best model by evaluation score",
        value=False,
    )
    if config["save_best_model_by_val_score"]:
        config["metric_name"] = st.text_input(
            "Metric name associated with eval_engine",
            key="ckpt_metric_name",
        )
        if not config["metric_name"]:
            st.error(":warning: Please input the evaluation metric name that will be used :warning:")
        st.warning(
            "Please make sure `eval_engine.state.metrics` has above provided metric name."
            " Otherwise it can result `KeyError`."
        )
    st.markdown("---")


def _add_early_stopping_by_val_score_options(config):
    config["add_early_stopping_by_val_score"] = st.checkbox(
        "Early stop the training by evaluation score",
        value=False,
    )
    if config["add_early_stopping_by_val_score"]:
        config["patience"] = st.number_input(
            "Number of events to wait if no improvement and then stop the training. (patience)",
            min_value=1,
            value=3,
        )
        config["es_metric_name"] = st.text_input(
            "Metric name associated with eval_engine",
            key="es_metric_name",
            help="This input `metric_name` can either be same as above or not."
            if config["save_best_model_by_val_score"]
            else None,
        )
        if not config["es_metric_name"]:
            st.error(":warning: Please input the evaluation metric name that will be used :warning:")
        st.warning(
            "Please make sure `eval_engine.state.metrics` has above provided metric name."
            " Otherwise it can result `KeyError`."
        )
    st.markdown("---")
