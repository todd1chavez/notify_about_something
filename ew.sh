#!/usr/bin/bash

export DISPLAY=:0

SCRIPT_DIR="$( cd "$( dirname "$0" )" &> /dev/null && pwd )"

FILENAME="main.py"
FILENAME1="start_telegram_bot_for_notify_about_something.sh"
FILENAME2="temporary_data_for_script"

PATH_TO_FILE="$SCRIPT_DIR/$FILENAME"
PATH_TO_FILE1="$SCRIPT_DIR/$FILENAME1"
PATH_TO_FILE2="$SCRIPT_DIR/$FILENAME2"


current_minutes=$(date +%M)
previous_launch_time=$(cat "$PATH_TO_FILE2" 2>/dev/null)


execute_script() {
  previous_launch_time=$(date +%M)
  echo "$previous_launch_time" > "$PATH_TO_FILE2"
  bash $PATH_TO_FILE1
  /root/notify_about_something/venv/bin/python "$PATH_TO_FILE"
}

execute_script

if [ "$(wc -c <"$PATH_TO_FILE2")" -eq 1 ] || [ "$(wc -c <"$PATH_TO_FILE2")" -eq 0 ]; then
  execute_script
elif [ "$current_minutes" -eq 0 ] && [ "$previous_launch_time" -eq 15 ]; then
  execute_script
elif [ "$current_minutes" -eq 15 ] && [ "$previous_launch_time" -eq 30 ]; then
  execute_script
elif [ "$current_minutes" -eq 30 ] && [ "$previous_launch_time" -eq 45 ]; then
  execute_script
elif [ "$current_minutes" -eq 45 ] && [ "$previous_launch_time" -eq 0 ]; then
  execute_script
fi
