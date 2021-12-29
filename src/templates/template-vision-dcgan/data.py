from typing import Any

import ignite.distributed as idist
import torchvision
import torchvision.transforms as T


def setup_data(config: Any):
    """Download datasets and create dataloaders

    Parameters
    ----------
    config: needs to contain `data_path`, `train_batch_size`, `eval_batch_size`, and `num_workers`
    """
    #::: if (it.use_dist) { :::#
    local_rank = idist.get_local_rank()
    #::: } :::#
    transform = T.Compose(
        [
            T.Resize(64),
            T.ToTensor(),
            T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    #::: if (it.use_dist) { :::#
    if local_rank > 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()
    #::: } :::#

    dataset_train = torchvision.datasets.CIFAR10(
        root=config.data_path,
        train=True,
        download=True,
        transform=transform,
    )
    dataset_eval = torchvision.datasets.CIFAR10(
        root=config.data_path,
        train=False,
        download=True,
        transform=transform,
    )
    nc = 3
    #::: if (it.use_dist) { :::#
    if local_rank == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()
    #::: } :::#

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
    return dataloader_train, dataloader_eval, nc
