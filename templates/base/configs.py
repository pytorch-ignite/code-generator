import streamlit as st


def get_configs() -> dict:
    config = {}
    with st.beta_expander("Training Configurations"):
        config["amp_mode"] = st.selectbox("AMP mode", ("amp", "apex"))
        config["train_batch_size"] = st.number_input(
            "Train batch size", min_value=1, value=1
        )
        config["eval_batch_size"] = st.number_input(
            "Eval batch size", min_value=1, value=1
        )
        config["data_path"] = st.text_input("Dataset path", value="./")
        config["device"] = st.selectbox("Device to use", ("cpu", "cuda", "xla"))
        config["filepath"] = st.text_input("Logging file path", value="./logs")
        config["num_workers"] = st.number_input(
            "Number of workers", min_value=0, value=2
        )
        config["max_epochs"] = st.number_input(
            "Maximum epochs to train", min_value=1, value=2
        )
        config["lr"] = st.number_input(
            "Learning rate used by torch.optim.*",
            min_value=0.0,
            value=1e-3,
            format="%e",
        )
        config["log_train"] = st.number_input(
            "Logging interval of training iterations", min_value=0, value=50
        )
        config["log_eval"] = st.number_input(
            "Logging interval of evaluation epoch", min_value=0, value=1
        )
        config["seed"] = st.number_input(
            "Seed used in ignite.utils.manual_seed()", min_value=0, value=666
        )
        config["backend"] = st.selectbox(
            "Backend to use", ("gloo", "nccl", "mpi", "xla-tpu", "horovod")
        )
        config["nproc_per_node"] = st.number_input(
            "Number of processes to launch on each node", min_value=0, value=0
        )
        config["nnodes"] = st.number_input(
            "Number of nodes to use for distributed training", min_value=0, value=0
        )
        config["node_rank"] = st.number_input(
            "Rank of the node for multi-node distributed training", min_value=0, value=0
        )

    return config
