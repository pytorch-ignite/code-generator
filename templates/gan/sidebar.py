from argparse import Namespace

import streamlit as st
import toml


params = toml.load("./templates/gan/config.toml")


def get_configs() -> dict:
    config = {}
    with st.beta_expander("GAN Configurations"):
        st.info("Those in the parenthesis are used in the code.")
        for k, v in params.items():
            for kv, vv in v.items():
                if k in ("nproc_per_node"):  # , "nnodes", "node_rank", "master_addr", "master_port"):
                    if st.checkbox("Use distributed training"):
                        config[k] = getattr(st, kv)(**vv)
                else:
                    config[k] = getattr(st, kv)(**vv)

    return config
