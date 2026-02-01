# Tombo Language - Simplest Installation (PowerShell)
# One-command install

Write-Host ""
Write-Host "========================================"
Write-Host "  TOMBO LANGUAGE INSTALLER" -ForegroundColor Green
Write-Host "========================================"
Write-Host ""

# Check Python
Write-Host "[1/3] Checking Python..." -ForegroundColor Cyan
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python 3.11+ not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host $pythonCheck

# Upgrade pip
Write-Host ""
Write-Host "[2/3] Upgrading pip..." -ForegroundColor Cyan
pip install -q --upgrade pip setuptools wheel

# Install Tombo
Write-Host ""
Write-Host "[3/3] Installing Tombo..." -ForegroundColor Cyan
pip install -e . *>$null

Write-Host ""
Write-Host "========================================"
Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "========================================"
Write-Host ""
Write-Host "To use Tombo:" -ForegroundColor Yellow
Write-Host "  python tombo.py"
Write-Host ""
Write-Host "Or in Python:"
Write-Host "  from src.core.interpreter import Interpreter"
Write-Host "  interp = Interpreter()"
Write-Host ""
Read-Host "Press Enter to exit"
