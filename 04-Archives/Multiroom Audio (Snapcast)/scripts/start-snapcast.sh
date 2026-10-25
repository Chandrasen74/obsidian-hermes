#!/bin/bash
# Brings the Snapcast stack up on demand. Nothing here is enabled at boot.
set -e
systemctl start snapserver mpd mpd-remote
sleep 1
# Guarantee silence until someone presses play
mpc stop 2>/dev/null || true
echo "snapserver: $(systemctl is-active snapserver)"
echo "mpd:       $(systemctl is-active mpd)"
echo "remote:    $(systemctl is-active mpd-remote)"
