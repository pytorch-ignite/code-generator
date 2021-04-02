#!/bin/bash

set -xeu

if [ $(uname) == "Darwin" ]; then
    grep -rl "$1" . | xargs sed -i "" "s/$1/$2/g"
else
    grep -rl "$1" . | xargs sed -i "s/$1/$2/g"
fi
