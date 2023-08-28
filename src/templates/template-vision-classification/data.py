from typing import Any

import ignite.distributed as idist
import torchvision
import torchvision.transforms as T


def setup_data(config: Any):
    """Download datasets and create dataloaders

    Parameters
    ----------
    config: needs to contain `data_path`, `batch_size`, `eval_batch_size`, and `num_workers`
    """
    #::: if (it.use_dist) { :::#
    local_rank = idist.get_local_rank()
    #::: } :::#
    train_transform = T.Compose(
        [
            T.Pad(4),
            T.RandomCrop(32, fill=128),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    eval_transform = T.Compose(
        [
            T.ToTensor(),
            T.Normalize(mean=[0.4914, 0.4822, 0.4465], std=[0.2023, 0.1994, 0.2010]),
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
        transform=train_transform,
    )
    dataset_eval = torchvision.datasets.CIFAR10(
        root=config.data_path,
        train=False,
        download=True,
        transform=eval_transform,
    )

    #::: if (it.use_dist) { :::#
    if local_rank == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()
    #::: } :::#

    dataloader_train = idist.auto_dataloader(
        dataset_train,
        batch_size=config.batch_size,
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
