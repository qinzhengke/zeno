#!/bin/bash

date=$(date +"%Y%m%d")

mkdir -p ${ZENO_OUTPUT_DIR}

cd ${ZENO_OUTPUT_DIR}
folder=log/analyzer/basic_plotter
mkdir -p ${folder}
python3 ~/zeno/analyzer/basic_plotter.py > ./${folder}/${date}.txt

# Update the ledger, should clone ledger project first.
cd ${LEDGER_DIR}
git remote update
git reset --hard origin/main

cd ${ZENO_OUTPUT_DIR}
folder=log/analyzer/blance
mkdir -p ${folder}
python3 ~/zeno/analyzer/blance.py ${LEDGER_DIR} > ./${folder}/${date}.txt

cd ${ZENO_OUTPUT_DIR}
folder=log/analyzer/twitter
mkdir -p ${folder}
python3 ~/zeno/analyzer/twitter_rank.py > ./${folder}/${date}.txt
