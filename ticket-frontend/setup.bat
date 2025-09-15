@echo off
echo ===================================================
echo        TICKET FRONTEND DEVELOPMENT SETUP
echo ===================================================
echo.

REM Kiểm tra Node.js đã được cài đặt
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [LỖI] Node.js chưa được cài đặt!
    echo Vui lòng cài đặt Node.js từ https://nodejs.org/
    exit /b 1
)

REM Kiểm tra và tạo file .env nếu chưa có
if not exist "%~dp0.env" (
    echo [THÔNG BÁO] File .env không tồn tại, đang tạo từ file mẫu...
    copy "%~dp0.env.example" "%~dp0.env" >nul
    if %ERRORLEVEL% NEQ 0 (
        echo [LỖI] Không thể tạo file .env!
        exit /b 1
    )
    echo [OK] Đã tạo file .env từ file mẫu
)

REM Cài đặt dependencies
echo [THÔNG BÁO] Đang cài đặt dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [LỖI] Cài đặt dependencies thất bại!
    exit /b 1
)
echo [OK] Đã cài đặt dependencies

echo.
echo [HOÀN THÀNH] Quá trình thiết lập đã hoàn tất!
echo.
echo Tiếp theo, bạn có thể:
echo  - Khởi động frontend:        npm run dev
echo  - Kiểm tra kết nối services: npm run check-connections
echo  - Kiểm tra cấu hình:         .\check_env.bat
echo.
echo Nhấn phím bất kỳ để thoát...
pause >nul