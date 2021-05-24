#!/usr/bin/env sh

set -eu

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

unzip_all
run_simple
