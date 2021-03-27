"""
`train_engine` and `eval_engine`
"""
from typing import Any, Tuple
import torch
from ignite.engine import Engine


# Edit below functions the way how the model will be training

# model_train_fn inside train_fn closure is how the model will be learning with given batch
# model_train_fn has to be provided with two arguments - engine which will be calling the
# model_train_fn with the provided current batch in each iteration
# any necessary arguments can be provided in train_fn
def train_fn():
    def model_train_fn(engine: Engine, batch: Any):
        return batch

    return model_train_fn


# model_eval_fn inside evaluate_fn closure is how the model will be evaluating with given batch
# model_eval_fn has to be provided with two arguments - engine which will be calling the
# model_eval_fn with the provided current batch in each iteration
# any necessary arguments can be provided in evaluate_fn
@torch.no_grad()
def evaluate_fn():
    def model_eval_fn(engine: Engine, batch: Any):
        return batch

    return model_eval_fn


# function for creating engines which will be used in main.py
# any necessary arguments can be provided.
def create_engines() -> Tuple[Engine]:
    train_engine = Engine(train_fn())
    eval_engine = Engine(evaluate_fn())

    return train_engine, eval_engine
