import sys

import streamlit as st

sys.path.append("./templates/")

from base.sidebar import get_configs as base_configs


params = {
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


def get_configs() -> dict:
    config = base_configs()
    config["project_name"] = None
    with st.beta_expander("Template Configurations"):

        # group by streamlit function type
        config["model_name"] = st.selectbox("Model name (model_name)", params["model_name"], 1)
        config["exp_logging"] = st.selectbox("Experiment tracking (exp_logging)", params["exp_logging"])
        if config["exp_logging"] is not None:
            config["project_name"] = st.text_input("Project name of experiment tracking system (project_name)")

        config["n_saved"] = st.number_input("Number of best models to store (n_saved)", min_value=1, value=2)

    return config
