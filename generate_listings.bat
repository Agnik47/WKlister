@echo off
REM Drag your filled master Excel file onto this file.
cd /d "%~dp0"
if "%~1"=="" (
  echo Drag the filled master sheet onto this file.
  pause
  exit /b
)
python generate.py "%~1" "%~dp1Listing_Output"
echo.
echo Files are in: %~dp1Listing_Output
pause
