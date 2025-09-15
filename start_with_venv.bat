@echo off
echo Khởi động Microservices với môi trường ảo Python
echo ------------------------------------------------
echo.

:: Kiểm tra xem môi trường ảo đã tồn tại chưa
if not exist "venv\Scripts\activate.bat" (
    echo Môi trường ảo chưa được tạo. Vui lòng chạy setup_venv.bat trước.
    echo.
    pause
    exit /b 1
)

:: Kích hoạt môi trường ảo
call venv\Scripts\activate.bat

:: Khởi động các service
echo Đang khởi động các service...
powershell -ExecutionPolicy Bypass -File run_venv.ps1 start

echo.
echo Nhấn phím bất kỳ để dừng tất cả các service...
pause >nul

:: Dừng các service
powershell -ExecutionPolicy Bypass -File run_venv.ps1 stop