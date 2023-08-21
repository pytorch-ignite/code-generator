import os
from argparse import Namespace
from typing import Iterable

import ignite.distributed as idist
import pytest
from data import setup_data
from omegaconf import OmegaConf
from torch import nn, optim
from torch.functional import Tensor
from torch.utils.data import DataLoader
from utils import save_config


def set_up():
    model = nn.Linear(1, 1)
    optimizer = optim.Adam(model.parameters())
    device = idist.device()
    loss_fn = nn.MSELoss()
    return model, optimizer, loss_fn, device


@pytest.mark.skipif(os.getenv("RUN_SLOW_TESTS", 0) == 0, reason="Skip slow tests")
def test_setup_data():
    config = Namespace(
        data_path="/tmp/data",
        model="bert-base-uncased",
        tokenizer_dir="/tmp/tokenizer",
        max_length=1,
        train_batch_size=1,
        eval_batch_size=1,
        num_workers=1,
    )
    train_loader, eval_loader = setup_data(config)
    assert isinstance(train_loader, DataLoader)
    assert isinstance(eval_loader, DataLoader)

    train_batch = next(iter(train_loader))
    assert isinstance(train_batch, Iterable)
    assert isinstance(train_batch["input_ids"], Tensor)
    assert isinstance(train_batch["attention_mask"], Tensor)
    assert isinstance(train_batch["token_type_ids"], Tensor)
    assert isinstance(train_batch["label"], Tensor)

    eval_batch = next(iter(eval_loader))
    assert isinstance(eval_batch["input_ids"], Tensor)
    assert isinstance(eval_batch["attention_mask"], Tensor)
    assert isinstance(eval_batch["token_type_ids"], Tensor)
    assert isinstance(eval_batch["label"], Tensor)


#::= from_template_common ::#
