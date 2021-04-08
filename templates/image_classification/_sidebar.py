import sys

import streamlit as st

sys.path.append("./templates")

from _base._sidebar import (
    default_none_options,
    distributed_options,
    ignite_handlers_options,
    ignite_loggers_options,
)


def dataset_options(config):
    st.markdown("## Dataset Options")
    config["data_path"] = st.text_input("Dataset path (data_path)", "./")
    st.markdown("---")


def dataloader_options(config):
    st.markdown("## DataLoader Options")
    config["train_batch_size"] = st.number_input("Train batch size (train_batch_size)", min_value=1, value=4)
    config["eval_batch_size"] = st.number_input("Eval batch size (eval_batch_size)", min_value=1, value=8)
    config["num_workers"] = st.number_input("Number of workers (num_workers)", min_value=0, value=2)
    st.markdown("---")


def optimizer_options(config):
    st.markdown("## Optimizer Options")
    config["lr"] = st.number_input(
        "Learning rate used by torch.optim.* (lr)",
        min_value=0.0,
        value=1e-3,
        format="%e",
    )
    config["momentum"] = st.number_input(
        "momentum used by torch.optim.SGD (momentum)",
        min_value=0.0,
        value=0.9,
        format="%e",
    )
    config["weight_decay"] = st.number_input(
        "weight_decay used by torch.optim.SGD (weight_decay)",
        min_value=0.0,
        value=1e-4,
        format="%e",
    )
    st.markdown("---")


def training_options(config):
    st.markdown("## Training Options")
    config["max_epochs"] = st.number_input("Maximum epochs to train (max_epochs)", min_value=1, value=2)
    config["num_warmup_epochs"] = st.number_input(
        "number of warm-up epochs before learning rate decay (num_warmup_epochs)", min_value=1, value=4
    )
    st.markdown("---")


def model_options(config):
    st.markdown("## Model Options")
    models = (
        "resnet18",
        "alexnet",
        "vgg16",
        "squeezenet1_0",
        "densenet161",
        "inception_v3",
        "googlenet",
        "shufflenet_v2_x1_0",
        "mobilenet_v2",
        "mobilenet_v3_large",
        "mobilenet_v3_small",
    )
    config["model"] = st.selectbox("Models", options=models)
    st.markdown("---")


def get_configs():
    config = {}
    config["train_epoch_length"] = None
    config["eval_epoch_length"] = None
    default_none_options(config)

    with st.beta_expander("Image Classification Template Configurations", expanded=True):
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

    return config
