@echo off
title Art Forge
cd /d "%~dp0"

where py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] The Python launcher "py" is not on PATH.
    echo         Install Python 3.12, then run this again.
    pause
    exit /b 1
)

py -3.12 forge.py
if errorlevel 1 pause
