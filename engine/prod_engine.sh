#!/bin/zsh

# Necessary to first run 'conda activate spotify_3.9'
# This Python virtual environment provides Spotify and OpenAI support.

# The Spotipy library requires the following information. This can be passed directly in the 
# program code but it should be isolated from source code by scripting it as
# shell environment variables.
export SPOTIPY_CLIENT_ID="2f9b6f9f32084d538aa69e74845a759a"
export SPOTIPY_CLIENT_SECRET="723dd34248ee4320b39f79feb23aacdc"
export SPOTIPY_REDIRECT_URI="http://127.0.0.1:8080"

# For api calls to OpenAI to get song information, need the api key in the environment
export OPENAI_API_KEY="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"


# Set the url where the web controller is running so data gathered by
# the engine can be sent to it.
# export WEB_CONTROLLER_URL="http://localhost:8081"
export WEB_CONTROLLER_URL="http://svpserver5.ddns.net:8081"
# export WEB_CONTROLLER_URL="http://192.168.1.162:8081"

python setlist_engine.py
