@echo off
echo ========================================================
echo Starting AI ScamShield Local Backend Daemon (FastAPI)
echo Privacy-First Offline Risk Intelligence Engine
echo ========================================================
cd /d "%~dp0"
.venv\Scripts\uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
