#!/bin/bash

# Запустить скрипт в фоновом режиме
# # и сохранить его PID, чтобы при необходимости завершить

SCRIPT_DIR="$( cd "$( dirname "$0" )" &> /dev/null && pwd )"

FILENAME="telegram_bot_for_notify_about_something.py"
PATH_TO_FILE="$SCRIPT_DIR/$FILENAME"

if pgrep -f "$PATH_TO_FILE" > /dev/null
then
  echo "Бот уже запущен"
else
  echo "Запускаем бота"
  /usr/bin/env python3 "$PATH_TO_FILE" &
fi
 

# Можно сохранить PID в файл
# echo $! > telegram_bot.pid
