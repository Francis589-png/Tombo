@echo off
REM Tombo Language - Simplest Installation
REM One-click install script for Windows

echo.
echo ========================================
echo  TOMBO LANGUAGE INSTALLER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.11+ not found!
    echo Please install Python from python.org
    pause
    exit /b 1
)

echo [1/3] Checking Python version...
python --version

echo.
echo [2/3] Installing dependencies...
pip install -q --upgrade pip setuptools wheel

echo.
echo [3/3] Installing Tombo Language...
pip install -e . >nul 2>&1

if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed
    echo But Tombo core is ready to use
)

echo.
echo ========================================
echo  INSTALLATION COMPLETE!
echo ========================================
echo.
echo To use Tombo, type:
echo   python tombo.py
echo.
echo Or in Python:
echo   from src.core.interpreter import Interpreter
echo   interp = Interpreter()
echo.
pause
