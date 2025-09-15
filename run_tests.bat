@echo off
echo Chạy test tích hợp giữa các microservices
echo ---------------------------------------------
echo.

:: Kích hoạt môi trường ảo
call venv\Scripts\activate.bat

:: Cài đặt thư viện requests nếu chưa có
pip install requests colorama

:: Chạy script test
python scripts\test_integration.py

echo.
pause