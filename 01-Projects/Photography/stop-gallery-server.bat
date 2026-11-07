@echo off
setlocal
echo Stopping Photography Gallery Server processes on port 8765 (if any)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8765" ^| findstr "LISTENING"') do (
  echo Killing PID %%a
  taskkill /PID %%a /F >nul 2>nul
)
echo Done.
pause
