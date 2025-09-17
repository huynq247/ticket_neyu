@echo off
echo Starting User Service on port 8000...
cd /d D:\NeyuProject
set PYTHON_EXE=D:\NeyuProject\venv_py310\Scripts\python.exe

REM Ensure dependencies are installed
REM %PYTHON_EXE% -m pip install -r services\user-service\requirements.txt

cd services\user-service
echo Starting User Service...
%PYTHON_EXE% main.py