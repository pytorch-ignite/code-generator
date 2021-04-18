#!/bin/bash

set -xeuo pipefail

if [ $1 == "generate" ]; then
    python ./tests/generate.py
elif [ $1 == "unittest" ]; then
    for dir in $(find ./tests/dist -type d -mindepth 1 -maxdepth 1 -not -path "./tests/dist/launch" -not -path "./tests/dist/spawn")
    do
        cd $dir
        pip install -r requirements.txt --progress-bar off -q
        cd ../../../
    done
    for dir in $(find ./tests/dist -type d -mindepth 1 -maxdepth 1 -not -path "./tests/dist/launch" -not -path "./tests/dist/spawn")
    do
        cd $dir
        pytest
        cd ../../../
    done
elif [ $1 == "default" ]; then
    for file in $(find ./tests/dist -iname "main.py" -not -path "./tests/dist/launch/*" -not -path "./tests/dist/spawn/*" -not -path "./tests/dist/single/*")
    do
        if [ $file == "./tests/dist/text_classification/main.py" ]; then
            python $file --verbose --log_every_iters 1 --num_workers 1 --epoch_length 5 --batch_size 16
        else
            python $file --verbose --log_every_iters 2 --num_workers 1 --epoch_length 10
        fi
    done
elif [ $1 == "launch" ]; then
    for file in $(find ./tests/dist/launch -iname "main.py" -not -path "./tests/dist/launch/single/*")
    do
        if [ $file == "./tests/dist/launch/text_classification/main.py" ]; then
            python -m torch.distributed.launch \
                --nproc_per_node 2 \
                --use_env $file \
                --verbose \
                --backend gloo \
                --num_workers 1 \
                --epoch_length 5 \
                --log_every_iters 1
                --batch_size 16
        else
            python -m torch.distributed.launch \
                --nproc_per_node 2 \
                --use_env $file \
                --verbose \
                --backend gloo \
                --num_workers 1 \
                --epoch_length 10 \
                --log_every_iters 2
        fi
    done
elif [ $1 == "spawn" ]; then
    for file in $(find ./tests/dist/spawn -iname "main.py" -not -path "./tests/dist/spawn/single/*")
    do
        if [ $file == "./tests/dist/spawn/text_classification/main.py" ]; then
            python $file \
                --verbose \
                --backend gloo \
                --num_workers 1 \
                --epoch_length 5 \
                --nproc_per_node 2 \
                --log_every_iters 1
                --batch_size 16
        else
            python $file \
                --verbose \
                --backend gloo \
                --num_workers 1 \
                --epoch_length 10 \
                --nproc_per_node 2 \
                --log_every_iters 2
        fi
    done
fi
