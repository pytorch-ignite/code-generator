{% block imports %}
from argparse import ArgumentParser
{% endblock %}

{% block defaults %}
DEFAULTS = {
    "use_amp": {
        "action": "store_true",
        "help": "use torch.cuda.amp for automatic mixed precision"
    },
    "resume_from": {
        "default": None,
        "type": str,
        "help": "path to the checkpoint file to resume, can also url starting with https (None)"
    },
    "seed": {
        "default": 666,
        "type": int,
        "help": "seed to use in ignite.utils.manual_seed() (666)"
    },
    "verbose": {
        "action": "store_true",
        "help": "use logging.INFO in ignite.utils.setup_logger",
    },

    # distributed training options
    "backend": {
        "default": None,
        "type": str,
        "help": "backend to use for distributed training (None)",
    },
    "nproc_per_node": {
        "default": {{nproc_per_node}},
        "type": int,
        "help": """number of processes to launch on each node, for GPU training
                this is recommended to be set to the number of GPUs in your system
                so that each process can be bound to a single GPU ({{ nproc_per_node }})""",
    },
    "node_rank": {
        "default": {{node_rank}},
        "type": int,
        "help": "rank of the node for multi-node distributed training ({{ node_rank }})",
    },
    "nnodes": {
        "default": {{nnodes}},
        "type": int,
        "help": "number of nodes to use for distributed training ({{ nnodes }})",
    },
    "master_addr": {
        "default": {{master_addr}},
        "type": str,
        "help": "master node TCP/IP address for torch native backends ({{ master_addr }})",
    },
    "master_port": {
        "default": {{master_port}},
        "type": int,
        "help": "master node port for torch native backends ({{ master_port }})",
    },
    "train_epoch_length": {
        "default": None,
        "type": int,
        "help": "epoch_length of Engine.run() for training"
    },
    "eval_epoch_length": {
        "default": None,
        "type": int,
        "help": "epoch_length of Engine.run() for evaluation"
    },
    # ignite handlers options
    "save_every_iters": {
        "default": {{save_every_iters}},
        "type": int,
        "help": "Saving iteration interval ({{save_every_iters}})",
    },
    "n_saved": {
        "default": {{n_saved}},
        "type": int,
        "help": "number of best models to store ({{ n_saved }})",
    },
    "log_every_iters": {
        "default": {{log_every_iters}},
        "type": int,
        "help": "logging interval for iteration progress bar ({{log_every_iters}})",
    },
    "with_pbars": {
        "default": {{with_pbars}},
        "type": bool,
        "help": "show epoch-wise and iteration-wise progress bars ({{with_pbars}})",
    },
    "with_pbar_on_iters": {
        "default": {{with_pbar_on_iters}},
        "type": bool,
        "help": "show iteration progress bar or not ({{with_pbar_on_iters}})",
    },
    "stop_on_nan": {
        "default": {{stop_on_nan}},
        "type": bool,
        "help": "stop the training if engine output contains NaN/inf values ({{stop_on_nan}})",
    },
    "clear_cuda_cache": {
        "default": {{clear_cuda_cache}},
        "type": bool,
        "help": "clear cuda cache every end of epoch ({{clear_cuda_cache}})",
    },
    "with_gpu_stats": {
        "default": {{with_gpu_stats}},
        "type": bool,
        "help": "show gpu information, requires pynvml ({{with_gpu_stats}})",
    },
    "patience": {
        "default": {{patience}},
        "type": int,
        "help": "number of events to wait if no improvement and then stop the training ({{patience}})"
    },
    "limit_sec": {
        "default": {{limit_sec}},
        "type": int,
        "help": "maximum time before training terminates in seconds ({{limit_sec}})"
    },

    # ignite logger options
    "output_dir": {
        "default": "{{ output_dir }}",
        "type": str,
        "help": "directory to save all outputs ({{ output_dir }})",
    },
    "logger_log_every_iters": {
        "default": {{logger_log_every_iters}},
        "type": int,
        "help": "logging interval for experiment tracking system ({{logger_log_every_iters}})",
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
