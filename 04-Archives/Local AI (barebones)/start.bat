@echo off
setlocal EnableExtensions
title START AI - Qwen3.5-9B llama.cpp server
chcp 65001 >nul

rem ============================================================
rem  One-file startup: barebones llama.cpp server for Qwen3.5-9B
rem  - Chat UI:  http://127.0.0.1:8080            (opens in browser)
rem  - API:      http://127.0.0.1:8080/v1         (OpenAI-compatible)
rem  - Stop: Ctrl+C here (then Y), or just close this window
rem  - Output: live in THIS window, saved to logs\llama_server.log
rem ============================================================

rem --- Paths and settings (edit here) ---
set "ROOT=%~dp0"
set "EXEDIR=%ROOT%llama.cpp\build\bin\Release"
set "EXE=%EXEDIR%\llama-server.exe"
set "MODEL=%USERPROFILE%\.lmstudio\models\lmstudio-community\Qwen3.5-9B-GGUF\Qwen3.5-9B-Q4_K_M.gguf"
set "HOST=127.0.0.1"
set "PORT=8080"
set "ALIAS=qwen3.5-9b"
set "CTXSZ=8192"
set "THREADS=6"
set "LOGDIR=%ROOT%logs"
set "LOGFILE=%LOGDIR%\llama_server.log"

rem --- Sanity checks ---
if not exist "%EXE%" (
  echo [X] llama-server.exe not found:
  echo     %EXE%
  echo     See LOCAL_AI_STARTUP.md for the fix.
  pause
  exit /b 1
)
if not exist "%MODEL%" (
  echo [X] Model file not found:
  echo     %MODEL%
  pause
  exit /b 1
)

rem --- Port busy? Offer to kill a stale server ---
set "BUSY=0"
for /f "tokens=5" %%p in ('netstat -aon ^| findstr ":%PORT% " ^| findstr "LISTENING"') do if not "%%p"=="0" set "BUSY=1"
if "%BUSY%"=="1" (
  echo [!] Port %PORT% is already in use.
  choice /c YN /n /m "[Y] kill stale llama-server.exe  [N] quit:  "
  if errorlevel 2 exit /b 1
  taskkill /f /im llama-server.exe >nul 2>&1
  timeout /t 2 /nobreak >nul
)

rem --- Rotate old log ---
if not exist "%LOGDIR%" mkdir "%LOGDIR%"
if exist "%LOGFILE%" move /y "%LOGFILE%" "%LOGDIR%\llama_server.old.log" >nul

echo.
echo [*] Chat UI : http://%HOST%:%PORT%   (browser opens, tab may
echo               show a load error until the model finishes loading)
echo [*] API     : http://%HOST%:%PORT%/v1
echo [*] Model   : %ALIAS%  (ctx %CTXSZ%, threads %THREADS%)
echo [*] Log     : %LOGFILE%  (also streamed live below)
echo.

start "" http://%HOST%:%PORT%

echo [*] Starting server in THIS window. Ready when you see the
echo     "listening on http://127.0.0.1:8080" line from llama.cpp.
echo.
cd /d "%EXEDIR%"
"%EXE%" -m "%MODEL%" --host %HOST% --port %PORT% --alias %ALIAS% --ctx-size %CTXSZ% --threads %THREADS% --jinja 2>&1 | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "$input | Tee-Object -FilePath '%LOGFILE%'"

echo.
echo [*] Server stopped. Log saved to: %LOGFILE%
exit /b 0
