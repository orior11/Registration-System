@echo off
REM Quick Start Script for Authentication API (Windows)

echo Starting Authentication API...
echo.

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found. Creating from .env.example...
    copy .env.example .env
    echo Please edit .env with your actual credentials before running again.
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check JWT_SECRET
findstr /C:"your-secret-key-here-change-this-in-production" .env >nul
if %errorlevel%==0 (
    echo.
    echo WARNING: You're using the default JWT_SECRET!
    echo Generate a secure one with:
    echo python -c "import secrets; print(secrets.token_urlsafe(32))"
    echo.
)

REM Start the server
echo.
echo Starting server...
echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
