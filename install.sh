#!/bin/bash

(crontab -l 2>/dev/null; echo "0 18 * * * bash ~/zeno/collector/run.sh") | crontab -
(crontab -l 2>/dev/null; echo "5 18 * * * rclone sync ~/.zeno gdrive: --bwlimit=8.5M --progress") | crontab -
