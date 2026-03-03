#!/usr/bin/zsh

export DISPLAY=:0

SCRIPT_DIR="$( cd "$( dirname "$0" )" &> /dev/null && pwd )"

FILENAME="main.py"
FILENAME1="start_telegram_bot_for_notify_about_something.sh"

PATH_TO_FILE="$SCRIPT_DIR/$FILENAME"
PATH_TO_FILE1="$SCRIPT_DIR/$FILENAME1"

bash $PATH_TO_FILE1

/usr/bin/env python3 "$PATH_TO_FILE"
