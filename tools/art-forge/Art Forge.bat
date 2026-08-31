@echo off
title Art Forge
cd /d "%~dp0"

set "FORGE_PY="

where python >nul 2>&1
if not errorlevel 1 (
    python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1
    if not errorlevel 1 set "FORGE_PY=python"
)

if not defined FORGE_PY (
    where py >nul 2>&1
    if not errorlevel 1 (
        py -3.12 -c "import sys" >nul 2>&1
        if not errorlevel 1 set "FORGE_PY=py -3.12"
    )
)

if not defined FORGE_PY (
    echo [ERROR] Python 3.12 or newer was not found.
    echo         Install 64-bit Python and enable "Add Python to PATH", then retry.
    echo         You can also run: python forge.py
    pause
    exit /b 1
)

%FORGE_PY% forge.py
if errorlevel 1 pause
