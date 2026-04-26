# JSON Comparator Full Stack Startup Script

Write-Host "Starting JSON Comparator Full Stack Application..." -ForegroundColor Green
Write-Host ""

# Start the FastAPI backend
Write-Host "[1/2] Starting FastAPI Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python main.py"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start the React frontend
Write-Host "[2/2] Starting React Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm start"

Write-Host ""
Write-Host "Both services are starting..." -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend UI: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")