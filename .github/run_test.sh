#!/bin/bash

set -xeu

if [ $1 = "generate" ]; then
    python ./tests/templates/gen_image_classification.py
elif [ $1 = "unittest" ]; then
    pytest ./tests/unittest -vvv -ra --color=yes --durations=0
elif [ $1 = "integration" ]; then
    cd ./tests/templates/dist/image_classification
    python main.py --verbose
fi
