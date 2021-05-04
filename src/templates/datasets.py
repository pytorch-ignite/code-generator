### imports ###
import ignite.distributed as idist


### vision_datasets ###
def get_datasets(path):
    import torchvision.transforms as T
    from torchvision.datasets import CIFAR10

    train_transform = T.Compose(
        [
            T.Pad(4),
            T.RandomCrop(32, fill=128),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ]
    )

    eval_transform = T.Compose(
        [
            T.ToTensor(),
            T.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
        ]
    )
    local_rank = idist.get_local_rank()

    if local_rank > 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    train_ds = CIFAR10(
        root=path, train=True, download=True, transform=train_transform
    )
    eval_ds = CIFAR10(
        root=path, train=False, download=True, transform=eval_transform
    )

    if local_rank == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    return train_ds, eval_ds
