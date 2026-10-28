@echo off
REM Publishes your changes to GitHub. The office laptop picks them up the next time
REM start_website.bat is started there. Run this on the developer PC (needs Node.js and Git).
title Wish Karo - publish a new version
cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
  echo Git is not installed. Install it from https://git-scm.com and run this again.
  pause
  exit /b
)

git remote get-url origin >nul 2>nul
if not errorlevel 1 goto build

echo This is the first publish.
echo Create an empty PRIVATE repository on github.com first, then copy its address.
set "URL="
set /p "URL=Paste the repository address (https://github.com/...): "
if "%URL%"=="" (
  echo No address given. Nothing was published.
  pause
  exit /b
)
git remote add origin "%URL%"

:build
echo.
echo Building the page...
pushd frontend
if not exist node_modules call npm install
call npm run build
if errorlevel 1 (
  popd
  echo.
  echo The page did not build. Fix the error above, then run publish again. Nothing was published.
  pause
  exit /b
)
popd

git add -A
git diff --cached --quiet
if not errorlevel 1 goto push

echo.
echo Files that changed:
git status --short
echo.
set "MSG="
set /p "MSG=In a few words, what did you change? "
if "%MSG%"=="" set "MSG=Update"
git commit -q -m "%MSG%"

:push
echo.
echo Sending to GitHub (the first time, a GitHub sign-in window may open)...
git push -u origin main
if errorlevel 1 (
  echo.
  echo Could not send it to GitHub. Check the internet connection and sign-in, then run publish again.
  pause
  exit /b
)

echo.
echo Published. The office laptop gets it the next time start_website is opened there.
pause
