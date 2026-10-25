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
rem  NOTE: no parenthesised IF blocks below. This folder name contains
rem  parentheses ("Local AI (barebones)"), and cmd.exe misparses a block
rem  whose condition string contains a ")". Use goto instead.
if exist "%EXE%" goto :exe_ok
echo [X] llama-server.exe not found:
echo     %EXE%
echo     See LOCAL_AI_STARTUP.md for the fix.
pause
exit /b 1
:exe_ok

if exist "%MODEL%" goto :model_ok
echo [X] Model file not found:
echo     %MODEL%
pause
exit /b 1
:model_ok

rem --- Port busy? Kill a stale llama-server, otherwise move to a free port ---
rem  (goto-based: no IF blocks, because this folder path has parentheses)
set "HOLDER="
for /f "tokens=5" %%p in ('netstat -aon ^| findstr ":%PORT% " ^| findstr "LISTENING"') do set "HOLDER=%%p"
if not defined HOLDER goto :port_ready

set "OWNER="
for /f "tokens=1 delims=," %%n in ('tasklist /fi "PID eq %HOLDER%" /nh /fo csv 2^>nul') do set "OWNER=%%~n"
echo [!] Port %PORT% is already in use by %OWNER% (PID %HOLDER%).
if /i "%OWNER%"=="llama-server.exe" goto :port_stale

echo     That is not a llama-server process, so it will not be killed.
echo     Looking for the next free port instead.
for /f %%q in ('powershell -NoProfile -Command "$p=8080; while($p -lt 8200){ $t=New-Object Net.Sockets.TcpListener([Net.IPAddress]::Any,$p); try{$t.Start();$t.Stop();break}catch{}; $p++ }; $p"') do set "PORT=%%q"
echo     Using port %PORT% instead (change PORT= above to pin one).
goto :port_ready

:port_stale
choice /c YN /n /m "Kill that stale llama-server? [Y/N] "
if errorlevel 2 exit /b 1
taskkill /f /pid %HOLDER% >nul 2>&1
timeout /t 2 /nobreak >nul

:port_ready

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
echo     "listening on http://%HOST%:%PORT%" line from llama.cpp.
echo.
cd /d "%EXEDIR%"
"%EXE%" -m "%MODEL%" --host %HOST% --port %PORT% --alias %ALIAS% --ctx-size %CTXSZ% --threads %THREADS% --jinja 2>&1 | %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "$input | Tee-Object -FilePath '%LOGFILE%'"

echo.
echo [*] Server stopped. Log saved to: %LOGFILE%
exit /b 0
