import ignite.distributed as idist
from torchvision import datasets as dset
from torchvision import transforms as T


def get_datasets(dataset, dataroot):
    """

    Args:
        dataset (str): Name of the dataset to use. See CLI help for details
        dataroot (str): root directory where the dataset will be stored.

    Returns:
        dataset, num_channels
    """
    local_rank = idist.get_local_rank()

    if local_rank > 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    resize = T.Resize(64)
    crop = T.CenterCrop(64)
    to_tensor = T.ToTensor()
    normalize = T.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))

    if dataset in {"imagenet", "folder", "lfw"}:
        dataset = dset.ImageFolder(root=dataroot, transform=T.Compose([resize, crop, to_tensor, normalize]))
        nc = 3

    elif dataset == "lsun":
        dataset = dset.LSUN(
            root=dataroot, classes=["bedroom_train"], transform=T.Compose([resize, crop, to_tensor, normalize])
        )
        nc = 3

    elif dataset == "cifar10":
        dataset = dset.CIFAR10(root=dataroot, download=True, transform=T.Compose([resize, to_tensor, normalize]))
        nc = 3

    elif dataset == "mnist":
        dataset = dset.MNIST(root=dataroot, download=True, transform=T.Compose([resize, to_tensor, normalize]))
        nc = 1

    elif dataset == "fake":
        dataset = dset.FakeData(size=256, image_size=(3, 64, 64), transform=to_tensor)
        nc = 3

    else:
        raise RuntimeError(f"Invalid dataset name: {dataset}")

    if local_rank == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    return dataset, nc
