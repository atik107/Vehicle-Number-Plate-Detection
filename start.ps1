# Complete Project Startup Script
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Vehicle & Plate Detection System" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "This will start both backend and frontend servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in new window
Write-Host "Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", ".\backend\start.ps1" -WorkingDirectory $PSScriptRoot

# Wait a bit for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Start frontend in new window
Write-Host "Starting Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", ".\frontend\start.ps1" -WorkingDirectory $PSScriptRoot

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Both servers are starting!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend UI: http://localhost:3000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check the new PowerShell windows for logs" -ForegroundColor Yellow
Write-Host "Close those windows to stop the servers" -ForegroundColor Yellow
Write-Host ""
