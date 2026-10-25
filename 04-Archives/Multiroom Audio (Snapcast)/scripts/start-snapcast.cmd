@echo off
REM Starts the Snapcast server on demand. Nothing auto-starts at boot.
wsl -d Ubuntu -u root -- bash /mnt/c/snapcast/start-snapcast.sh
