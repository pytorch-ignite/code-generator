#!/bin/bash

set -xeu

if [ $1 == "dist_lint" ]; then
    # Check that ./dist-tests/ exists and code is unzipped
    ls ./dist-tests/vision-classification-all/main.py
    # Comment dist-tests in .gitignore to make black running on ./dist-tests folder
    sed -i "s/dist-tests/# dist-tests/g" .gitignore

    ufmt diff .
    flake8 --select F401,F821 ./dist-tests  # find unused imports and non imported objects

    # Restore .gitignore
    sed -i "s/\([# ]\+\)dist-tests/dist-tests/g" .gitignore
elif [ $1 == "source_lint" ]; then
    ufmt diff .
elif [ $1 == "fmt" ]; then
    ufmt format .
elif [ $1 == "install" ]; then
    pip install --upgrade "black==23.3.0" "usort==1.0.6" "ufmt==2.1.0" flake8
fi
