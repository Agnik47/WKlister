@echo off
REM Developer mode (needs Node.js). Save a file and the page rebuilds by itself:
REM   frontend\src\*   -> the page is rebuilt in about a second, refresh the browser
REM   *.py             -> the server restarts by itself
title Wish Karo - developer mode
cd /d "%~dp0"

where npm >nul 2>nul
if errorlevel 1 (
  echo Developer mode needs Node.js. Install it from https://nodejs.org and run this again.
  pause
  exit /b
)

if not exist frontend\node_modules (
  pushd frontend
  call npm install
  popd
)

start "Page rebuild - leave open" cmd /k "cd /d %~dp0frontend && npm run watch"
start "" http://localhost:5050
set DEV=1
python app.py
pause
