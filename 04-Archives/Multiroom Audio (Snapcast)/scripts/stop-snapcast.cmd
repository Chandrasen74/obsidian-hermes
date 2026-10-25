@echo off
REM Stops the Snapcast server and shuts the WSL VM down completely.
wsl -d Ubuntu -u root -- bash -c "systemctl stop snapserver mpd mpd-remote mpd.socket 2>/dev/null; exit 0"
wsl --shutdown
echo Snapcast stopped.
