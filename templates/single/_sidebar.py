import sys

import streamlit as st

sys.path.append("./templates")

from _base._sidebar import default_none_options, distributed_options, ignite_handlers_options, ignite_loggers_options


def get_configs():
    config = {}
    config["train_epoch_length"] = None
    config["eval_epoch_length"] = None
    default_none_options(config)

    with st.beta_expander("Single Model, Single Optimizer Template Configurations", expanded=True):
        st.info("Those in the parenthesis are used in the generated code.")

        # group by configurations type
        distributed_options(config)
        ignite_handlers_options(config)
        ignite_loggers_options(config)

    return config
