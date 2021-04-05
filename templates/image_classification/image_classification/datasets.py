from torchvision import datasets
from torchvision.transforms import Compose, Normalize, Pad, RandomCrop, RandomHorizontalFlip, ToTensor

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
    train_ds = datasets.CIFAR10(root=path, train=True, download=True, transform=train_transform)
    eval_ds = datasets.CIFAR10(root=path, train=False, download=True, transform=eval_transform)

    return train_ds, eval_ds
