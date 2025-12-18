@echo off
cd /d "%~dp0"
echo ========================================
echo   AUTO PARTS REQUEST WEBSITE
echo ========================================
echo.
echo Starting server...
echo.
echo Customer Page: http://localhost:5001
echo Admin Panel: http://localhost:5001/admin
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
