from torchvision import datasets

datasets.CIFAR10("~/data", train=True, download=True)
datasets.CIFAR10("~/data", train=False, download=True)

datasets.VOCSegmentation("~/data", year="2012", image_set="train", download=True)
