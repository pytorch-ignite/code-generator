from argparse import ArgumentParser

import torch

from ignite.handlers import DiskSaver


def thresholded_output_transform(output):
    y_pred, y = output
    return torch.round(torch.sigmoid(y_pred)), y


def get_save_handler(config):
    if config.with_clearml:
        from ignite.contrib.handlers.clearml_logger import ClearMLSaver

        return ClearMLSaver(dirname=config.output_path)

    return DiskSaver(config.output_path, require_empty=False)


def get_default_parser(defaults):
    parser = ArgumentParser(add_help=False)

    for key, value in defaults.items():
        parser.add_argument(f"--{key}", **value)

    return parser
