@echo off

set python="%~dp0\server\app\venv\Scripts\python.exe"
%python% "%~dp0\server\app\manage.py" run_telegram_bot

pause