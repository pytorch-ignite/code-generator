"""
Generates the metadata used in the sidebar of template configurations.
The goal is to make Code-Generator free of pytorch and its related libraries free
when running the app on streamlit.
"""

import json

from torchvision import models

METADATA_FILEPATH = "./templates/image_classification/metadata.json"


def generate_classi_model_names():
    """Generate image classification models from torchvision."""
    names = []
    for k in models.__dict__.keys():
        if (
            not k.startswith("_")
            and not k[0].istitle()
            and k not in ["utils", "segmentation", "detection", "video", "quantization"]
        ):
            names.append(k)
    obj = {"model_name": names}
    with open(METADATA_FILEPATH, "w") as fp:
        json.dump(obj, fp)


if __name__ == "__main__":
    generate_classi_model_names()
