#!/usr/bin/env sh

set -xeu

CWD=$(pwd)


run_simple_fire() {
  for dir in $(find ./dist-tests/$1-simple-fire -type d)
  do
    cd $dir
    python main.py ../../src/tests/ci-configs/$1-simple.yaml
    cd $CWD
  done
}

run_all_fire() {
  for dir in $(find ./dist-tests/$1-all-fire -type d)
  do
    cd $dir
    pytest -vra --color=yes --tb=short test_*.py
    python main.py ../../src/tests/ci-configs/$1-all.yaml
    cd $CWD
  done
}

run_launch_fire() {
  for dir in $(find ./dist-tests/$1-launch-fire -type d)
  do
    cd $dir
    torchrun --nproc_per_node 2 main.py ../../src/tests/ci-configs/$1-launch.yaml --backend gloo
    cd $CWD
  done
}

run_spawn_fire() {
  for dir in $(find ./dist-tests/$1-spawn-fire -type d)
  do
    cd $dir
    python main.py ../../src/tests/ci-configs/$1-spawn.yaml --backend gloo
    cd $CWD
  done
}

if [ $1 = "simple" ]; then
  run_simple_fire $2
elif [ $1 = "all" ]; then
  run_all_fire $2
elif [ $1 = "launch" ]; then
  run_launch_fire $2
elif [ $1 = "spawn" ]; then
  run_spawn_fire $2
fi
