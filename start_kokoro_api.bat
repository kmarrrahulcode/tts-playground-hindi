@echo off
REM TTS Playground API Starter - Kokoro Hindi Model
REM This script can be run from anywhere on your system

REM Set the project directory (change this if you move the project)
set SCRIPT_DIR=C:\Workspace\Interests\TTS\tts-playground-hindi

echo ============================================================
echo TTS Playground API - Kokoro Hindi
echo ============================================================
echo.
echo Project Directory: %SCRIPT_DIR%
echo Virtual Environment: venv-kokoro
echo Model: kokoro
echo.

REM Check if virtual environment exists
if not exist "%SCRIPT_DIR%\venv-kokoro\Scripts\activate.bat" (
    echo ERROR: venv-kokoro not found at %SCRIPT_DIR%\venv-kokoro
    echo.
    echo Please create it first - requires Python 3.10-3.12:
    echo   py -3.11 -m venv venv-kokoro
    echo   venv-kokoro\Scripts\activate
    echo   pip install -r requirements-kokoro.txt
    echo   pip install -e .
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...

echo.
echo Starting API server...
echo API will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Run Python from the virtual environment directly
"%SCRIPT_DIR%\venv-kokoro\Scripts\python.exe" "%SCRIPT_DIR%\api\start_api.py" --engine kokoro
