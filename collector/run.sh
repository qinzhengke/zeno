#!/bin/bash

date=$(date +"%Y%m%d")

mkdir -p ~/.zeno

cd ~/.zeno
folder=log/collector/twitter/basic_collector
mkdir -p ${folder}
python3 ~/zeno/collector/twitter/basic_collector.py > ./${folder}/${date}.txt

cd ~/.zeno
folder=log/collector/cryptorank/basic_collector
mkdir -p ${folder}
python3 ~/zeno/collector/cryptorank/basic_collector.py > ./${folder}/${date}.txt