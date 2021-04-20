import sys

import streamlit as st

sys.path.append("./templates")

from _base._sidebar import (
    default_none_options,
    distributed_options,
    ignite_handlers_options,
    ignite_loggers_options,
    test_all_options,
)


def dataset_options(config):
    st.markdown("## Dataset Options")
    config["dataset"] = st.selectbox(
        "Dataset to use (dataset)",
        ["cifar10", "lsun", "imagenet", "folder", "lfw", "fake", "mnist"],
    )
    config["data_path"] = st.text_input("Dataset path (data_path)", "./")
    st.markdown("---")


def dataloader_options(config):
    st.markdown("## DataLoader Options")
    config["batch_size"] = st.number_input("Train batch size (batch_size)", min_value=1, value=16)
    config["num_workers"] = st.number_input("Number of workers (num_workers)", min_value=0, value=2)
    st.markdown("---")


def optimizer_options(config):
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
    config["max_epochs"] = st.number_input("Maximum epochs to train (max_epochs)", min_value=1, value=5)
    st.markdown("---")


def model_options(config):
    st.markdown("## Model Options")
    config["z_dim"] = st.number_input("Size of the latent z vector (z_dim)", value=100)
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

    config["saved_G"] = None
    config["saved_D"] = None
    default_none_options(config)

    with st.beta_expander("GAN Template Configurations", expanded=True):
        st.info("Names in the parenthesis are variable names used in the generated code.")

        # group by configurations type
        model_options(config)
        dataset_options(config)
        dataloader_options(config)
        optimizer_options(config)
        training_options(config)
        distributed_options(config)
        ignite_handlers_options(config)
        ignite_loggers_options(config)
        test_all_options(config)

    return config
