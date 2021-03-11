#!/bin/bash

set -xeu

if [ $1 = "lint" ]; then
    flake8 app templates --max-line-length 120
    isort app templates --check --settings pyproject.toml
    black app templates --check --config pyproject.toml
elif [ $1 = "fmt" ]; then
    isort app templates --color --settings pyproject.toml
    black app templates --config pyproject.toml
elif [ $1 = "install" ]; then
    pip install flake8 "black==19.10b0" "isort==5.7.0"
fi
