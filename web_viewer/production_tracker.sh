#!/bin/bash

# Script to run on my Raspberry Pi server

# RUN_ON_HOST:USING_PORT forms the URL where JavaScript posts are directed
# This specifies how a browser outside my internal network calls my Raspberry Pi
# server. A hostname from NOIP is configured to allow outside callers. A port
# number that is configured to be forwarded by my Netgear router is specified.
export RUN_ON_HOST="svpserver5.ddns.net"
export USING_PORT="8081"
export DEBUG_MODE=True


# Program execution using nohup (no hang up) to permit running even after the
# command shell closes. It keeps running in the background because of trailing &.
# Stdout and stderr streams are redirected to file web_ctl.log
# I have configured this for invocation from rc.local at boot time.
nohup python /home/stephenharding/my_code/python/setlist_web/setlist_web.py > trkr_web_ctl.log 2>&1  &
