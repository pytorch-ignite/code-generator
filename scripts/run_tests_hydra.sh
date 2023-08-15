#!/usr/bin/env sh

set -xeu

CWD=$(pwd)


run_simple_hydra() {
  for dir in $(find ./dist-tests/$1-simple-hydra -type d)
  do
    cd $dir
    python main.py --config-dir=../../src/tests/ci-configs --config-name=$1-simple.yaml 
    cd $CWD
  done
}

run_all_hydra() {
  for dir in $(find ./dist-tests/$1-all-hydra -type d)
  do
    cd $dir
    pytest -vra --color=yes --tb=short test_*.py
    python main.py --config-dir=../../src/tests/ci-configs --config-name=$1-all.yaml
    cd $CWD
  done
}

run_launch_hydra() {
  for dir in $(find ./dist-tests/$1-launch-hydra -type d)
  do
    cd $dir
    torchrun --nproc_per_node 2 main.py --config-dir=../../src/tests/ci-configs --config-name=$1-launch.yaml ++backend='gloo'
    cd $CWD
  done
}

run_spawn_hydra() {
  for dir in $(find ./dist-tests/$1-spawn-hydra -type d)
  do
    cd $dir
    python main.py --config-dir=../../src/tests/ci-configs --config-name=$1-spawn.yaml ++backend='gloo'
    cd $CWD
  done
}

elif [ $1 = "simple" ]; then
  run_simple_hydra $2
elif [ $1 = "all" ]; then
  run_all_hydra $2
elif [ $1 = "launch" ]; then
  run_launch_hydra $2
elif [ $1 = "spawn" ]; then
  run_spawn_hydra $2
fi
