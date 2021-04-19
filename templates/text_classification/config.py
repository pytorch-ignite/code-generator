{% extends "_argparse.py" %}
{% block imports %}{% endblock %}
{% block defaults %}
{{ super() }}
UPDATES = {
    "data_dir": {
        "default": "{{ data_dir }}",
        "type": str,
        "help": "Dataset cache directory, Default: %(default)s",
    },
    "model": {
        "default": "{{ model }}",
        "type": str,
        "choices": ["bert-base-uncased"],
        "help": "Model name (from transformers) to setup model, tokenize and config to train, Default: %(default)s",
    },
    "model_dir": {
        "default": "{{ model_dir }}",
        "type": str,
        "help": "Cache directory to download the pretrained model, Default: %(default)s",
    },
    "tokenizer_dir": {
        "default": "{{ tokenizer_dir }}",
        "type": str,
        "help": "Tokenizer cache directory, Default: %(default)s",
    },
    "num_classes": {
        "default": {{ num_classes }},
        "type": int,
        "help": "Number of target classes. Default: %(default)s",
    },
    "dropout": {
        "default": {{ dropout }},
        "type": float,
        "help": "Dropout probability, Default: %(default)s",
    },
    "n_fc": {
        "default": {{ n_fc }},
        "type": int,
        "help": "Number of neurons in the last fully connected layer, Default: %(default)s",
    },
    "max_length": {
        "default": {{ max_length }},
        "type": int,
        "help": "Maximum number of tokens for the inputs to the transformer model, Default: %(default)s",
    },
    "batch_size": {
        "default": {{ batch_size }},
        "type": int,
        "help": "Total batch size, Default: %(default)s",
    },
    "weight_decay": {
        "default": {{ weight_decay }},
        "type": float,
        "help": "Weight decay, Default: %(default)s",
    },
    "num_workers": {
        "default": {{ num_workers }},
        "type": int,
        "help": "Number of workers in the data loader, Default: %(default)s",
    },
    "max_epochs": {
        "default": {{ max_epochs }},
        "type": int,
        "help": "Number of epochs to train the model, Default: %(default)s",
    },
    "learning_rate": {
        "default": {{ learning_rate }},
        "type": float,
        "help": "Peak of piecewise linear learning rate scheduler, Default: %(default)s",
    },
    "num_warmup_epochs": {
        "default": {{ num_warmup_epochs }},
        "type": int,
        "help": "Number of warm-up epochs before learning rate decay, Default: %(default)s",
    },
    "validate_every": {
        "default": {{ validate_every }},
        "type": int,
        "help": "Run model's validation every validate_every epochs, Default: %(default)s",
    },
    "checkpoint_every": {
        "default": {{ checkpoint_every }},
        "type": int,
        "help": "Store training checkpoint every checkpoint_every iterations, Default: %(default)s",
    },
    "log_every_iters": {
        "default": {{ log_every_iters }},
        "type": int,
        "help": "Argument to log batch loss every log_every_iters iterations. 0 to disable it, Default: %(default)s",
    },
    "eval_epoch_length": {
        "default": None,
        "type": int,
        "help": "epoch_length of evaluator, Default: %(default)s"
    },
}

DEFAULTS.update(UPDATES)
{% endblock %}
{% block get_default_parser %}{% endblock %}