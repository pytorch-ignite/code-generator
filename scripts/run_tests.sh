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
  for dir in $(find ./dist-tests/*-simple -type d)
  do
    cd $dir
    python main.py --data_path ~/data
    cd $CWD
  done
}

run_all() {
  for dir in $(find ./dist-tests/*-all -type d)
  do
    cd $dir
    python main.py --data_path ~/data
    cd $CWD
  done
}

run_launch() {
  for dir in $(find ./dist-tests/*-launch -type d)
  do
    cd $dir
    python -m torch.distributed.launch \
      --nproc_per_node 2 --use_env \
      main.py --backend gloo --data_path ~/data
    cd $CWD
  done
}

run_spawn() {
  for dir in $(find ./dist-tests/*-spawn -type d)
  do
    cd $dir
    python main.py --data_path ~/data \
      --nproc_per_node 2 --backend gloo
    cd $CWD
  done
}

if [ $1 = "unzip" ]; then
  unzip_all
elif [ $1 = "simple" ]; then
  run_simple
elif [ $1 = "all" ]; then
  run_all
elif [ $1 = "launch" ]; then
  run_launch
elif [ $1 = "spawn" ]; then
  run_spawn
fi
