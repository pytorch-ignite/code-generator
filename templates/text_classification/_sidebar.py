import sys

import streamlit as st

sys.path.append("./templates")

from _base._sidebar import (
    default_none_options,
    distributed_options,
    ignite_handlers_options,
    ignite_loggers_options,
)


def get_configs() -> dict:
    config = {}
    config["train_epoch_length"] = None
    config["eval_epoch_length"] = None
    default_none_options(config)

    st.header("Transformer")

    st.subheader("Model Options")
    config["model"] = st.selectbox(
        "Model name (from transformers) to setup model, tokenize and config to train (model)",
        options=["bert-base-uncased"],
    )
    config["model_dir"] = st.text_input("Cache directory to download the pretrained model (model_dir)", value="./")
    config["tokenizer_dir"] = st.text_input("Tokenizer cache directory (tokenizer_dir)", value="./tokenizer")
    config["num_classes"] = st.number_input(
        "Number of target classes. Default, 1 (binary classification) (num_classes)", min_value=0, value=1
    )
    config["max_length"] = st.number_input(
        "Maximum number of tokens for the inputs to the transformer model (max_length)", min_value=1, value=256
    )
    config["dropout"] = st.number_input(
        "Dropout probability (dropout)", min_value=0.0, max_value=1.0, value=0.3, format="%f"
    )
    config["n_fc"] = st.number_input(
        "Number of neurons in the last fully connected layer (n_fc)", min_value=1, value=768
    )
    st.markdown("---")

    st.subheader("Dataset Options")
    config["data_dir"] = st.text_input("Dataset cache directory (data_dir)", value="./")
    st.markdown("---")

    st.subheader("DataLoader Options")
    config["batch_size"] = st.number_input("Total batch size (batch_size)", min_value=1, value=16)
    config["num_workers"] = st.number_input("Number of workers in the data loader (num_workers)", min_value=1, value=2)
    st.markdown("---")

    st.subheader("Optimizer Options")
    config["learning_rate"] = st.number_input(
        "Peak of piecewise linear learning rate scheduler", min_value=0.0, value=5e-5, format="%e"
    )
    config["weight_decay"] = st.number_input("Weight decay", min_value=0.0, value=0.01, format="%f")
    st.markdown("---")

    st.subheader("Training Options")
    config["max_epochs"] = st.number_input("Number of epochs to train the model", min_value=1, value=3)
    config["num_warmup_epochs"] = st.number_input(
        "Number of warm-up epochs before learning rate decay", min_value=0, value=0
    )
    config["validate_every"] = st.number_input(
        "Run model's validation every validate_every epochs", min_value=0, value=1
    )
    config["checkpoint_every"] = st.number_input(
        "Store training checkpoint every checkpoint_every iterations", min_value=0, value=1000
    )
    config["log_every_iters"] = st.number_input(
        "Argument to log batch loss every log_every_iters iterations. 0 to disable it", min_value=0, value=15
    )
    st.markdown("---")

    distributed_options(config)
    ignite_handlers_options(config)
    ignite_loggers_options(config)

    return config
