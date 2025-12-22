@echo off
REM TTS Playground API Starter - XTTS Hindi Model
REM This script can be run from anywhere on your system

REM Set the project directory (change this if you move the project)
set SCRIPT_DIR=C:\Workspace\Interests\TTS\tts-playground-hindi

echo ============================================================
echo TTS Playground API - XTTS Hindi
echo ============================================================
echo.
echo Project Directory: %SCRIPT_DIR%
echo Virtual Environment: venv
echo Model: xtts-hindi
echo.

REM Check if virtual environment exists
if not exist "%SCRIPT_DIR%\venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found at %SCRIPT_DIR%\venv
    echo Please create it first by running: python -m venv venv
    echo.
    pause
    exit /b 1
)

REM Check if HF_TOKEN is set
if "%HF_TOKEN%"=="" (
    echo WARNING: HF_TOKEN environment variable is not set
    echo Please set it using: set HF_TOKEN=your_token_here
    echo.
    set /p HF_TOKEN="Enter your Hugging Face token (or press Enter to continue): "
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
"%SCRIPT_DIR%\venv\Scripts\python.exe" "%SCRIPT_DIR%\api\start_api.py"
