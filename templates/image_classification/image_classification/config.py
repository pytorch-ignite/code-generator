{% extends "_argparse.pyi" %}
{% block get_default_parser %}
UPDATES = {
    # dataset options
    "data_path": {
        "default": "{{ data_path }}",
        "type": str,
        "help": "datasets path ({{ data_path }})",
    },
    # dataloader options
    "train_batch_size": {
        "default": {{train_batch_size}},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed ({{ train_batch_size }})",
    },
    "eval_batch_size": {
        "default": {{eval_batch_size}},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed ({{ eval_batch_size }})",
    },
    "num_workers": {
        "default": {{num_workers}},
        "type": int,
        "help": "num_workers for DataLoader ({{ num_workers }})",
    },
    # optimizer options
    "lr": {
        "default": {{lr}},
        "type": float,
        "help": "learning rate used by torch.optim.* ({{ lr }})",
    },
    "momentum": {
        "default": {{momentum}},
        "type": float,
        "help": "momentum used by torch.optim.SGD ({{ momentum }})",
    },
    "weight_decay": {
        "default": {{weight_decay}},
        "type": float,
        "help": "weight_decay used by torch.optim.SGD ({{ weight_decay }})",
    },
    # training options
    "max_epochs": {
        "default": {{max_epochs}},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for training ({{ max_epochs }})",
    },
    "num_warmup_epochs": {
        "default": {{num_warmup_epochs}},
        "type": int,
        "help": "number of warm-up epochs before learning rate decay. ({{ num_warmup_epochs }})",
    },
    # model options
    "model": {
        "default": "{{model}}",
        "type": str,
        "help": "model to use, available all torchvision classification models",
    }
}

DEFAULTS.update(UPDATES)

{{ super() }}
{% endblock %}
