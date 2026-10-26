@echo off
title Moto Phone Cleaner
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -STA -File "%~dp0PhoneCleaner.ps1"
