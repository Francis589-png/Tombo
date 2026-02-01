@echo off
setlocal enabledelayedexpansion

echo Adding Tombo to PATH...
set TOMBO_PATH=C:\Users\FRANCIS JUSU\Documents\TOMBO

REM Add to user PATH
reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "%TOMBO_PATH%;!Path!" /f

echo.
echo ✓ Tombo added to PATH!
echo.
echo Close and reopen PowerShell, then type:
echo   tombo
echo.
pause
