@echo off

set python="%~dp0\server\app\venv\Scripts\python.exe"
%python% "%~dp0\server\app\manage.py" runserver 0.0.0.0:8000

pause