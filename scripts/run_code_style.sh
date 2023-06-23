#!/bin/bash

set -xeu

if [ $1 == "lint" ]; then
    # Check that ./dist-tests/ exists and code is unzipped
    ls ./dist-tests/vision-classification-all/main.py
    ufmt diff .
    flake8 --select F401 ./dist-tests  # find unused imports
elif [ $1 == "min_lint" ]; then
    ufmt diff .
elif [ $1 == "fmt" ]; then
    ufmt format .
elif [ $1 == "install" ]; then
    pip install --upgrade "black==23.3.0" "usort==1.0.6" "ufmt==2.1.0" flake8
fi
