@echo off
echo ========================================
echo TTS Playground API - VibeVoice Hindi
echo Model: tarun7r/vibevoice-hindi-1.5B
echo ========================================
echo.

REM Activate the VibeVoice virtual environment
if exist "venv-vibevoice\Scripts\activate.bat" (
    echo Activating venv-vibevoice...
    call venv-vibevoice\Scripts\activate.bat
) else (
    echo ERROR: venv-vibevoice not found!
    echo Please create it first:
    echo   python -m venv venv-vibevoice
    echo   venv-vibevoice\Scripts\activate
    echo   pip install -e . -r requirements-vibevoice.txt
    pause
    exit /b 1
)

echo.
echo Starting API server...
echo API will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

cd api
python start_api.py

pause
