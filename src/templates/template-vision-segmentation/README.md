[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# Segmentation Template

This is the segmentation template by Code-Generator using `deeplabv3_resnet101` and `cifar10` dataset from TorchVision and training is powered by PyTorch and PyTorch-Ignite.

**Note:**
The dataset used in this template is quite substantial, with a size of several GBs and automatically downloading it can be seen as an unexpected behaviour. To prevent unexpected behavior or excessive bandwidth usage, the automatic downloading of the dataset has been disabled by default.

To download the dataset:

```python
python -c "from data import download_datasets; download_datasets('/path/to/data')"
```

or

```py
from data import download_datasets
download_datasets('/path/to/data')
```

#::= from_template_common ::#
