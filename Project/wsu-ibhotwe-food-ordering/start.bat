@echo off
cd /d "%~dp0"
echo Starting WSU Ibhotwe Food Ordering Platform...
py -m uvicorn backend.main:app --reload
if errorlevel 1 (
    python -m uvicorn backend.main:app --reload
)
pause
