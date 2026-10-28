@echo off
title Wish Karo Listing Tool
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python is not installed. Install it from https://www.python.org/downloads/
  echo IMPORTANT: tick "Add python.exe to PATH" during install, then run this again.
  pause
  exit /b
)

REM Get the newest published version from GitHub. No internet, or a problem? Start the version we have.
where git >nul 2>nul
if not errorlevel 1 if exist .git (
  echo Checking for a new version...
  git pull --ff-only --quiet
  if errorlevel 1 (
    echo Could not update right now. Starting the version on this PC.
  )
)

REM Install what the tool needs on the first run, and again whenever requirements.txt changes.
fc /b requirements.txt .installed_requirements >nul 2>nul
if errorlevel 1 (
  echo Installing what the tool needs. This takes about a minute...
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo Install failed. Check the internet connection and try again.
    pause
    exit /b
  )
  copy /y requirements.txt .installed_requirements >nul
)

REM Only on a PC that has Node.js (the developer PC): rebuild the page from frontend\src first.
REM The office laptop has no Node.js and simply uses the page that is already built.
where npm >nul 2>nul
if not errorlevel 1 if exist frontend\package.json (
  echo Rebuilding the page...
  pushd frontend
  if not exist node_modules call npm install
  call npm run build
  if errorlevel 1 echo The page could not be rebuilt. Using the last built page.
  popd
)

start "" http://localhost:5050
python app.py
pause
