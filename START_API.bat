@echo off
echo ========================================
echo NER Smart Logistics - Starting API Server
echo ========================================
echo.

cd /d "%~dp0backend"

echo Activating Python environment...
call venv\Scripts\activate.bat

echo Setting Python path...
set PYTHONPATH=%~dp0backend

echo.
echo Starting FastAPI server...
echo API will be available at: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload
