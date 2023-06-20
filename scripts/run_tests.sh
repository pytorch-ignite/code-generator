#!/usr/bin/env sh

set -xeu

CWD=$(pwd)

unzip_all() {
  for dir in $(find ./dist-tests -type f -iname \*.zip)
  do
    echo $dir
    echo ${dir%.*}
    unzip $dir -d ${dir%.*}
    rm -rf $dir
  done
}

run_simple() {
  for dir in $(find ./dist-tests/$1-simple -type d)
  do
    cd $dir
    python main.py ../../src/tests/ci-configs/$1-simple.yaml
    cd $CWD
  done
}

run_all() {
  for dir in $(find ./dist-tests/$1-all -type d)
  do
    cd $dir
    pytest -vra --color=yes --tb=short test_*.py
    python main.py ../../src/tests/ci-configs/$1-all.yaml
    cd $CWD
  done
}

run_launch() {
  for dir in $(find ./dist-tests/$1-launch -type d)
  do
    cd $dir
    torchrun --nproc_per_node 2 main.py ../../src/tests/ci-configs/$1-launch.yaml --backend gloo
    cd $CWD
  done
}

run_spawn() {
  for dir in $(find ./dist-tests/$1-spawn -type d)
  do
    cd $dir
    python main.py ../../src/tests/ci-configs/$1-spawn.yaml --backend gloo
    cd $CWD
  done
}

if [ $1 = "unzip" ]; then
  unzip_all
elif [ $1 = "simple" ]; then
  run_simple $2
elif [ $1 = "all" ]; then
  run_all $2
elif [ $1 = "launch" ]; then
  run_launch $2
elif [ $1 = "spawn" ]; then
  run_spawn $2
fi
