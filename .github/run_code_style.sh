#!/bin/bash

set -xeu

if [ $1 == "lint" ]; then
    flake8 app templates/*/_sidebar.py tests --config .flake8
    isort app templates/*/_sidebar.py tests --check --settings pyproject.toml
    black app templates/*/_sidebar.py tests --check --config pyproject.toml
elif [ $1 == "fmt" ]; then
    isort app templates/*/_sidebar.py tests --color --settings pyproject.toml
    black app templates/*/_sidebar.py tests --config pyproject.toml
elif [ $1 == "install" ]; then
    pip install flake8 "black==20.8b1" "isort==5.7.0"
fi
