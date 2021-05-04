### imports ###
from torch import nn


### get_model ###
def get_model(name: str) -> nn.Module:
    from torchvision import models

    if name in models.__dict__:
        fn = models.__dict__[name]
    else:
        raise RuntimeError(f"Unknown model name {name}")

    return fn()
