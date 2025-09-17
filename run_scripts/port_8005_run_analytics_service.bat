@echo off
echo Starting Analytics Service on port 8005...
cd /d D:\NeyuProject
set PYTHON_EXE=D:\NeyuProject\venv_py310\Scripts\python.exe
cd services\analytics-service
REM %PYTHON_EXE% -m pip install -r requirements.txt
%PYTHON_EXE% main.py