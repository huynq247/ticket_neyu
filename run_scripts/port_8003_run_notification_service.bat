@echo off
echo Starting Notification Service on port 8003...
cd /d D:\NeyuProject
set PYTHON_EXE=D:\NeyuProject\venv_py310\Scripts\python.exe
cd services\notification-service
REM %PYTHON_EXE% -m pip install -r requirements.txt
%PYTHON_EXE% main.py