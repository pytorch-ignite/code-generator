import sys
from argparse import Namespace

import streamlit as st
import toml

sys.path.append("./templates")

from _base._sidebar import (
    default_none_options,
    distributed_options,
    ignite_handlers_options,
    ignite_loggers_options,
)

params = toml.load("./templates/text_classification/_config.toml")
# params = Namespace(**{k: Namespace(**v) if isinstance(v, dict) else v for k, v in params.items()})
params = Namespace(**params)


def get_configs() -> dict:
    config = {}
    config["train_epoch_length"] = None
    config["eval_epoch_length"] = None
    default_none_options(config)

    st.header("Transformer")

    st.subheader("Model Options")
    config["model"] = st.selectbox(**params.model)
    config["model_dir"] = st.text_input(**params.model_dir)
    config["tokenizer_dir"] = st.text_input(**params.tokenizer_dir)
    config["num_classes"] = st.number_input(**params.num_classes)
    config["max_length"] = st.number_input(**params.max_length)
    config["dropout"] = st.number_input(**params.dropout)
    config["n_fc"] = st.number_input(**params.n_fc)
    st.markdown("---")

    st.subheader("Dataset Options")
    config["data_dir"] = st.text_input(**params.data_dir)
    st.markdown("---")

    st.subheader("DataLoader Options")
    config["batch_size"] = st.number_input(**params.batch_size)
    config["num_workers"] = st.number_input(**params.num_workers)
    st.markdown("---")

    st.subheader("Optimizer Options")
    config["learning_rate"] = st.number_input(**params.learning_rate)
    config["weight_decay"] = st.number_input(**params.weight_decay)
    st.markdown("---")

    st.subheader("Training Options")
    config["max_epochs"] = st.number_input(**params.max_epochs)
    config["num_warmup_epochs"] = st.number_input(**params.num_warmup_epochs)
    config["validate_every"] = st.number_input(**params.validate_every)
    config["checkpoint_every"] = st.number_input(**params.checkpoint_every)
    config["log_every_iters"] = st.number_input(**params.log_every_iters)
    st.markdown("---")

    distributed_options(config)
    ignite_handlers_options(config)
    ignite_loggers_options(config)

    return config
