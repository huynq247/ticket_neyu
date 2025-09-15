@echo off
echo Tạo môi trường Python ảo cho dự án Ticket Management
echo -----------------------------------------------------
echo.

:: Tạo thư mục cho môi trường ảo nếu chưa tồn tại
if not exist "venv" (
    echo Đang tạo môi trường ảo với Python hiện tại...
    python -m venv venv
) else (
    echo Môi trường ảo đã tồn tại.
)

:: Kích hoạt môi trường ảo
echo Kích hoạt môi trường ảo...
call venv\Scripts\activate.bat

:: Nâng cấp pip
echo Nâng cấp pip...
python -m pip install --upgrade pip

:: Cài đặt các dependency cho User Service
echo Cài đặt dependencies cho User Service...
cd services\user-service
pip install -r requirements.txt
cd ..\..

:: Cài đặt các dependency cho Ticket Service
echo Cài đặt dependencies cho Ticket Service...
cd services\ticket-service
pip install -r requirements.txt
cd ..\..

:: Cài đặt các dependency cho API Gateway
echo Cài đặt dependencies cho API Gateway...
cd services\api-gateway
npm install
cd ..\..

echo.
echo Môi trường đã được thiết lập thành công!
echo Để kích hoạt môi trường ảo sau này, chỉ cần chạy: venv\Scripts\activate.bat
echo.

:: Giữ cửa sổ cmd mở
cmd /k venv\Scripts\activate.bat