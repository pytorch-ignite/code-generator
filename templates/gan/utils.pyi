{% block imports %}
from argparse import ArgumentParser

{% endblock %}

{% block get_default_parser %}
DEFAULTS = {
    "batch_size": {
        "default": {{ batch_size }},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed ({{ batch_size }})",
    },
    "data_path": {
        "default": "{{ data_path }}",
        "type": str,
        "help": "datasets path ({{ data_path }})",
    },
    "filepath": {
        "default": "{{ filepath }}",
        "type": str,
        "help": "logging file path ({{ filepath }})",
    },
    "num_workers": {
        "default": {{ num_workers }},
        "type": int,
        "help": "num_workers for DataLoader ({{ num_workers }})",
    },
    "max_epochs": {
        "default": {{ max_epochs }},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for training ({{ max_epochs }})",
    },
    "epoch_length": {
        "default": None,
        "type": int,
        "help": "epoch_length of ignite.Engine.run() for training (None)",
    },
    "lr": {
        "default": {{ lr }},
        "type": float,
        "help": "learning rate used by torch.optim.* ({{ lr }})",
    },
    "log_train": {
        "default": {{ log_train }},
        "type": int,
        "help": "logging interval of training iteration ({{ log_train }})",
    },
    "seed": {
        "default": {{ seed }},
        "type": int,
        "help": "used in ignite.utils.manual_seed() ({{ seed }})",
    },
    "verbose": {
        "action": "store_true",
        "help": "use logging.INFO in ignite.utils.setup_logger",
    },
    "nproc_per_node": {
        "default": {{ nproc_per_node }},
        "type": int,
        "help": """number of processes to launch on each node, for GPU training
                this is recommended to be set to the number of GPUs in your system
                so that each process can be bound to a single GPU ({{ nproc_per_node }})""",
    },
    "nnodes": {
        "default": {{ nnodes }},
        "type": int,
        "help": "number of nodes to use for distributed training ({{ nnodes }})",
    },
    "node_rank": {
        "default": {{ node_rank }},
        "type": int,
        "help": "rank of the node for multi-node distributed training ({{ node_rank }})",
    },
    "master_addr": {
        "default": {{ master_addr }},
        "type": str,
        "help": "master node TCP/IP address for torch native backends ({{ master_addr }})",
    },
    "master_port": {
        "default": {{ master_port }},
        "type": int,
        "help": "master node port for torch native backends {{ master_port }}"
    },
    "n_saved": {
        "default": {{ n_saved }},
        "type": int,
        "help": "number of best models to store ({{ n_saved }})",
    },
    "dataset": {
        "default": "{{ dataset }}",
        "type": str,
        "choices": ["cifar10", "lsun", "imagenet", "folder", "lfw", "fake", "mnist"],
        "help": "dataset to use ({{ dataset }})",
    },
    "z_dim": {
        "default": {{ z_dim }},
        "type": int,
        "help": "size of the latent z vector ({{ z_dim }})",
    },
    "alpha": {
        "default": {{ alpha }},
        "type": float,
        "help": "running average decay factor ({{ alpha }})",
    },
    "g_filters": {
        "default": {{ g_filters }},
        "type": int,
        "help": "number of filters in the second-to-last generator deconv layer ({{ g_filters }})",
    },
    "d_filters": {
        "default": {{ d_filters }},
        "type": int,
        "help": "number of filters in first discriminator conv layer ({{ d_filters }})",
    },
    "beta_1": {
        "default": {{ beta_1 }},
        "type": float,
        "help": "beta_1 for Adam optimizer ({{ beta_1 }})",
    },
    "saved_G": {
        "default": {{ saved_G }},
        "type": str,
        "help": "path to saved generator ({{ saved_G }})",
    },
    "saved_D": {
        "default": {{ saved_D }},
        "type": str,
        "help": "path to saved discriminator ({{ saved_D }})",
    }
}


def get_default_parser():
    """Get the default configs for training."""
    parser = ArgumentParser(add_help=False)

    for key, value in DEFAULTS.items():
        parser.add_argument(f"--{key}", **value)

    return parser
{% endblock %}
