@echo off
echo ========================================
echo NER Smart Logistics - System Startup
echo ========================================
echo.

echo Step 1: Starting Docker containers...
cd /d "%~dp0backend"
docker compose up -d

echo.
echo Step 2: Waiting for database to be ready...
timeout /t 10 /nobreak

echo.
echo Step 3: Checking container status...
docker compose ps

echo.
echo ========================================
echo Docker containers started!
echo ========================================
echo.
echo Next steps:
echo 1. Run START_API.bat to start the API server
echo 2. Or activate manually:
echo    cd backend
echo    venv\Scripts\activate
echo    set PYTHONPATH=%~dp0backend
echo    uvicorn app.main:app --reload
echo.
pause
