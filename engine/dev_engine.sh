#!/bin/zsh

# Necessary to first run 'conda activate spotify_3.9'
# This Python virtual environment provides Spotify and OpenAI support.



# Set the url where the web controller is running so data gathered by
# the engine can be sent to it.
export WEB_CONTROLLER_URL="http://localhost:8081"
# export WEB_CONTROLLER_URL="http://svpserver5.ddns.net:8081"
# export WEB_CONTROLLER_URL="http://192.168.1.162:8080"

python setlist_engine.py
