import os
from typing import Any

import ignite.distributed as idist
import torchvision
import torchvision.transforms as T
from hydra.utils import get_original_cwd


def setup_data(config: Any):
    """Download datasets and create dataloaders

    Parameters
    ----------
    config: needs to contain `data_path`, `train_batch_size`, `eval_batch_size`, and `num_workers`
    """
    cwd = get_original_cwd()
    local_rank = idist.get_local_rank()
    transform = T.Compose(
        [
            T.ToTensor(),
            T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )

    if local_rank > 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    dataset_train = torchvision.datasets.CIFAR10(
        root=os.path.join(cwd, config.data_path),
        train=True,
        download=True,
        transform=transform,
    )
    dataset_eval = torchvision.datasets.CIFAR10(
        root=os.path.join(cwd, config.data_path),
        train=False,
        download=True,
        transform=transform,
    )
    if local_rank == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    dataloader_train = idist.auto_dataloader(
        dataset_train,
        batch_size=config.train_batch_size,
        shuffle=True,
        num_workers=config.num_workers,
    )
    dataloader_eval = idist.auto_dataloader(
        dataset_eval,
        batch_size=config.eval_batch_size,
        shuffle=False,
        num_workers=config.num_workers,
    )
    return dataloader_train, dataloader_eval
