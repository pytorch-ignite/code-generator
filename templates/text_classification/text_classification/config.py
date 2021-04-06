DEFAULTS = {
    "data_dir": {
        "default": "/tmp/data",
        "type": str,
        "help": "Dataset cache directory",
    },
    "model": {
        "default": "bert-base-uncased",
        "type": str,
        "choices": ["bert-base-uncased"],
        "help": "Model name (from transformers) to setup model, tokenize and config to train",
    },
    "model_dir": {
        "default": "/tmp/model",
        "type": str,
        "help": "Cache directory to download the pretrained model",
    },
    "tokenizer_dir": {
        "default": "/tmp/tokenizer",
        "type": str,
        "help": "Tokenizer cache directory",
    },
    "num_classes": {
        "default": 1,
        "type": int,
        "help": "Number of target classes. Default, 1 (binary classification)",
    },
    "dropout": {
        "default": 0.3,
        "type": float,
        "help": "Dropout probability",
    },
    "n_fc": {
        "default": 768,
        "type": int,
        "help": "Number of neurons in the last fully connected layer",
    },
    "max_length": {
        "default": 256,
        "type": int,
        "help": "Maximum number of tokens for the inputs to the transformer model",
    },
    "batch_size": {
        "default": 1,
        "type": int,
        "help": "Total batch size",
    },
    "weight_decay": {
        "default": 0.01,
        "type": float,
        "help": "Weight decay",
    },
    "num_workers": {
        "default": 4,
        "type": int,
        "help": "Number of workers in the data loader",
    },
    "num_epochs": {
        "default": 3,
        "type": int,
        "help": "Number of epochs to train the model",
    },
    "learning_rate": {
        "default": 5e-5,
        "type": float,
        "help": "Peak of piecewise linear learning rate scheduler",
    },
    "num_warmup_epochs": {
        "default": 0,
        "type": int,
        "help": "Number of warm-up epochs before learning rate decay",
    },
    "validate_every": {
        "default": 1,
        "type": int,
        "help": "Run model's validation every validate_every epochs",
    },
    "checkpoint_every": {
        "default": 1000,
        "type": int,
        "help": "Store training checkpoint every checkpoint_every iterations",
    },
    "resume_from": {
        "default": None,
        "type": str,
        "help": "Path to checkpoint to use to resume the training from",
    },
    "log_every_iters": {
        "default": 15,
        "type": int,
        "help": "Argument to log batch loss every log_every_iters iterations. 0 to disable it",
    },
    "with_clearml": {
        "default": False,
        "type": bool,
        "help": "Setup experiment ClearML logger",
    },
}
