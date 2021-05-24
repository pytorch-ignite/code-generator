from torchvision import datasets

datasets.MNIST("~/data", train=True, download=True)
datasets.MNIST("~/data", train=False, download=True)

datasets.VOCSegmentation(
    "~/data", year="2012", image_set="train", download=True
)
