from argparse import Namespace

import toml
import streamlit as st


params = toml.load("./templates/text_classification/config.toml")
# params = Namespace(**{k: Namespace(**v) if isinstance(v, dict) else v for k, v in params.items()})
params = Namespace(**params)
# Handle Nones after toml
params.backend["options"][0] = None
params.nproc_per_node["value"] = None
params.resume_from["value"] = None


def get_configs() -> dict:
    config = {}
    st.header("Transformer")
    config["seed"] = st.number_input(**params.seed)
    config["data_dir"] = st.text_input(**params.data_dir)
    config["output_dir"] = st.text_input(**params.output_dir)
    config["model"] = st.selectbox(**params.model)
    config["model_dir"] = st.text_input(**params.model_dir)
    config["tokenizer_dir"] = st.text_input(**params.tokenizer_dir)
    config["num_classes"] = st.number_input(**params.num_classes)
    config["dropout"] = st.number_input(**params.dropout)
    config["n_fc"] = st.number_input(**params.n_fc)
    config["max_length"] = st.number_input(**params.max_length)
    config["batch_size"] = st.number_input(**params.batch_size)
    config["weight_decay"] = st.number_input(**params.weight_decay)
    config["num_workers"] = st.number_input(**params.num_workers)
    config["num_epochs"] = st.number_input(**params.num_epochs)
    config["learning_rate"] = st.number_input(**params.learning_rate)
    config["num_warmup_epochs"] = st.number_input(**params.num_warmup_epochs)
    config["validate_every"] = st.number_input(**params.validate_every)
    config["checkpoint_every"] = st.number_input(**params.checkpoint_every)
    config["backend"] = st.selectbox(**params.backend)
    config["nproc_per_node"] = st.text_input(**params.nproc_per_node)
    config["resume_from"] = st.text_input(**params.resume_from)
    config["log_every_iters"] = st.number_input(**params.log_every_iters)
    config["with_clearml"] = st.checkbox(**params.with_clearml)
    config["with_amp"] = st.checkbox(**params.with_amp)
    return config
