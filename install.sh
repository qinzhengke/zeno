#!/bin/bash

(crontab -l 2>/dev/null; echo "ZENO_OUTPUT_DIR=/root/zeno_output") | crontab -
(crontab -l 2>/dev/null; echo "LEDGER_DIR=/root/ledger") | crontab -
(crontab -l 2>/dev/null; echo "0 18 * * * bash ~/zeno/collector/run.sh") | crontab -
(crontab -l 2>/dev/null; echo "10 18 * * * bash ~/zeno/analyzer/run.sh") | crontab -
(crontab -l 2>/dev/null; echo "20 18 * * * rclone sync ~/.zeno gdrive: --bwlimit=8.5M --progress") | crontab -
