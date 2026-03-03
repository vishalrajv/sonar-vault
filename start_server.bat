@echo off
echo Starting Sonar Vault Server...
echo.

if not exist .venv (
    echo Error: Virtual environment [.venv] not found.
    echo Please run the setup steps or create the venv first.
    pause
    exit /b
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo.
echo Server is starting at http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server.
echo.

uvicorn app.main:app --reload
