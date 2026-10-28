@echo off
REM Builds the page and creates the zip to copy to the office laptop. Needs Node.js.
title Wish Karo - make release
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0make_release.ps1"
echo.
pause
