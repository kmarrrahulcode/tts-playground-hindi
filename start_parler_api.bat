@echo off
echo Starting Indic Parler TTS API...
echo.

REM Check if venv-parler exists
if not exist "venv-parler\Scripts\activate.bat" (
    echo ERROR: venv-parler not found!
    echo.
    echo Please create it first:
    echo   python -m venv venv-parler
    echo   venv-parler\Scripts\activate
    echo   pip install -r requirements-parler.txt
    echo   pip install -e .
    pause
    exit /b 1
)

REM Activate and run
call venv-parler\Scripts\activate.bat
python api\start_api.py --engine indic-parler
