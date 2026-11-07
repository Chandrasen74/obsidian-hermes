@echo off
setlocal
cd /d "%~dp0"

set "PY=C:\Python314\python.exe"
if not exist "%PY%" set "PY=python"

if not exist "gallery-server\config.json" (
  echo Creating gallery-server\config.json from example...
  copy /Y "gallery-server\config.example.json" "gallery-server\config.json" >nul
  echo.
  echo IMPORTANT: Edit gallery-server\config.json and set a strong TOKEN before using on LAN/Tailscale.
  echo Then run this script again.
  echo.
  pause
  exit /b 1
)

if not exist "gallery-server\.venv\Scripts\python.exe" (
  echo Creating virtual environment...
  "%PY%" -m venv "gallery-server\.venv"
  if errorlevel 1 (
    echo Failed to create venv.
    pause
    exit /b 1
  )
)

echo Installing/updating server dependencies (first run may take a minute)...
"gallery-server\.venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r "gallery-server\requirements.txt"
if errorlevel 1 (
  echo Dependency install failed.
  pause
  exit /b 1
)

echo.
echo Starting Photography Gallery Server (Phase 1)...
echo Press Ctrl+C to stop.
echo.
"gallery-server\.venv\Scripts\python.exe" "gallery-server\server.py"
if errorlevel 1 pause
