{% extends "_argparse.py" %}
{% block imports %}{% endblock %}
{% block defaults %}
{{ super() }}
UPDATES = {
    "data_dir": {
        "default": "{{ data_dir }}",
        "type": str,
        "help": "Dataset cache directory",
    },
    "model": {
        "default": "{{ model }}",
        "type": str,
        "choices": ["bert-base-uncased"],
        "help": "Model name (from transformers) to setup model, tokenize and config to train",
    },
    "model_dir": {
        "default": "{{ model_dir }}",
        "type": str,
        "help": "Cache directory to download the pretrained model",
    },
    "tokenizer_dir": {
        "default": "{{ tokenizer_dir }}",
        "type": str,
        "help": "Tokenizer cache directory",
    },
    "num_classes": {
        "default": {{ num_classes }},
        "type": int,
        "help": "Number of target classes. Default, 1 (binary classification)",
    },
    "dropout": {
        "default": {{ dropout }},
        "type": float,
        "help": "Dropout probability",
    },
    "n_fc": {
        "default": {{ n_fc }},
        "type": int,
        "help": "Number of neurons in the last fully connected layer",
    },
    "max_length": {
        "default": {{ max_length }},
        "type": int,
        "help": "Maximum number of tokens for the inputs to the transformer model",
    },
    "batch_size": {
        "default": {{ batch_size }},
        "type": int,
        "help": "Total batch size",
    },
    "weight_decay": {
        "default": {{ weight_decay }},
        "type": float,
        "help": "Weight decay",
    },
    "num_workers": {
        "default": {{ num_workers }},
        "type": int,
        "help": "Number of workers in the data loader",
    },
    "max_epochs": {
        "default": {{ max_epochs }},
        "type": int,
        "help": "Number of epochs to train the model",
    },
    "learning_rate": {
        "default": {{ learning_rate }},
        "type": float,
        "help": "Peak of piecewise linear learning rate scheduler",
    },
    "num_warmup_epochs": {
        "default": {{ num_warmup_epochs }},
        "type": int,
        "help": "Number of warm-up epochs before learning rate decay",
    },
    "validate_every": {
        "default": {{ validate_every }},
        "type": int,
        "help": "Run model's validation every validate_every epochs",
    },
    "checkpoint_every": {
        "default": {{ checkpoint_every }},
        "type": int,
        "help": "Store training checkpoint every checkpoint_every iterations",
    },
    "log_every_iters": {
        "default": {{ log_every_iters }},
        "type": int,
        "help": "Argument to log batch loss every log_every_iters iterations. 0 to disable it",
    },
    "eval_epoch_length": {
        "default": None,
        "type": int,
        "help": "epoch_length of evaluator"
    },
}

DEFAULTS.update(UPDATES)
{% endblock %}
{% block get_default_parser %}{% endblock %}