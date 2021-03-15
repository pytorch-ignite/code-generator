import json
import sys

import streamlit as st

sys.path.append("./templates/base")

from base_config import get_configs as base_configs


def get_configs() -> dict:
    with open("./templates/image_classification/metadata.json", "r") as fp:
        model_names = json.load(fp)["model_name"]

    config = base_configs()
    with st.beta_expander("Template Configurations"):
        config["model_name"] = st.selectbox("Model name (model_name)", model_names)

    return config
