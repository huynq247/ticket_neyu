@echo off
echo Khoi dong Ticket Management System
echo -------------------------------------------
echo.
echo Dang khoi dong cac microservice...

:: Khoi dong microservices
start powershell -ExecutionPolicy Bypass -NoExit -Command "cd D:\NeyuProject; .\run_local.ps1 start; echo 'Microservices dang chay. Dong cua so nay se tat tat ca cac service.'"

:: Cho 5 giay de microservices khoi dong
echo Cho 5 giay de microservices khoi dong...
timeout /t 5 /nobreak > nul

:: Khoi dong frontend
echo Dang khoi dong frontend...
start powershell -ExecutionPolicy Bypass -NoExit -Command "cd D:\NeyuProject\ticket-frontend; npm run dev"

echo.
echo Tat ca cac dich vu da duoc khoi dong!
echo.
echo - Microservices: cua so PowerShell rieng biet
echo - Frontend: http://localhost:3000
echo.
echo Dong cua so PowerShell cua microservices se tat cac service backend
echo.
echo Nhap bat ky phim nao de dong cua so nay...
pause > nul