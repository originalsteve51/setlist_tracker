#!/bin/bash

# Use the spotify_3.9 conda environment and run the program passed as an argument
conda run -n spotify_3.9 --live-stream ./$1
