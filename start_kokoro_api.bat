@echo off
echo Starting Kokoro TTS API - Hindi...
echo.

REM Check if venv-kokoro exists
if not exist "venv-kokoro\Scripts\activate.bat" (
    echo ERROR: venv-kokoro not found!
    echo.
    echo Please create it first - requires Python 3.10-3.12:
    echo   py -3.11 -m venv venv-kokoro
    echo   venv-kokoro\Scripts\activate
    echo   pip install -r requirements-kokoro.txt
    echo   pip install -e .
    pause
    exit /b 1
)

REM Activate and run
call venv-kokoro\Scripts\activate.bat
python api\start_api.py --engine kokoro
