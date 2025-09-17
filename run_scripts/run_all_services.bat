@echo off
echo Starting all microservices in separate windows...

cd /d D:\NeyuProject\run_scripts

:: Chạy từng service trong một cửa sổ CMD riêng biệt
start cmd /k run_user_service.bat
timeout /t 5
start cmd /k run_ticket_service.bat
timeout /t 5
start cmd /k run_file_service.bat
timeout /t 5
start cmd /k run_notification_service.bat
timeout /t 5
start cmd /k run_report_service.bat
timeout /t 5
start cmd /k run_analytics_service.bat
timeout /t 5
start cmd /k run_api_gateway.bat
timeout /t 5
start cmd /k run_frontend.bat

echo All services have been started in separate windows.
echo Please check each window for any error messages.