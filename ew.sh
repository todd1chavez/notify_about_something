#!/usr/bin/zsh

echo "скрипт запущен" >> /tmp/ew_test.log

export DISPLAY=:0

echo "скрипт запущен 1" >> /tmp/ew_test.log

SCRIPT_DIR="$( cd "$( dirname "$0" )" &> /dev/null && pwd )"

FILENAME="main.py"

PATH_TO_FILE="$SCRIPT_DIR/$FILENAME"

echo "скрипт запущен 2" >> /tmp/ew_test.log

echo "$PATH_TO_FILE"
/usr/bin/env python3 "$PATH_TO_FILE"

echo "скрипт запущен 3" >> /tmp/ew_test.log
