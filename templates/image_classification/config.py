{% extends "_argparse.py" %}
{% block get_default_parser %}
UPDATES = {
    # dataset options
    "data_path": {
        "default": "{{ data_path }}",
        "type": str,
        "help": "datasets path. Default: %(default)s",
    },
    # dataloader options
    "train_batch_size": {
        "default": {{train_batch_size}},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed. Default: %(default)s",
    },
    "eval_batch_size": {
        "default": {{eval_batch_size}},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed. Default: %(default)s",
    },
    "num_workers": {
        "default": {{num_workers}},
        "type": int,
        "help": "num_workers for DataLoader. Default: %(default)s",
    },
    # optimizer options
    "lr": {
        "default": {{lr}},
        "type": float,
        "help": "learning rate used by torch.optim.*. Default: %(default)s",
    },
    "momentum": {
        "default": {{momentum}},
        "type": float,
        "help": "momentum used by torch.optim.SGD. Default: %(default)s",
    },
    "weight_decay": {
        "default": {{weight_decay}},
        "type": float,
        "help": "weight_decay used by torch.optim.SGD. Default: %(default)s",
    },
    # training options
    "max_epochs": {
        "default": {{max_epochs}},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for training. Default: %(default)s",
    },
    "num_warmup_epochs": {
        "default": {{num_warmup_epochs}},
        "type": int,
        "help": "number of warm-up epochs before learning rate decay. Default: %(default)s",
    },
    # model options
    "model": {
        "default": "{{model}}",
        "type": str,
        "help": "model to use, available all torchvision classification models. Default: %(default)s",
    }
}

DEFAULTS.update(UPDATES)

{{ super() }}
{% endblock %}
