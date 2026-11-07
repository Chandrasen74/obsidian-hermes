@echo off
REM Photography pipeline - all scripts live here permanently (temp folder gets cleaned)
REM Order: organize -> index -> gallery -> gemini descriptions
set PY=C:\Python314\python.exe
set T=C:\Users\Kanchan Verma\OneDrive\Desktop\Opencode\01-Projects\photography-pipeline

echo [1/4] Organizing photography folder...
"%PY%" -W ignore "%T%\organize_photos.py"
if errorlevel 1 (echo Organize FAILED - stopping.& pause& exit /b 1)

echo [2/4] Building photo index...
"%PY%" -W ignore "%T%\photo_index.py"
if errorlevel 1 (echo Index FAILED - stopping.& pause& exit /b 1)

echo [3/4] Building gallery...
"%PY%" -W ignore "%T%\build_gallery.py"
if errorlevel 1 (echo Gallery FAILED - stopping.& pause& exit /b 1)

echo [4/4] Gemini description queue (stops cleanly when the daily quota is used, resumable)...
if not exist "%T%\gemini_key.txt" (
  echo No Gemini key file found - skipping descriptions. Gallery works without them.
) else (
  "%PY%" -W ignore "%T%\gemini_describe.py"
)

echo.
echo PIPELINE COMPLETE. Gallery: OneDrive\Desktop\photography\gallery.html
pause
