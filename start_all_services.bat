@echo off
echo Starting all backend microservices with Python 3.10...

:: Start PowerShell script to start all services
powershell -File "%~dp0start_all_services.ps1"