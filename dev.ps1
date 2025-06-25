# PowerShell script for FINDSYM development tasks

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Write-Header {
    param([string]$Message)
    Write-Host "`n=== $Message ===" -ForegroundColor Green
}

function Invoke-DevCommand {
    param(
        [string]$Cmd,
        [string]$Description
    )
    Write-Header $Description
    Write-Host "Running: $Cmd" -ForegroundColor Yellow
    
    $result = cmd /c $Cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Command failed with return code $LASTEXITCODE" -ForegroundColor Red
        return $false
    }
    return $true
}

function Clean {
    Write-Header "Cleaning build artifacts"
    
    # Remove build directories
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    Get-ChildItem -Path . -Filter "*.egg-info" -Directory | Remove-Item -Recurse -Force
    
    # Remove Python cache files
    Get-ChildItem -Path . -Name "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Name "*.pyc" -Recurse | Remove-Item -Force
    
    Write-Host "Cleanup completed" -ForegroundColor Green
}

function Format-Code {
    Invoke-DevCommand "black findsym/ examples/ test_*.py" "Formatting with black"
    Invoke-DevCommand "isort findsym/ examples/ test_*.py" "Sorting imports with isort"
}

function Test-Lint {
    $success = $true
    
    if (-not (Invoke-DevCommand "flake8 findsym/ examples/ test_*.py" "Running flake8")) {
        $success = $false
    }
    
    if (-not (Invoke-DevCommand "black --check findsym/ examples/ test_*.py" "Checking black formatting")) {
        $success = $false
    }
    
    if (-not (Invoke-DevCommand "isort --check-only findsym/ examples/ test_*.py" "Checking import sorting")) {
        $success = $false
    }
    
    return $success
}

function Test-Package {
    return Invoke-DevCommand "pytest" "Running tests"
}

function Build-Package {
    Clean
    return Invoke-DevCommand "python -m build" "Building package"
}

function Test-Build {
    return Invoke-DevCommand "twine check dist/*" "Checking built package"
}

function Upload-PyPI {
    Write-Header "Uploading to PyPI"
    Write-Host "Note: You'll need to enter your PyPI credentials" -ForegroundColor Yellow
    return Invoke-DevCommand "twine upload dist/*" "Uploading to PyPI"
}

function Install-Dev {
    return Invoke-DevCommand "pip install -e ." "Installing in development mode"
}

function Show-Help {
    Write-Host @"

FINDSYM Development Helper (PowerShell)

Available commands:
  clean          - Remove build artifacts and cache files
  format         - Format code using black and isort
  lint           - Run linting checks (flake8, black, isort)
  test           - Run test suite
  build          - Build the package
  build-check    - Check the built package
  install-dev    - Install in development mode
  upload         - Upload to PyPI
  help           - Show this help

Complete release workflow:
  1. .\dev.ps1 clean
  2. .\dev.ps1 format
  3. .\dev.ps1 lint
  4. .\dev.ps1 test
  5. .\dev.ps1 build
  6. .\dev.ps1 build-check
  7. .\dev.ps1 upload

Usage:
  .\dev.ps1 <command>

"@ -ForegroundColor Cyan
}

# Main command dispatcher
switch ($Command.ToLower()) {
    "clean" { Clean }
    "format" { Format-Code }
    "lint" { Test-Lint }
    "test" { Test-Package }
    "build" { Build-Package }
    "build-check" { Test-Build }
    "upload" { Upload-PyPI }
    "install-dev" { Install-Dev }
    "help" { Show-Help }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help 
    }
}
