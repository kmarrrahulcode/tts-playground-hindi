Write-Host "Checking specific virtual environments for TTS Playground..."

# Function to check and create venv
function Ensure-Venv {
    param (
        [string]$VenvPath,
        [string]$ReqFile
    )

    if (Test-Path $VenvPath) {
        Write-Host "  [SKIP] '$VenvPath' already exists." -ForegroundColor Yellow
    }
    else {
        Write-Host "  [CREATE] Creating '$VenvPath'..." -ForegroundColor Cyan
        python -m venv $VenvPath
        
        if (Test-Path "$VenvPath\Scripts\pip.exe") {
             Write-Host "  [INSTALL] Installing dependencies from '$ReqFile'..." -ForegroundColor Cyan
             & "$VenvPath\Scripts\pip.exe" install -r $ReqFile
             Write-Host "  [DONE] Setup complete for '$VenvPath'." -ForegroundColor Green
        } else {
             Write-Error "Failed to create virtual environment architecture at '$VenvPath'."
        }
    }
}

# 1. Standard venv
Write-Host "`n1. Standard Environment (venv)"
Ensure-Venv -VenvPath "venv" -ReqFile "requirements.txt"

# 2. Indri venv
Write-Host "`n2. Indri Environment (venv-indri)"
Ensure-Venv -VenvPath "venv-indri" -ReqFile "requirements-indri.txt"

Write-Host "`nAll checks complete. Environments are ready if no errors occurred." -ForegroundColor Green
Read-Host "Press Enter to exit..."
