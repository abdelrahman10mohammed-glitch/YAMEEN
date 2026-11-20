@echo off
title YAMEEN - Launcher
cd /d "%~dp0"
py main.py
if %ERRORLEVEL% NEQ 0 (
    python main.py
)
pause
