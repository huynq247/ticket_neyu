# Script để cập nhật quyền cho vai trò admin và manager

Write-Host "Cập nhật quyền cho vai trò admin và manager..." -ForegroundColor Yellow

# Đảm bảo dịch vụ user-service đang chạy
$userServiceRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/health" -Method GET -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        $userServiceRunning = $true
        Write-Host "User Service đang chạy, tiếp tục cập nhật quyền..." -ForegroundColor Green
    }
} catch {
    Write-Host "User Service không chạy. Vui lòng khởi động trước khi chạy script này." -ForegroundColor Red
    Write-Host "Bạn có thể sử dụng lệnh: ./run_user_service.ps1" -ForegroundColor Yellow
    exit 1
}

# Đường dẫn tới Python và môi trường ảo
$pythonPath = "$PSScriptRoot\venv_py310\Scripts\python.exe"
if (-not (Test-Path $pythonPath)) {
    $pythonPath = "python"
    Write-Host "Sử dụng Python mặc định trong hệ thống" -ForegroundColor Yellow
}

# Cài đặt module requests nếu chưa có
Write-Host "Kiểm tra và cài đặt module requests nếu cần..." -ForegroundColor Yellow
& $pythonPath -c "
try:
    import requests
    print('Module requests đã được cài đặt')
except ImportError:
    import sys
    import subprocess
    print('Cài đặt module requests...')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
    print('Đã cài đặt module requests thành công')
"

# Chạy script Python để cập nhật quyền
Write-Host "Đang chạy script cập nhật quyền..." -ForegroundColor Cyan
& $pythonPath "$PSScriptRoot\scripts\update_role_permissions.py"

# Kiểm tra kết quả
if ($LASTEXITCODE -eq 0) {
    Write-Host "Cập nhật quyền thành công!" -ForegroundColor Green
    Write-Host "Vui lòng đăng xuất và đăng nhập lại để áp dụng các quyền mới." -ForegroundColor Yellow
} else {
    Write-Host "Có lỗi xảy ra khi cập nhật quyền. Vui lòng kiểm tra lỗi ở trên." -ForegroundColor Red
}