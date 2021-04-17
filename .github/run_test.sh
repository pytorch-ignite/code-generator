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
        python $file --verbose --log_every_iters 2 --num_workers 0 --epoch_length 10
    done
elif [ $1 == "launch" ]; then
    for file in $(find ./tests/dist/launch -iname "main.py" -not -path "./tests/dist/*" -not -path "./tests/dist/spawn/*" -not -path "./tests/dist/launch/single/*")
    do
        python -m torch.distributed.launch --nproc_per_node 2 $file --verbose --log_every_iters 2 --num_workers 0 --epoch_length 10
    done
elif [ $1 == "spawn" ]; then
    for file in $(find ./tests/dist/spawn -iname "main.py" -not -path "./tests/dist/launch/*" -not -path "./tests/dist/*" -not -path "./tests/dist/spawn/single/*")
    do
        python $file --verbose --log_every_iters 2 --num_workers 0 --epoch_length 10 --nproc_per_node 2
    done
fi
