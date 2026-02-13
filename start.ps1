# Multi-Disease Risk Analytics Platform
# Quick Installation and Run Script

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Multi-Disease Risk Analytics Platform" -ForegroundColor Cyan  
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
    
    Write-Host "Installing/Updating dependencies..." -ForegroundColor Yellow
    pip install --quiet -r requirements.txt
    
    Write-Host ""
    Write-Host "✓ Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting Flask application..." -ForegroundColor Yellow
    Write-Host "Access the app at: http://localhost:5000" -ForegroundColor Cyan
    Write-Host ""
    
    python run.py
    
} else {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
    
    Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    Write-Host ""
    Write-Host "✓ Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Starting Flask application..." -ForegroundColor Yellow
    Write-Host "Access the app at: http://localhost:5000" -ForegroundColor Cyan
    Write-Host ""
    
    python run.py
}
