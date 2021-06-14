#!/bin/bash

set -xeu

if [ $1 == "lint" ]; then
    black . -l 80 --check
    isort . --profile black --check
    flake8 --select F401 .  # find unused imports
elif [ $1 == "fmt" ]; then
    isort . --profile black
    black . -l 80
elif [ $1 == "install" ]; then
    pip install "black==20.8b1" "isort==5.7.0" flake8
fi
