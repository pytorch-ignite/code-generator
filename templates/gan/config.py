{% extends "_argparse.py" %}
{% block get_default_parser %}
UPDATES = {
    # dataset options
    "dataset": {
        "default": "{{ dataset }}",
        "type": str,
        "choices": ["cifar10", "lsun", "imagenet", "folder", "lfw", "fake", "mnist"],
        "help": "dataset to use. Default: %(default)s",
    },
    "data_path": {
        "default": "{{ data_path }}",
        "type": str,
        "help": "datasets path. Default: %(default)s",
    },
    # dataloader options
    "batch_size": {
        "default": {{batch_size}},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed. Default: %(default)s",
    },
    "num_workers": {
        "default": {{num_workers}},
        "type": int,
        "help": "num_workers for DataLoader. Default: %(default)s",
    },
    # optimizer options
    "beta_1": {
        "default": {{beta_1}},
        "type": float,
        "help": "beta_1 for Adam optimizer. Default: %(default)s",
    },
    "lr": {
        "default": {{lr}},
        "type": float,
        "help": "learning rate used by torch.optim.*. Default: %(default)s",
    },
    # training options
    "max_epochs": {
        "default": {{max_epochs}},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for training. Default: %(default)s",
    },
    # model options
    "z_dim": {
        "default": {{z_dim}},
        "type": int,
        "help": "size of the latent z vector. Default: %(default)s",
    },
    "g_filters": {
        "default": {{g_filters}},
        "type": int,
        "help": "number of filters in the second-to-last generator deconv layer. Default: %(default)s",
    },
    "d_filters": {
        "default": {{d_filters}},
        "type": int,
        "help": "number of filters in first discriminator conv layer. Default: %(default)s",
    },
}

DEFAULTS.update(UPDATES)

{{ super() }}
{% endblock %}
