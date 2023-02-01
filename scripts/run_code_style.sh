#!/bin/bash

set -xeu

if [ $1 == "lint" ]; then
    ufmt diff .
    flake8 --select F401 .  # find unused imports
elif [ $1 == "fmt" ]; then
    ufmt format .
elif [ $1 == "install" ]; then
    pip install --upgrade "black==21.12b0" "usort==1.0.2" "ufmt==1.3.2" flake8
fi
