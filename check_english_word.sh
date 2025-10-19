#!/bin/bash

export DISPLAY=:0

# python3 main.py english_words "$@"

PATH_TO_FILE="/home/me/foo/utility/notify_about_something/main.py"

/usr/bin/env python3 "$PATH_TO_FILE" english_words "$@"
