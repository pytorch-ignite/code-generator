{% block imports %}
from argparse import ArgumentParser
from typing import Any, Optional

import ignite.distributed as idist
import torch
from ignite.contrib.engines import common
from ignite.engine.engine import Engine
from models import get_model
from torch import nn, optim
from torch.optim.optimizer import Optimizer

{% endblock %}

{% block get_default_parser %}
DEFAULTS = {
    "train_batch_size": {
        "default": {{ train_batch_size }},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed ({{ train_batch_size }})",
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
    "train_max_epochs": {
        "default": {{ train_max_epochs }},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for training ({{ train_max_epochs }})",
    },
    "eval_max_epochs": {
        "default": {{ eval_max_epochs }},
        "type": int,
        "help": "max_epochs of ignite.Engine.run() for evaluation ({{ eval_max_epochs }})",
    },
    "train_epoch_length": {
        "default": {{ train_epoch_length }},
        "type": int,
        "help": "epoch_length of ignite.Engine.run() for training ({{ train_epoch_length }})",
    },
    "eval_epoch_length": {
        "default": {{ eval_epoch_length }},
        "type": int,
        "help": "epoch_length of ignite.Engine.run() for evaluation ({{ eval_epoch_length }})",
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
    "log_eval": {
        "default": {{ log_eval }},
        "type": int,
        "help": "logging interval of evaluation epoch ({{ log_eval }})",
    },
    "seed": {
        "default": {{ seed }},
        "type": int,
        "help": "used in ignite.utils.manual_seed() ({{ seed }})",
    },
    "eval_batch_size": {
        "default": {{ eval_batch_size }},
        "type": int,
        "help": "will be equally divided by number of GPUs if in distributed ({{ eval_batch_size }})",
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
    "model_name": {
        "default": "{{ model_name }}",
        "type": str,
        "help": "image classification model name ({{ model_name }})",
    },
    "project_name": {
        "default": "{{ project_name }}",
        "type": str,
        "help": "project name of experiment tracking system ({{ project_name }})"
    },
    "n_saved": {
        "default": {{ n_saved }},
        "type": int,
        "help": "number of best models to store ({{ n_saved }})",
    },
    "save_every_iters": {
        "default": {{ save_every_iters }},
        "type": int,
        "help": "model saving interval ({{ save_every_iters }})",
    }
}


def get_default_parser():
    """Get the default configs for training."""
    parser = ArgumentParser(add_help=False)

    for key, value in DEFAULTS.items():
        parser.add_argument(f"--{key}", **value)

    return parser
{% endblock %}


{% block log_metrics %}
def log_metrics(engine: Engine, tag: str, device: torch.device) -> None:
    """Log ``engine.state.metrics`` with given ``engine``
    and memory info with given ``device``.

    Args:
        engine (Engine): instance of ``Engine`` which metrics to log.
        tag (str): a string to add at the start of output.
        device (torch.device): current torch.device to log memory info.
    """
    max_epochs = len(str(engine.state.max_epochs))
    max_iters = len(str(engine.state.max_iters))
    metrics_format = "{tag} [{epoch:>{max_epochs}}/{iteration:0{max_iters}d}]: {metrics}".format(
        tag=tag,
        epoch=engine.state.epoch,
        max_epochs=max_epochs,
        iteration=engine.state.iteration,
        max_iters=max_iters,
        metrics=engine.state.metrics,
    )
    if "cuda" in device.type:
        metrics_format += " Memory - {:.2f} MB".format(
            torch.cuda.max_memory_allocated(device) / (1024.0 * 1024.0)
        )
    engine.logger.info(metrics_format)
{% endblock %}


{% block initialize %}
def initialize(config: Any):
    device = idist.device()
    model = idist.auto_model(get_model(config.model_name))
    optimizer = idist.auto_optim(optim.Adam(model.parameters(), lr=config.lr))
    loss_fn = nn.CrossEntropyLoss().to(device)

    return device, model, optimizer, loss_fn
{% endblock %}


{% block eval_ckpt_common_training %}
def setup_common_handlers(
    config: Any,
    eval_engine: Engine,
    train_engine: Engine,
    model: nn.Module,
    optimizer: Optimizer
):
    eval_ckpt_handler = common.save_best_model_by_val_score(
        output_path=config.filepath,
        evaluator=eval_engine,
        model=model,
        metric_name='eval_accuracy',
        n_saved=config.n_saved,
        trainer=train_engine,
        tag='eval',
    )
    to_save = {
        'model': model,
        'optimizer': optimizer,
        'train_enginer': train_engine
    }
    common.setup_common_training_handlers(
        trainer=train_engine,
        to_save=to_save,
        save_every_iters=config.save_every_iters,
        output_path=config.filepath,
        with_pbars=False,
        clear_cuda_cache=False
    )
    return eval_ckpt_handler
{% endblock %}

{% block exp_logging %}
def setup_exp_logging(
    train_engine: Engine,
    config: Any,
    eval_engine: Optional[Engine] = None,
    optimizer: Optional[Optimizer] = None,
    name: Optional[str] = None
):
    {% if exp_logging == "wandb" %}
    exp_logger = common.setup_wandb_logging(
        trainer=train_engine,
        optimizers=optimizer,
        evaluators=eval_engine,
        config=config,
        project=config.project_name,
        name=name,
    )
    return exp_logger
    {% else %}
    return None
    {% endif %}
{% endblock %}
