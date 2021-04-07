#!/bin/bash

set -xeu

if [ $1 == "generate" ]; then
    python ./tests/generate.py
elif [ $1 == "unittest" ]; then
    for dir in $(find ./tests/dist -type d -mindepth 1 -maxdepth 1)
    do
        cd $dir
        pip install -r requirements.txt --progress-bar off -q
        cd ../../../
    done
    for dir in $(find ./tests/dist -type d -mindepth 1 -maxdepth 1)
    do
        cd $dir
        pytest test_all.py -vra --color=yes --durations=0
        cd ../../../
    done
elif [ $1 == "integration" ]; then
    for file in $(find ./tests/integration -iname "*.sh")
    do
        bash $file
    done
fi
