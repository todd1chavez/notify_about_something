#!/bin/bash

export DISPLAY=:0

SCRIPT_DIR="$( cd "$( dirname "$0" )" &> /dev/null && pwd )"

FILENAME="main.py"

PATH_TO_FILE="$SCRIPT_DIR/$FILENAME"

echo "$PATH_TO_FILE"
/usr/bin/env python3 "$PATH_TO_FILE"
