@echo off
echo Khoi dong Day Du Microservices Ticket Management System
echo -------------------------------------------
echo.
echo Dang khoi dong tat ca cac microservices...

:: Khoi dong microservices
start powershell -ExecutionPolicy Bypass -NoExit -Command "cd D:\NeyuProject; .\run_local_enhanced.ps1 start; echo 'Microservices dang chay. Dong cua so nay se tat tat ca cac service.'"

:: Cho 10 giay de microservices khoi dong
echo Cho 10 giay de microservices khoi dong...
timeout /t 10 /nobreak > nul

:: Khoi dong frontend
echo Dang khoi dong frontend...
start powershell -ExecutionPolicy Bypass -NoExit -Command "cd D:\NeyuProject\ticket-frontend; npm run dev"

echo.
echo Tat ca cac dich vu da duoc khoi dong!
echo.
echo - Microservices: cua so PowerShell rieng biet
echo - User Service: http://localhost:8000/docs
echo - Ticket Service: http://localhost:8001/docs
echo - File Service: http://localhost:8002/docs
echo - Notification Service: http://localhost:8003/docs
echo - Report Service: http://localhost:8004/docs
echo - Analytics Service: http://localhost:8005/docs
echo - API Gateway: http://localhost:8080
echo - Frontend: http://localhost:3000
echo.
echo Dong cua so PowerShell cua microservices se tat cac service backend
echo.
echo Nhap bat ky phim nao de dong cua so nay...
pause > nul