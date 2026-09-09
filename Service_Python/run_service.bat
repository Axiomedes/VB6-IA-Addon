@echo off
title VB6 AI Assistant - FastAPI Service
:: Forzar a que el directorio de trabajo sea la carpeta donde está este .bat
cd /d "%~dp0"
echo =====================================================================
echo    INICIANDO SERVICIO LOCAL: VB6 AI Assistant (FastAPI)
echo =====================================================================
echo Puerto: 8765
echo URL:    http://127.0.0.1:8765
echo Docs:   http://127.0.0.1:8765/docs
echo =====================================================================
python -m uvicorn app.main:app --host 127.0.0.1 --port 8765 --reload
pause
