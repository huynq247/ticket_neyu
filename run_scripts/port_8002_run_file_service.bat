@echo off
echo Starting File Service on port 8002...
cd /d D:\NeyuProject
set PYTHON_EXE=D:\NeyuProject\venv_py310\Scripts\python.exe
cd services\file-service
REM %PYTHON_EXE% -m pip install -r requirements.txt
%PYTHON_EXE% main.py