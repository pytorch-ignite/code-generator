import sys

import streamlit as st

sys.path.append("./templates/base")

from base_sidebar import get_configs as base_configs


params = {
    "model_name": [
        "alexnet",
        "resnet",
        "vgg",
        "squeezenet",
        "inception_v3",
        "densenet",
        "googlenet",
        "mobilenetv2",
        "mobilenetv3",
        "mnasnet",
        "shufflenetv2",
    ],
    "exp_logging": [
        "wandb",
    ],
}


def get_configs() -> dict:
    config = base_configs()
    with st.beta_expander("Template Configurations"):
        config["model_name"] = st.selectbox("Model name (model_name)", params["model_name"], 1)
        config["exp_logging"] = st.selectbox("Experiment Tracking (exp_logging)", params["exp_logging"])

    return config
