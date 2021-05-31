from torchvision.models.segmentation import deeplabv3_resnet101


def setup_model(config):
    return deeplabv3_resnet101(num_classes=config.num_classes)
