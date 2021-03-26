import streamlit as st


def dataset_options(config):
    st.markdown("## Dataset Options")
    config["dataset"] = st.selectbox(
        "Dataset to use (dataset)",
        ["cifar10", "lsun", "imagenet", "folder", "lfw", "fake", "mnist"],
    )
    config["data_path"] = st.text_input("Dataset path (data_path)", "./")

    config["filepath"] = st.text_input("Logging file path (filepath)", "./logs")
    st.markdown("---")


def dataloader_options(config):
    st.markdown("## DataLoader Options")
    config["batch_size"] = st.number_input("Train batch size (batch_size)", min_value=1, value=4)
    config["num_workers"] = st.number_input("Number of workers (num_workers)", min_value=0, value=2)
    st.markdown("---")

    st.markdown("## Optimizer Options")
    config["beta_1"] = st.number_input("beta_1 for Adam optimizer (beta_1)", value=0.5)
    config["lr"] = st.number_input(
        "Learning rate used by torch.optim.* (lr)",
        min_value=0.0,
        value=1e-3,
        format="%e",
    )
    st.markdown("---")


def training_options(config):
    st.markdown("## Training Options")
    config["max_epochs"] = st.number_input("Maximum epochs to train (max_epochs)", min_value=1, value=2)
    config["log_train"] = st.number_input("Logging interval of training iterations (log_train)", min_value=0, value=50)
    config["seed"] = st.number_input("Seed used in ignite.utils.manual_seed() (seed)", min_value=0, value=666)
    st.markdown("---")


def distributed_options(config):
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
    config["output_path"] = st.text_input(
        "Output path to indicate where to_save objects are stored (output_path)",
        value="./logs",
    )
    config["save_every_iters"] = st.number_input(
        "Saving iteration interval (save_every_iters)", min_value=1, value=1000
    )
    config["n_saved"] = st.number_input("Number of best models to store (n_saved)", min_value=1, value=2)
    config["log_every_iters"] = st.number_input(
        "Logging interval for iteration progress bar",
        min_value=1,
        value=100,
        help="Setting to a lower value can cause tqdm" " to fluch quickly for fast trainings",
    )
    config["with_pbars"] = st.checkbox(
        "Show two progress bars",
        value=True,
        help=(
            "This option will enable two progress bars - one for epoch,"
            " one for iteration if `with_pbar_on_iters` is `False`,"
            " only epoch-wise progress bar will be enabled."
        ),
    )
    config["with_pbar_on_iters"] = st.checkbox(
        "Show iteration-wise progress bar",
        value=True,
        help="This option has no effect if `with_pbars` is `False`",
    )
    config["stop_on_nan"] = st.checkbox("Stop the training if engine output contains NaN/inf values", value=True)
    config["clear_cuda_cache"] = st.checkbox(
        "Clear cuda cache every end of epoch",
        value=True,
        help="This is calling `torch.cuda.empty_cache()` every end of epoch",
    )
    st.markdown("---")
    config["setup_common_training_handlers"] = True


def model_options(config):
    st.markdown("## Model Options")
    config["z_dim"] = st.number_input("Size of the latent z vector (z_dim)", value=100)
    config["alpha"] = st.number_input("Running average decay factor (alpha)", value=0.98)
    config["g_filters"] = st.number_input(
        "Number of filters in the second-to-last generator deconv layer (g_filters)",
        value=64,
    )
    config["d_filters"] = st.number_input("Number of filters in first discriminator conv layer (d_filters)", value=64)
    st.markdown("---")


def get_configs() -> dict:
    config = {}
    config["train_epoch_length"] = None
    config["eval_epoch_length"] = None

    # distributed configs
    config["nproc_per_node"] = None
    config["nnodes"] = None
    config["node_rank"] = None
    config["master_addr"] = None
    config["master_port"] = None
    config["saved_G"] = None
    config["saved_D"] = None

    with st.beta_expander("GAN Template Configurations", expanded=True):
        st.info("Those in the parenthesis are used in the generated code.")

        # group by configurations type
        dataset_options(config)
        dataloader_options(config)
        training_options(config)
        distributed_options(config)
        ignite_handlers_options(config)
        model_options(config)

    return config
