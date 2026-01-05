param(
    [switch]$Run
)

$ErrorActionPreference = "Stop"

# Ensure we're running from the script's directory
Push-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$root = Resolve-Path ..
Set-Location $root

# Create venv if missing
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment (.venv)..."
    python -m venv .venv
}

# Activate venv
$venvActivate = ".venv/Scripts/Activate.ps1"
. $venvActivate

# Upgrade pip and install deps
python -m pip install --upgrade pip
if (Test-Path "pyproject.toml") {
    Write-Host "Installing package in editable mode..."
    python -m pip install -e .
} else {
    python -m pip install -r requirements.txt
}

Write-Host "Setup complete."

if ($Run) {
    if (Get-Command map-ui -ErrorAction SilentlyContinue) {
        map-ui
    } else {
        python UI.py
    }
}
