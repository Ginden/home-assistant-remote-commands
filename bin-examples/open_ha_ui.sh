#!/usr/bin/env bash

# Open Home Assistant UI in default browser
URL="http://homeassistant.local:8123"
if [[ "$(uname)" == "Darwin" ]]; then
  open "$URL"
else
  xdg-open "$URL"
fi