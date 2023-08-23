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

# Python-Argparser functions

run_simple() {
  for dir in $(find ./dist-tests/$1-simple-argparse -type d)
  do
    cd $dir
    python main.py ../../src/tests/ci-configs/$1-simple.yaml
    cd $CWD
  done
}

run_all() {
  for dir in $(find ./dist-tests/$1-all-argparse -type d)
  do
    cd $dir
    pytest -vra --color=yes --tb=short test_*.py
    python main.py ../../src/tests/ci-configs/$1-all.yaml
    cd $CWD
  done
}

run_launch() {
  for dir in $(find ./dist-tests/$1-launch-argparse -type d)
  do
    cd $dir
    torchrun --nproc_per_node 2 main.py ../../src/tests/ci-configs/$1-launch.yaml --backend gloo
    cd $CWD
  done
}

run_spawn() {
  for dir in $(find ./dist-tests/$1-spawn-argparse -type d)
  do
    cd $dir
    python main.py ../../src/tests/ci-configs/$1-spawn.yaml --backend gloo
    cd $CWD
  done
}

# Python-fire functions

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


if [ $1 = "unzip" ]; then
  unzip_all
elif [ $1 = "simple" ]; then
  if [ $3 = "argparse" ]; then 
    run_simple $2
  elif [ $3 = "fire" ]; then 
    run_simple_fire $2
  fi
elif [ $1 = "all" ]; then
  if [ $3 = "argparse" ]; then 
    run_all $2
  elif [ $3 = "fire" ]; then 
    run_all_fire $2
  fi
elif [ $1 = "launch" ]; then
  if [ $3 = "argparse" ]; then 
    run_launch $2
  elif [ $3 = "fire" ]; then 
    run_launch_fire $2
  fi
elif [ $1 = "spawn" ]; then
  if [ $3 = "argparse" ]; then 
    run_spawn $2
  elif [ $3 = "fire" ]; then 
    run_spawn_fire $2
  fi
fi
