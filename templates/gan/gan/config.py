{% extends "_argparse.py" %}
{% block get_default_parser %}
UPDATES = {
    # dataset options
    "dataset": {
        "default": "{{ dataset }}",
        "type": str,
        "choices": ["cifar10", "lsun", "imagenet", "folder", "lfw", "fake", "mnist"],
        "help": "dataset to use ({{ dataset }})",
    },
    "data_path": {
        "default": "{{ data_path }}",
        "type": str,
        "help": "datasets path ({{ data_path }})",
    },
    # dataloader options
    "batch_size": {
        "default": {{batch_size}},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed ({{ batch_size }})",
    },
    "num_workers": {
        "default": {{num_workers}},
        "type": int,
        "help": "num_workers for DataLoader ({{ num_workers }})",
    },
    # optimizer options
    "beta_1": {
        "default": {{beta_1}},
        "type": float,
        "help": "beta_1 for Adam optimizer ({{ beta_1 }})",
    },
    "lr": {
        "default": {{lr}},
        "type": float,
        "help": "learning rate used by torch.optim.* ({{ lr }})",
    },
    # training options
    "max_epochs": {
        "default": {{max_epochs}},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for training ({{ max_epochs }})",
    },
    # model options
    "z_dim": {
        "default": {{z_dim}},
        "type": int,
        "help": "size of the latent z vector ({{ z_dim }})",
    },
    "g_filters": {
        "default": {{g_filters}},
        "type": int,
        "help": "number of filters in the second-to-last generator deconv layer ({{ g_filters }})",
    },
    "d_filters": {
        "default": {{d_filters}},
        "type": int,
        "help": "number of filters in first discriminator conv layer ({{ d_filters }})",
    },
}

DEFAULTS.update(UPDATES)

{{ super() }}
{% endblock %}
