#!/bin/bash

date=$(date +"%Y%m%d")

cd ~/.zeno/tfc_collector
node ~/zeno/collector/main.mjs > log.txt
cd ~/.zeno
mkdir -p log/cryptorank/basic_collector
python3 ~/zeno/collector/cryptorank/basic_collector.py > ./log/cryptorank/basic_collector/${date}.txt