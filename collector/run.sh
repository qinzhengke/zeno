#!/bin/bash

date=$(date +"%Y%m%d")

mkdir -p ${ZENO_OUTPUT_DIR}

cd ${ZENO_OUTPUT_DIR}
folder=log/collector/twitter/basic_collector
mkdir -p ${folder}
python3 ~/zeno/collector/twitter/basic_collector.py > ./${folder}/${date}.txt

cd ${ZENO_OUTPUT_DIR}
folder=log/collector/cryptorank/basic_collector
mkdir -p ${folder}
python3 ~/zeno/collector/cryptorank/basic_collector.py > ./${folder}/${date}.txt

cd ${ZENO_OUTPUT_DIR}
folder=log/collector/cryptorank/global_collector
mkdir -p ${folder}
python3 ~/zeno/collector/cryptorank/global_collector.py > ./${folder}/${date}.txt

cd ${ZENO_OUTPUT_DIR}
folder=log/collector/alternative/fng_collector
mkdir -p ${folder}
python3 ~/zeno/collector/alternative/fng_collector.py > ./${folder}/${date}.txt

cd ${ZENO_OUTPUT_DIR}
folder=log/collector/alternative/ticker_collector
mkdir -p ${folder}
python3 ~/zeno/collector/alternative/ticker_collector.py > ./${folder}/${date}.txt
