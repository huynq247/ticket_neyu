@echo off
echo ===================================================
echo        TICKET FRONTEND ENVIRONMENT CHECKER
echo ===================================================
echo.

REM Kiểm tra xem file .env có tồn tại không
if exist "%~dp0.env" (
    echo [OK] File .env đã tồn tại
) else (
    echo [CẢNH BÁO] File .env không tồn tại! Đang tạo từ file mẫu...
    copy "%~dp0.env.example" "%~dp0.env" > nul
    if exist "%~dp0.env" (
        echo [OK] Đã tạo file .env từ file mẫu thành công
    ) else (
        echo [LỖI] Không thể tạo file .env!
        exit /b 1
    )
)

echo.
echo Cấu hình hiện tại:
echo ---------------------------------------------------
findstr /v "^#" "%~dp0.env" | findstr /v "^$"
echo ---------------------------------------------------
echo.

echo API Gateway URL:   http://localhost:%VITE_DEV_SERVER_PORT%
echo Frontend URL:      http://localhost:%VITE_DEV_SERVER_PORT%
echo.

echo === Các bước tiếp theo ===
echo 1. Kiểm tra cấu hình API Gateway và Port trong file .env
echo 2. Khởi động backend microservices với run_local_enhanced.ps1
echo 3. Khởi động frontend với npm run dev
echo.

echo Nhấn phím bất kỳ để thoát...
pause > nul