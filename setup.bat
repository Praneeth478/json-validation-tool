@echo off
echo JSON Comparator Setup Script
echo =============================
echo.

echo [1/3] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Installing Node.js dependencies...
cd frontend
if not exist package.json (
    echo ERROR: frontend/package.json not found
    pause
    exit /b 1
)

call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)

cd ..

echo.
echo [3/3] Setup complete!
echo.
echo ✅ Python dependencies installed
echo ✅ Node.js dependencies installed
echo ✅ Ready to start the application
echo.
echo Next steps:
echo   1. Run: start_fullstack.bat (or start_fullstack.ps1)
echo   2. Access Frontend: http://localhost:3000
echo   3. Access Backend API: http://localhost:8000/docs
echo.
pause