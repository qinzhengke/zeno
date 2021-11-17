#!/bin/bash

mkdir -p ~/.zeno

cd /root/.zeno/tfc_analyzer
node /root/zeno/analyzer/main.mjs > log.txt
