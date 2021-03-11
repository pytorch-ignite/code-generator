import streamlit as st


def get_configs() -> dict:
    config = {}
    with st.beta_expander("Training Configurations"):
        st.info("Common base training configurations. Those in the parenthesis are used in the code.")

        # group by streamlit function type
        config["amp_mode"] = st.selectbox("AMP mode (amp_mode)", ("None", "amp", "apex"))
        config["device"] = st.selectbox("Device to use (device)", ("cpu", "cuda", "xla"))

        config["data_path"] = st.text_input("Dataset path (data_path)", value="./")
        config["filepath"] = st.text_input("Logging file path (filepath)", value="./logs")

        config["train_batch_size"] = st.number_input("Train batch size (train_batch_size)", min_value=1, value=1)
        config["eval_batch_size"] = st.number_input("Eval batch size (eval_batch_size)", min_value=1, value=1)
        config["num_workers"] = st.number_input("Number of workers (num_workers)", min_value=0, value=2)
        config["max_epochs"] = st.number_input("Maximum epochs to train (max_epochs)", min_value=1, value=2)
        config["lr"] = st.number_input(
            "Learning rate used by torch.optim.* (lr)", min_value=0.0, value=1e-3, format="%e",
        )
        config["log_train"] = st.number_input(
            "Logging interval of training iterations (log_train)", min_value=0, value=50
        )
        config["log_eval"] = st.number_input("Logging interval of evaluation epoch (log_eval)", min_value=0, value=1)
        config["seed"] = st.number_input("Seed used in ignite.utils.manual_seed() (seed)", min_value=0, value=666)
        if st.checkbox("Use distributed training"):
            config["nproc_per_node"] = st.number_input(
                "Number of processes to launch on each node (nproc_per_node)", min_value=1,
            )
            config["nnodes"] = st.number_input("Number of nodes to use for distributed training (nnodes)", min_value=1,)
            if config["nnodes"] > 1:
                st.info(
                    "The following options are only supported by torch.distributed, namely 'gloo' and 'nccl' backends."
                    " For other backends, please specify spawn_kwargs in main.py"
                )
                config["node_rank"] = st.number_input(
                    "Rank of the node for multi-node distributed training (node_rank)", min_value=0,
                )
                if config["node_rank"] > (config["nnodes"] - 1):
                    st.error(f"node_rank should be between 0 and {config['nnodes'] - 1}")
                config["master_addr"] = st.text_input(
                    "Master node TCP/IP address for torch native backends (master_addr)", "'127.0.0.1'",
                )
                st.warning("Please include single quote in master_addr.")
                config["master_port"] = st.text_input(
                    "Master node port for torch native backends (master_port)", "8080"
                )
            else:
                config["node_rank"] = None
                config["master_addr"] = None
                config["master_port"] = None
        else:
            config["nproc_per_node"] = None
            config["nnodes"] = None
            config["node_rank"] = None
            config["master_addr"] = None
            config["master_port"] = None

    return config
