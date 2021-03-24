from argparse import Namespace

import streamlit as st

params = {
    "data_path": {"value": "./"},
    "filepath": {"value": "./logs"},
    "train_batch_size": {"min_value": 1, "value": 4},
    "eval_batch_size": {"min_value": 1, "value": 4},
    "num_workers": {"min_value": 0, "value": 2},
    "train_max_epochs": {"min_value": 1, "value": 2},
    "eval_max_epochs": {"min_value": 1, "value": 2},
    "lr": {"min_value": 0.0, "value": 0.001, "format": "%e"},
    "log_train": {"min_value": 0, "value": 50},
    "log_eval": {"min_value": 0, "value": 1},
    "seed": {"min_value": 0, "value": 666},
    # Distributed training part
    # {min_value: 1} if distributed training is on else None
    "nproc_per_node": {"nondist_train": None, "dist_train": {"min_value": 1}},
    # {min_value: 1} if distributed training is on else None
    "nnodes": {"nondist_train": None, "dist_train": {"min_value": 1}},
    # {min_value: 0} if nnodes > 1 else None
    "node_rank": {"singlenode": None, "multinode": {"min_value": 0}},
    # '127.0.0.1' if nnodes > 1 else None
    "master_addr": {"singlenode": None, "multinode": "'127.0.0.1'"},
    # "8080" if nnodes > 1 else None
    "master_port": {"singlenode": None, "multinode": "8080"},
    "model_name": [
        "alexnet",
        "resnet18",
        "vgg16",
        "squeezenet1_0",
        "inception_v3",
        "densenet161",
        "googlenet",
        "mobilenet_v2",
        "mobilenet_v3_small",
        "resnext50_32x4d",
        "shufflenet_v2_x1_0",
    ],
    "exp_logging": [
        None,
        "wandb",
    ],
}

params = Namespace(**{k: v for k, v in params.items()})


def get_configs() -> dict:
    config = {}
    config["train_epoch_length"] = None
    config["eval_epoch_length"] = None

    # Plain training, use None
    config["nproc_per_node"] = params.nproc_per_node["nondist_train"]
    config["nnodes"] = params.nnodes["nondist_train"]
    config["node_rank"] = params.node_rank["singlenode"]
    config["master_addr"] = params.master_addr["singlenode"]
    config["master_port"] = params.master_port["singlenode"]

    with st.beta_expander("Image Classification Template Configurations", expanded=True):
        st.info("Those in the parenthesis are used in the generated code.")

        # group by configurations type

        st.markdown("## Dataset Options")
        config["data_path"] = st.text_input("Dataset path (data_path)", **params.data_path)
        config["filepath"] = st.text_input("Logging file path (filepath)", **params.filepath)
        st.markdown("---")

        st.markdown("## DataLoader Options")
        config["train_batch_size"] = st.number_input("Train batch size (train_batch_size)", **params.train_batch_size)
        config["eval_batch_size"] = st.number_input("Eval batch size (eval_batch_size)", **params.eval_batch_size)
        config["num_workers"] = st.number_input("Number of workers (num_workers)", **params.num_workers)
        st.markdown("---")

        st.markdown("## Optimizer Options")
        config["lr"] = st.number_input("Learning rate used by torch.optim.* (lr)", **params.lr)
        st.markdown("---")

        st.markdown("## Training Options")
        config["log_train"] = st.number_input("Logging interval of training iterations (log_train)", **params.log_train)
        config["log_eval"] = st.number_input("Logging interval of evaluation epoch (log_eval)", **params.log_eval)
        config["seed"] = st.number_input("Seed used in ignite.utils.manual_seed() (seed)", **params.seed)

        config["train_max_epochs"] = st.number_input(
            "Maximum epochs to train (train_max_epochs)", **params.train_max_epochs
        )
        config["eval_max_epochs"] = st.number_input(
            "Maximum epochs to eval (eval_max_epochs)", **params.eval_max_epochs
        )
        st.markdown("---")

        st.markdown("## Distributed Training Options")
        if st.checkbox("Use distributed training"):
            config["nproc_per_node"] = st.number_input(
                "Number of processes to launch on each node (nproc_per_node)", **params.nproc_per_node["dist_train"]
            )
            config["nnodes"] = st.number_input(
                "Number of nodes to use for distributed training (nnodes)", **params.nnodes["dist_train"]
            )
            if config["nnodes"] > 1:
                st.info(
                    "The following options are only supported by torch.distributed, namely 'gloo' and 'nccl' backends."
                    " For other backends, please specify spawn_kwargs in main.py"
                )
                config["node_rank"] = st.number_input(
                    "Rank of the node for multi-node distributed training (node_rank)",
                    **params.node_rank["multinode"],
                )
                if config["node_rank"] > (config["nnodes"] - 1):
                    st.error(f"node_rank should be between 0 and {config['nnodes'] - 1}")
                config["master_addr"] = st.text_input(
                    "Master node TCP/IP address for torch native backends (master_addr)",
                    params.master_addr["multinode"],
                )
                st.warning("Please include single quote in master_addr.")
                config["master_port"] = st.text_input(
                    "Master node port for torch native backends (master_port)", params.master_port["multinode"]
                )
        st.markdown("---")

        st.markdown("## Ignite Handlers Options")
        config["exp_logging"] = st.selectbox("Experiment tracking (exp_logging)", params.exp_logging)
        if config["exp_logging"] is not None:
            config["project_name"] = st.text_input(
                "Project name of experiment tracking system (project_name)", "code-generator"
            )
        config["n_saved"] = st.number_input("Number of best models to store (n_saved)", min_value=1, value=2)
        config["save_every_iters"] = st.number_input(
            "Model saving interval (save_every_iters)", min_value=10, value=1000
        )
        st.markdown("---")

        st.markdown("## Model Options")
        config["model_name"] = st.selectbox("Model name (model_name)", params.model_name, 1)
        st.markdown("---")

    return config
