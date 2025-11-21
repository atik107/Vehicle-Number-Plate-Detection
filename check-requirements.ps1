# System Check Script
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "System Requirements Check" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Python
Write-Host "Checking Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -ge 3 -and $minor -ge 8) {
            Write-Host " ✓ $pythonVersion" -ForegroundColor Green
        } else {
            Write-Host " ✗ Python 3.8+ required" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    $allGood = $false
}

# Check Node.js
Write-Host "Checking Node.js..." -NoNewline
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "v(\d+)") {
        $major = [int]$matches[1]
        if ($major -ge 16) {
            Write-Host " ✓ $nodeVersion" -ForegroundColor Green
        } else {
            Write-Host " ✗ Node.js 16+ required" -ForegroundColor Red
            $allGood = $false
        }
    }
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    $allGood = $false
}

# Check npm
Write-Host "Checking npm..." -NoNewline
try {
    $npmVersion = npm --version 2>&1
    Write-Host " ✓ v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    $allGood = $false
}

# Check pip
Write-Host "Checking pip..." -NoNewline
try {
    $pipVersion = pip --version 2>&1
    if ($pipVersion -match "pip (\d+\.\d+)") {
        Write-Host " ✓ $($matches[1])" -ForegroundColor Green
    } else {
        Write-Host " ✓ Installed" -ForegroundColor Green
    }
} catch {
    Write-Host " ✗ Not found" -ForegroundColor Red
    $allGood = $false
}

# Check disk space
Write-Host "Checking disk space..." -NoNewline
$drive = (Get-Location).Drive
$freeSpace = (Get-PSDrive $drive.Name).Free / 1GB
if ($freeSpace -gt 0.5) {
    Write-Host " ✓ $([math]::Round($freeSpace, 2)) GB available" -ForegroundColor Green
} else {
    Write-Host " ⚠ Low disk space: $([math]::Round($freeSpace, 2)) GB" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✓ All requirements met!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Cyan
    Write-Host "  .\start.ps1" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "✗ Some requirements are missing" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install:" -ForegroundColor Yellow
    Write-Host "  - Python 3.8+: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  - Node.js 16+: https://nodejs.org/" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
