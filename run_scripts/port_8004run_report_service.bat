@echo off
echo Starting Report Service on port 8004...
cd /d D:\NeyuProject
set PYTHON_EXE=D:\NeyuProject\venv_py310\Scripts\python.exe
cd services\report-service
REM %PYTHON_EXE% -m pip install -r requirements.txt
%PYTHON_EXE% main.py