#!/usr/bin/env bash

# Append current timestamp to a log file in home directory
LOGFILE="$HOME/ha_remote_commands.log"
echo "Remote command executed at $(date)" >> "$LOGFILE"