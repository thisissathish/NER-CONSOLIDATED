@echo off
echo ========================================
echo NER Smart Logistics - Quick Start Guide
echo ========================================
echo.
echo This script will help you start the entire system.
echo.
echo Prerequisites:
echo [1] Docker Desktop must be running
echo [2] Python virtual environment must be set up
echo.
echo ========================================
echo.

:MENU
echo What would you like to do?
echo.
echo [1] Start Docker containers only
echo [2] Start API server (assumes Docker is running)
echo [3] Start everything (Docker + API)
echo [4] Stop everything
echo [5] Check system status
echo [6] Open API documentation in browser
echo [7] Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto START_DOCKER
if "%choice%"=="2" goto START_API
if "%choice%"=="3" goto START_ALL
if "%choice%"=="4" goto STOP_ALL
if "%choice%"=="5" goto CHECK_STATUS
if "%choice%"=="6" goto OPEN_DOCS
if "%choice%"=="7" goto END

echo Invalid choice. Please try again.
goto MENU

:START_DOCKER
echo.
echo Starting Docker containers...
cd /d "%~dp0backend"
docker compose up -d
echo.
echo Docker containers started!
echo.
pause
goto MENU

:START_API
echo.
echo Starting API server...
echo Opening new window...
start "NER API Server" cmd /k "cd /d "%~dp0backend" && call venv\Scripts\activate.bat && set PYTHONPATH=%~dp0backend && uvicorn app.main:app --reload"
echo.
echo API server starting in new window...
echo Wait 10 seconds, then visit: http://localhost:8000/docs
echo.
pause
goto MENU

:START_ALL
echo.
echo Starting Docker containers...
cd /d "%~dp0backend"
docker compose up -d
echo.
echo Waiting 15 seconds for database to initialize...
timeout /t 15 /nobreak
echo.
echo Starting API server in new window...
start "NER API Server" cmd /k "cd /d "%~dp0backend" && call venv\Scripts\activate.bat && set PYTHONPATH=%~dp0backend && uvicorn app.main:app --reload"
echo.
echo System starting up!
echo Wait 10 seconds, then visit: http://localhost:8000/docs
echo.
pause
goto MENU

:STOP_ALL
echo.
echo Stopping all services...
cd /d "%~dp0backend"
docker compose down
echo.
echo All services stopped.
echo.
pause
goto MENU

:CHECK_STATUS
echo.
echo Checking system status...
echo.
echo === Docker Containers ===
cd /d "%~dp0backend"
docker compose ps
echo.
echo === Checking API Server ===
curl http://localhost:8000/health 2>nul
if errorlevel 1 (
    echo API server is NOT running
) else (
    echo API server is running!
)
echo.
pause
goto MENU

:OPEN_DOCS
echo.
echo Opening API documentation in browser...
start http://localhost:8000/docs
echo.
pause
goto MENU

:END
echo.
echo Exiting...
exit
