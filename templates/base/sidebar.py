from argparse import Namespace

import streamlit as st

params = {
    "data_path": {
        "app": {"value": "./"},
        "test": {"prefix": "tmp", "suffix": ""},
    },
    "filepath": {
        "app": {"value": "./logs"},
        "test": {"prefix": "tmp", "suffix": ""},
    },
    "train_batch_size": {
        "app": {"min_value": 1, "value": 4},
        "test": {"min_value": 1, "max_value": 2},
    },
    "eval_batch_size": {
        "app": {"min_value": 1, "value": 4},
        "test": {"min_value": 1, "max_value": 2},
    },
    "num_workers": {
        "app": {"min_value": 0, "value": 2},
        "test": {"min_value": 1, "max_value": 2},
    },
    "train_max_epochs": {
        "app": {"min_value": 1, "value": 2},
        "test": {"min_value": 1, "max_value": 2},
    },
    "eval_max_epochs": {
        "app": {"min_value": 1, "value": 2},
        "test": {"min_value": 1, "max_value": 2},
    },
    "train_epoch_length": None,
    "eval_epoch_length": None,
    "lr": {
        "app": {"min_value": 0.0, "value": 0.001, "format": "%e"},
        "test": {"min_value": 0.0, "max_value": 1},
    },
    "log_train": {
        "app": {"min_value": 0, "value": 50},
        "test": {"min_value": 1, "max_value": 10},
    },
    "log_eval": {
        "app": {"min_value": 0, "value": 1},
        "test": {"min_value": 1, "max_value": 10},
    },
    "seed": {
        "app": {"min_value": 0, "value": 666},
        "test": {"min_value": 0, "max_value": 1000},
    },
    # Distributed training part
    # {min_value: 1} if distributed training is on else None
    "nproc_per_node": {
        "app": {"nondist_train": None, "dist_train": {"min_value": 1}},
        "test": {"nondist_train": None, "dist_train": {"min_value": 1, "max_value": 2}},
    },
    # {min_value: 1} if distributed training is on else None
    "nnodes": {
        "app": {"nondist_train": None, "dist_train": {"min_value": 1}},
        "test": {"nondist_train": None, "dist_train": {"min_value": 1, "max_value": 2}},
    },
    # {min_value: 0} if nnodes > 1 else None
    "node_rank": {
        "app": {"singlenode": None, "multinode": {"min_value": 0}},
        "test": {"singlenode": None, "multinode": {"min_value": 0, "max_value": 2}},
    },
    # '127.0.0.1' if nnodes > 1 else None
    "master_addr": {
        "app": {"singlenode": None, "multinode": "'127.0.0.1'"},
        "test": {"singlenode": None, "multinode": "'127.0.0.1'"},
    },
    # "8080" if nnodes > 1 else None
    "master_port": {
        "app": {"singlenode": None, "multinode": "8080"},
        "test": {"singlenode": None, "multinode": "8080"},
    },
}
params = Namespace(**{k: Namespace(**v) if isinstance(v, dict) else v for k, v in params.items()})


def get_configs() -> dict:
    config = {}
    config["train_epoch_length"] = params.train_epoch_length
    config["eval_epoch_length"] = params.eval_epoch_length

    with st.beta_expander("Training Configurations"):
        st.info("Common base training configurations. Those in the parenthesis are used in the code.")

        # group by streamlit function type
        config["data_path"] = st.text_input("Dataset path (data_path)", **params.data_path.app)
        config["filepath"] = st.text_input("Logging file path (filepath)", **params.filepath.app)

        config["train_batch_size"] = st.number_input(
            "Train batch size (train_batch_size)", **params.train_batch_size.app
        )
        config["eval_batch_size"] = st.number_input("Eval batch size (eval_batch_size)", **params.eval_batch_size.app)
        config["num_workers"] = st.number_input("Number of workers (num_workers)", **params.num_workers.app)

        config["lr"] = st.number_input("Learning rate used by torch.optim.* (lr)", **params.lr.app)
        config["log_train"] = st.number_input(
            "Logging interval of training iterations (log_train)", **params.log_train.app
        )
        config["log_eval"] = st.number_input("Logging interval of evaluation epoch (log_eval)", **params.log_eval.app)
        config["seed"] = st.number_input("Seed used in ignite.utils.manual_seed() (seed)", **params.seed.app)

        config["train_max_epochs"] = st.number_input(
            "Maximum epochs to train (train_max_epochs)", **params.train_max_epochs.app
        )
        config["eval_max_epochs"] = st.number_input(
            "Maximum epochs to eval (eval_max_epochs)", **params.eval_max_epochs.app
        )

        # Plain training, use None
        config["nproc_per_node"] = params.nproc_per_node.app["nondist_train"]
        config["nnodes"] = params.nnodes.app["nondist_train"]
        config["node_rank"] = params.node_rank.app["singlenode"]
        config["master_addr"] = params.master_addr.app["singlenode"]
        config["master_port"] = params.master_port.app["singlenode"]

        # Distributed training config
        if st.checkbox("Use distributed training"):
            config["nproc_per_node"] = st.number_input(
                "Number of processes to launch on each node (nproc_per_node)", **params.nproc_per_node.app["dist_train"]
            )
            config["nnodes"] = st.number_input(
                "Number of nodes to use for distributed training (nnodes)", **params.nnodes.app["dist_train"]
            )
            if config["nnodes"] > 1:
                st.info(
                    "The following options are only supported by torch.distributed, namely 'gloo' and 'nccl' backends."
                    " For other backends, please specify spawn_kwargs in main.py"
                )
                config["node_rank"] = st.number_input(
                    "Rank of the node for multi-node distributed training (node_rank)",
                    **params.node_rank.app["multinode"],
                )
                if config["node_rank"] > (config["nnodes"] - 1):
                    st.error(f"node_rank should be between 0 and {config['nnodes'] - 1}")
                config["master_addr"] = st.text_input(
                    "Master node TCP/IP address for torch native backends (master_addr)",
                    params.master_addr.app["multinode"],
                )
                st.warning("Please include single quote in master_addr.")
                config["master_port"] = st.text_input(
                    "Master node port for torch native backends (master_port)", params.master_port.app["multinode"]
                )

    return config
