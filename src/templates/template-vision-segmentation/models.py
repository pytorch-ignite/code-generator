from torchvision.models.segmentation import deeplabv3_resnet50


def setup_model(config):
    return deeplabv3_resnet50(num_classes=config.num_classes)
