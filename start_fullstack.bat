@echo off
echo Starting JSON Comparator Full Stack Application...
echo.

REM Start the FastAPI backend
echo [1/2] Starting FastAPI Backend...
start "FastAPI Backend" cmd /k "cd /d \"%~dp0\" && python main.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start the React frontend
echo [2/2] Starting React Frontend...
start "React Frontend" cmd /k "cd /d \"%~dp0frontend\" && npm start"

echo.
echo Both services are starting...
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:3000
echo.
echo Close this window or press any key to continue...
pause >nul