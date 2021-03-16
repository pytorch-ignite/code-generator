#!/bin/bash

set -xeu

if [ $1 = "generate" ]; then
    python ./tests/generate.py
elif [ $1 = "unittest" ]; then
    pytest ./tests/unittest -vvv -ra --color=yes --durations=0
elif [ $1 = "integration" ]; then
    for file in $(find ./tests/integration -iname "*.sh")
    do
        bash $file
    done
fi
