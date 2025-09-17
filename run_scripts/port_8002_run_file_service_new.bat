@echo off
echo Starting File Service on port 8002 with new main file...
cd /d D:\NeyuProject
set PYTHON_EXE=D:\NeyuProject\venv_py310\Scripts\python.exe
cd services\file-service
%PYTHON_EXE% main_new.py