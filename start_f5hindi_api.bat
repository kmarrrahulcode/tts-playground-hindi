@echo off
echo Starting F5-Hindi TTS API - Voice Cloning...
echo.

REM Check if venv-f5hindi exists
if not exist "venv-f5hindi\Scripts\activate.bat" (
    echo ERROR: venv-f5hindi not found!
    echo.
    echo Please create it first - requires Python 3.10+:
    echo   py -3.11 -m venv venv-f5hindi
    echo   venv-f5hindi\Scripts\activate
    echo   pip install -r requirements-f5hindi.txt
    echo   pip install -e .
    pause
    exit /b 1
)

REM Activate and run
call venv-f5hindi\Scripts\activate.bat
python api\start_api.py --engine f5-hindi
