from argparse import Namespace

import albumentations as A
import cv2
import ignite.distributed as idist
import numpy as np
import torch
from albumentations.pytorch import ToTensorV2 as ToTensor
from ignite.utils import convert_tensor
from PIL import Image
from torch.utils.data import Dataset
from torchvision.datasets.voc import VOCSegmentation


class TransformedDataset(Dataset):
    def __init__(self, ds, transform_fn):
        assert isinstance(ds, Dataset)
        assert callable(transform_fn)
        self.ds = ds
        self.transform_fn = transform_fn

    def __len__(self):
        return len(self.ds)

    def __getitem__(self, index):
        dp = self.ds[index]
        return self.transform_fn(**dp)


class VOCSegmentationPIL(VOCSegmentation):

    target_names = [
        "background",
        "aeroplane",
        "bicycle",
        "bird",
        "boat",
        "bottle",
        "bus",
        "car",
        "cat",
        "chair",
        "cow",
        "diningtable",
        "dog",
        "horse",
        "motorbike",
        "person",
        "plant",
        "sheep",
        "sofa",
        "train",
        "tv/monitor",
    ]

    def __init__(self, *args, return_meta=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.return_meta = return_meta

    def __getitem__(self, index):
        img = np.asarray(Image.open(self.images[index]).convert("RGB"))
        assert img is not None, f"Image at '{self.images[index]}' has a problem"
        mask = np.asarray(Image.open(self.masks[index]))

        if self.return_meta:
            return {
                "image": img,
                "mask": mask,
                "meta": {
                    "index": index,
                    "image_path": self.images[index],
                    "mask_path": self.masks[index],
                },
            }

        return {"image": img, "mask": mask}


def setup_data(config: Namespace):
    dataset_train = VOCSegmentationPIL(
        root=config.data_path, year="2012", image_set="train", download=False
    )
    dataset_eval = VOCSegmentationPIL(
        root=config.data_path, year="2012", image_set="val", download=False
    )

    val_img_size = 513
    train_img_size = 480

    mean = (0.485, 0.456, 0.406)
    std = (0.229, 0.224, 0.225)

    transform_train = A.Compose(
        [
            A.RandomScale(
                scale_limit=(0.0, 1.5), interpolation=cv2.INTER_LINEAR, p=1.0
            ),
            A.PadIfNeeded(
                val_img_size, val_img_size, border_mode=cv2.BORDER_CONSTANT
            ),
            A.RandomCrop(train_img_size, train_img_size),
            A.HorizontalFlip(),
            A.Blur(blur_limit=3),
            A.Normalize(mean=mean, std=std),
            ignore_mask_boundaries,
            ToTensor(),
        ]
    )

    transform_eval = A.Compose(
        [
            A.PadIfNeeded(
                val_img_size, val_img_size, border_mode=cv2.BORDER_CONSTANT
            ),
            A.Normalize(mean=mean, std=std),
            ignore_mask_boundaries,
            ToTensor(),
        ]
    )

    dataset_train = TransformedDataset(
        dataset_train, transform_fn=transform_train
    )
    dataset_eval = TransformedDataset(dataset_eval, transform_fn=transform_eval)

    dataloader_train = idist.auto_dataloader(
        dataset_train,
        shuffle=True,
        batch_size=config.train_batch_size,
        num_workers=config.num_workers,
        drop_last=True,
    )
    dataloader_eval = idist.auto_dataloader(
        dataset_eval,
        shuffle=False,
        batch_size=config.train_batch_size,
        num_workers=config.num_workers,
        drop_last=False,
    )

    return dataloader_train, dataloader_eval


def ignore_mask_boundaries(force_apply, **kwargs):
    assert "mask" in kwargs, "Input should contain 'mask'"
    mask = kwargs["mask"]
    mask[mask == 255] = 0
    kwargs["mask"] = mask
    return kwargs


def denormalize(t, mean, std, max_pixel_value=255):
    assert isinstance(t, torch.Tensor), f"{type(t)}"
    assert t.ndim == 3
    d = t.device
    mean = torch.tensor(mean, device=d).unsqueeze(-1).unsqueeze(-1)
    std = torch.tensor(std, device=d).unsqueeze(-1).unsqueeze(-1)
    tensor = std * t + mean
    tensor *= max_pixel_value
    return tensor


def prepare_image_mask(batch, device, non_blocking):
    x, y = batch["image"], batch["mask"]
    x = convert_tensor(x, device, non_blocking=non_blocking)
    y = convert_tensor(y, device, non_blocking=non_blocking).long()
    return x, y


def download_datasets(data_path):
    VOCSegmentation(data_path, image_set="train", download=True)
    VOCSegmentation(data_path, image_set="val", download=True)
