# from https://github.com/pytorch/ignite/blob/master/setup.py

import io
import os

from setuptools import find_packages, setup

VERSION = "0.1.0"


def read(*names, **kwargs):
    with io.open(os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def dependencies(fname):
    with open(fname, "r") as f:
        return [dep.replace("\n", "") for dep in f.readlines()]


readme = read("README.md")

requirements = dependencies("requirements.txt")

setup(
    # Metadata
    name="{{ project_name }}",
    version=VERSION,
    long_description_content_type="text/markdown",
    long_description=readme,
    license="MIT",
    # Package info
    packages=find_packages(
        exclude=(
            "tests",
            "tests.*",
        )
    ),
    zip_safe=True,
    install_requires=requirements,
)
