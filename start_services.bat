@echo off
echo Khởi động Microservices Ticket Management System
echo -------------------------------------------
echo.

powershell -ExecutionPolicy Bypass -File run_local.ps1 start

echo.
echo Nhấn phím bất kỳ để dừng tất cả các service...
pause >nul

powershell -ExecutionPolicy Bypass -File run_local.ps1 stop