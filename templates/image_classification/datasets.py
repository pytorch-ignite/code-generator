import ignite.distributed as idist
from torchvision import datasets
from torchvision.transforms import (
    Compose,
    Normalize,
    Pad,
    RandomCrop,
    RandomHorizontalFlip,
    ToTensor,
)

train_transform = Compose(
    [
        Pad(4),
        RandomCrop(32, fill=128),
        RandomHorizontalFlip(),
        ToTensor(),
        Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ]
)

eval_transform = Compose(
    [
        ToTensor(),
        Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ]
)


def get_datasets(path):
    local_rank = idist.get_local_rank()

    if local_rank > 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    train_ds = datasets.CIFAR10(root=path, train=True, download=True, transform=train_transform)
    eval_ds = datasets.CIFAR10(root=path, train=False, download=True, transform=eval_transform)

    if local_rank == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    return train_ds, eval_ds
