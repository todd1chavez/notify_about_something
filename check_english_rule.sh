#!/bin/bash

export DISPLAY=:0

PATH_TO_FILE="/home/me/foo/utility/notify_about_something/main.py"

/usr/bin/env python3 "$PATH_TO_FILE" english_rules "$@"
