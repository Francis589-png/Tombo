@echo off
REM Tombo Language Interpreter for Windows
REM Run Tombo scripts from command line

cd /d "%~dp0"

if "%1"=="" (
    python tombo.py
) else (
    python tombo.py %1
)
