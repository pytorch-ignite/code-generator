{% block imports %}
from argparse import ArgumentParser
{% endblock %}

{% block defaults %}
DEFAULTS = {
    "use_amp": {
        "action": "store_true",
        "help": "use torch.cuda.amp for automatic mixed precision. Default: %(default)s"
    },
    "resume_from": {
        "default": None,
        "type": str,
        "help": "path to the checkpoint file to resume, can also url starting with https. Default: %(default)s"
    },
    "seed": {
        "default": 666,
        "type": int,
        "help": "seed to use in ignite.utils.manual_seed(). Default: %(default)s"
    },
    "verbose": {
        "action": "store_true",
        "help": "use logging.INFO in ignite.utils.setup_logger. Default: %(default)s",
    },

    # distributed training options
    "backend": {
        "default": None,
        "type": str,
        "help": "backend to use for distributed training. Default: %(default)s",
    },
    "nproc_per_node": {
        "default": {{nproc_per_node}},
        "type": int,
        "help": """number of processes to launch on each node, for GPU training
                this is recommended to be set to the number of GPUs in your system
                so that each process can be bound to a single GPU. Default: %(default)s""",
    },
    "node_rank": {
        "default": {{node_rank}},
        "type": int,
        "help": "rank of the node for multi-node distributed training. Default: %(default)s",
    },
    "nnodes": {
        "default": {{nnodes}},
        "type": int,
        "help": "number of nodes to use for distributed training. Default: %(default)s",
    },
    "master_addr": {
        "default": {{master_addr}},
        "type": str,
        "help": "master node TCP/IP address for torch native backends. Default: %(default)s",
    },
    "master_port": {
        "default": {{master_port}},
        "type": int,
        "help": "master node port for torch native backends. Default: %(default)s",
    },
    "train_epoch_length": {
        "default": None,
        "type": int,
        "help": "epoch_length of Engine.run() for training. Default: %(default)s"
    },
    "eval_epoch_length": {
        "default": None,
        "type": int,
        "help": "epoch_length of Engine.run() for evaluation. Default: %(default)s"
    },
    # ignite handlers options
    "save_every_iters": {
        "default": {{save_every_iters}},
        "type": int,
        "help": "Saving iteration interval. Default: %(default)s",
    },
    "n_saved": {
        "default": {{n_saved}},
        "type": int,
        "help": "number of best models to store. Default: %(default)s",
    },
    "log_every_iters": {
        "default": {{log_every_iters}},
        "type": int,
        "help": "logging interval for iteration progress bar. Default: %(default)s",
    },
    "with_pbars": {
        "default": {{with_pbars}},
        "type": bool,
        "help": "show epoch-wise and iteration-wise progress bars. Default: %(default)s",
    },
    "with_pbar_on_iters": {
        "default": {{with_pbar_on_iters}},
        "type": bool,
        "help": "show iteration progress bar or not. Default: %(default)s",
    },
    "stop_on_nan": {
        "default": {{stop_on_nan}},
        "type": bool,
        "help": "stop the training if engine output contains NaN/inf values. Default: %(default)s",
    },
    "clear_cuda_cache": {
        "default": {{clear_cuda_cache}},
        "type": bool,
        "help": "clear cuda cache every end of epoch. Default: %(default)s",
    },
    "with_gpu_stats": {
        "default": {{with_gpu_stats}},
        "type": bool,
        "help": "show gpu information, requires pynvml. Default: %(default)s",
    },
    "patience": {
        "default": {{patience}},
        "type": int,
        "help": "number of events to wait if no improvement and then stop the training. Default: %(default)s"
    },
    "limit_sec": {
        "default": {{limit_sec}},
        "type": int,
        "help": "maximum time before training terminates in seconds. Default: %(default)s"
    },

    # ignite logger options
    "output_dir": {
        "default": "{{ output_dir }}",
        "type": str,
        "help": "directory to save all outputs. Default: %(default)s",
    },
    "logger_log_every_iters": {
        "default": {{logger_log_every_iters}},
        "type": int,
        "help": "logging interval for experiment tracking system. Default: %(default)s",
    },
}
{% endblock %}


{% block get_default_parser %}
def get_default_parser() -> ArgumentParser:
    """Get the default configs for training."""
    parser = ArgumentParser(add_help=False)

    for key, value in DEFAULTS.items():
        parser.add_argument(f"--{key}", **value)

    return parser
{% endblock %}
