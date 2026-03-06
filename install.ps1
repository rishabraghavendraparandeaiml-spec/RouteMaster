#!/usr/bin/env pwsh
# RouteMaster AI - Automated Installation Script

Write-Host "====== RouteMaster AI - Automated Setup ======" -ForegroundColor Cyan
Write-Host ""

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force | Out-Null

function Write-Status($msg, $status) {
    $color = switch($status) {
        "OK" { "Green" }
        "ERR" { "Red" }
        "WARN" { "Yellow" }
        default { "Cyan" }
    }
    Write-Host "[$status] $msg" -ForegroundColor $color
}

# Check Python
Write-Status "Checking Python..." "INFO"
$pythonExists = $false
try {
    $output = python --version 2>&1
    if ($?) {
        Write-Status "$output found" "OK"
        $pythonExists = $true
    }
} catch {
    $pythonExists = $false
}

if (-not $pythonExists) {
    Write-Host ""
    Write-Status "Installing Python 3.11..." "INFO"
    Write-Host ""
    
    # Try winget
    Write-Status "Attempting winget installation..." "INFO"
    try {
        $result = winget install Python.Python.3.11 -h -e --accept-package-agreements --accept-source-agreements 2>&1
        Start-Sleep -Seconds 3
        $pythonExists = python --version 2>&1
        if ($?) {
            Write-Status "Python installed via winget" "OK"
        }
    } catch {
        Write-Status "Winget failed, trying alternatives..." "WARN"
    }
    
    # Try choco
    if (-not $pythonExists) {
        Write-Status "Attempting Chocolatey installation..." "INFO"
        try {
            $choco = Get-Command choco -ErrorAction SilentlyContinue
            if ($choco) {
                choco install python -y 2>&1 | Out-Null
                Start-Sleep -Seconds 3
                $output = python --version 2>&1
                if ($?) {
                    Write-Status "Python installed via Chocolatey" "OK"
                    $pythonExists = $true
                }
            }
        } catch {
            Write-Status "Chocolatey failed" "WARN"
        }
    }
    
    # Try direct download
    if (-not $pythonExists) {
        Write-Status "Downloading Python installer..." "INFO"
        try {
            [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
            $url = "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe"
            $path = "$env:TEMP\python-3.11.8-amd64.exe"
            
            (New-Object System.Net.WebClient).DownloadFile($url, $path)
            Write-Status "Running installer..." "INFO"
            
            Start-Process -FilePath $path -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
            Start-Sleep -Seconds 3
            
            $output = python --version 2>&1
            if ($?) {
                Write-Status "Python installed successfully" "OK"
                $pythonExists = $true
            }
            Remove-Item $path -Force -ErrorAction SilentlyContinue
        } catch {
            Write-Status "Direct download failed: $_" "ERR"
        }
    }
    
    if (-not $pythonExists) {
        Write-Host ""
        Write-Status "Python installation failed" "ERR"
        Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Status "Installing dependencies..." "INFO"
Write-Host ""

$packages = @(
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "pydantic==2.5.0",
    "python-multipart==0.0.6"
)

foreach ($pkg in $packages) {
    Write-Status "Installing $pkg..." "INFO"
    python -m pip install $pkg --quiet 2>&1 | Out-Null
}

Write-Host ""
Write-Status "Testing installation..." "INFO"
Write-Host ""

python --version
python -m pip --version 2>&1
python -c "import fastapi; print('FastAPI: OK')" 2>&1

Write-Host ""
Write-Host "=========== INSTALLATION COMPLETE ===========" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run: python app.py" -ForegroundColor Yellow
Write-Host "  2. Open: http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
