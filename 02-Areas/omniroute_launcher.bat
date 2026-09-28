@echo off
REM Omniroute Launcher for Second Brain
REM Backup command stored in "omniroute startup.txt"

echo Starting Omniroute Second Brain...
echo.

REM Execute omniroute with logging
omniroute --log

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit.
    pause >nul
)
