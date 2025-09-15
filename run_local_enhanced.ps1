# PowerShell script để chạy các microservice trực tiếp trên Windows
# Script này sẽ chạy các service mà không cần Docker, sử dụng database từ xa

# Biến lưu trữ Process ID của các service
$userServicePid = $null
$ticketServicePid = $null
$fileServicePid = $null
$notificationServicePid = $null
$reportServicePid = $null
$analyticsServicePid = $null
$apiGatewayPid = $null

# Kiểm tra Python đã được cài đặt chưa
function Test-Python {
    try {
        $pythonVersion = python --version
        Write-Host "Python đã được cài đặt: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Python chưa được cài đặt hoặc không có trong PATH. Vui lòng cài đặt Python 3.9+ và thử lại." -ForegroundColor Red
        return $false
    }
}

# Kiểm tra Node.js đã được cài đặt chưa
function Test-NodeJS {
    try {
        $nodeVersion = node --version
        Write-Host "Node.js đã được cài đặt: $nodeVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Node.js chưa được cài đặt hoặc không có trong PATH. Vui lòng cài đặt Node.js 14+ và thử lại." -ForegroundColor Red
        return $false
    }
}

# Kiểm tra các dependency cho Python
function Install-PythonDependencies {
    param (
        [string]$servicePath
    )
    
    if (-not (Test-Python)) { return $false }
    
    Write-Host "Kiểm tra và cài đặt các dependency Python cho $servicePath..." -ForegroundColor Yellow
    
    # Chuyển đến thư mục service
    Set-Location -Path "$PSScriptRoot\services\$servicePath"
    
    # Cài đặt các dependency
    python -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Đã cài đặt thành công các dependency cho $servicePath" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "Lỗi khi cài đặt dependency cho $servicePath" -ForegroundColor Red
        return $false
    }
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
}

# Kiểm tra các dependency cho Node.js
function Install-NodeDependencies {
    param (
        [string]$servicePath
    )
    
    if (-not (Test-NodeJS)) { return $false }
    
    Write-Host "Kiểm tra và cài đặt các dependency Node.js cho $servicePath..." -ForegroundColor Yellow
    
    # Chuyển đến thư mục service
    Set-Location -Path "$PSScriptRoot\services\$servicePath"
    
    # Cài đặt các dependency
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Đã cài đặt thành công các dependency cho $servicePath" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "Lỗi khi cài đặt dependency cho $servicePath" -ForegroundColor Red
        return $false
    }
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
}

# Chạy User Service
function Start-UserService {
    if (-not (Test-Python)) { return }
    
    # Cài đặt dependencies nếu cần
    if (-not (Install-PythonDependencies -servicePath "user-service")) { return }
    
    Write-Host "Đang khởi động User Service..." -ForegroundColor Green
    
    # Chuyển đến thư mục user service
    Set-Location -Path "$PSScriptRoot\services\user-service"
    
    # Khởi động service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000 --reload" -PassThru -NoNewWindow
    $script:userServicePid = $process.Id
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "User Service đã khởi động thành công (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Truy cập tại: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không thể khởi động User Service" -ForegroundColor Red
    }
}

# Chạy Ticket Service
function Start-TicketService {
    if (-not (Test-Python)) { return }
    
    # Cài đặt dependencies nếu cần
    if (-not (Install-PythonDependencies -servicePath "ticket-service")) { return }
    
    Write-Host "Đang khởi động Ticket Service..." -ForegroundColor Green
    
    # Chuyển đến thư mục ticket service
    Set-Location -Path "$PSScriptRoot\services\ticket-service"
    
    # Khởi động service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8001 --reload" -PassThru -NoNewWindow
    $script:ticketServicePid = $process.Id
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "Ticket Service đã khởi động thành công (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Truy cập tại: http://localhost:8001/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không thể khởi động Ticket Service" -ForegroundColor Red
    }
}

# Chạy File Service
function Start-FileService {
    if (-not (Test-Python)) { return }
    
    # Cài đặt dependencies nếu cần
    if (-not (Install-PythonDependencies -servicePath "file-service")) { return }
    
    Write-Host "Đang khởi động File Service..." -ForegroundColor Green
    
    # Chuyển đến thư mục file service
    Set-Location -Path "$PSScriptRoot\services\file-service"
    
    # Khởi động service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8002 --reload" -PassThru -NoNewWindow
    $script:fileServicePid = $process.Id
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "File Service đã khởi động thành công (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Truy cập tại: http://localhost:8002/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không thể khởi động File Service" -ForegroundColor Red
    }
}

# Chạy Notification Service
function Start-NotificationService {
    if (-not (Test-Python)) { return }
    
    # Cài đặt dependencies nếu cần
    if (-not (Install-PythonDependencies -servicePath "notification-service")) { return }
    
    Write-Host "Đang khởi động Notification Service..." -ForegroundColor Green
    
    # Chuyển đến thư mục notification service
    Set-Location -Path "$PSScriptRoot\services\notification-service"
    
    # Khởi động service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8003 --reload" -PassThru -NoNewWindow
    $script:notificationServicePid = $process.Id
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "Notification Service đã khởi động thành công (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Truy cập tại: http://localhost:8003/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không thể khởi động Notification Service" -ForegroundColor Red
    }
}

# Chạy Report Service
function Start-ReportService {
    if (-not (Test-Python)) { return }
    
    # Cài đặt dependencies nếu cần
    if (-not (Install-PythonDependencies -servicePath "report-service")) { return }
    
    Write-Host "Đang khởi động Report Service..." -ForegroundColor Green
    
    # Chuyển đến thư mục report service
    Set-Location -Path "$PSScriptRoot\services\report-service"
    
    # Khởi động service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8004 --reload" -PassThru -NoNewWindow
    $script:reportServicePid = $process.Id
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "Report Service đã khởi động thành công (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Truy cập tại: http://localhost:8004/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không thể khởi động Report Service" -ForegroundColor Red
    }
}

# Chạy Analytics Service
function Start-AnalyticsService {
    if (-not (Test-Python)) { return }
    
    # Cài đặt dependencies nếu cần
    if (-not (Install-PythonDependencies -servicePath "analytics-service")) { return }
    
    Write-Host "Đang khởi động Analytics Service..." -ForegroundColor Green
    
    # Chuyển đến thư mục analytics service
    Set-Location -Path "$PSScriptRoot\services\analytics-service"
    
    # Khởi động service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8005 --reload" -PassThru -NoNewWindow
    $script:analyticsServicePid = $process.Id
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "Analytics Service đã khởi động thành công (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Truy cập tại: http://localhost:8005/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không thể khởi động Analytics Service" -ForegroundColor Red
    }
}

# Chạy API Gateway
function Start-APIGateway {
    if (-not (Test-NodeJS)) { return }
    
    # Cài đặt dependencies nếu cần
    if (-not (Install-NodeDependencies -servicePath "api-gateway")) { return }
    
    Write-Host "Đang khởi động API Gateway..." -ForegroundColor Green
    
    # Chuyển đến thư mục API gateway
    Set-Location -Path "$PSScriptRoot\services\api-gateway"
    
    # Khởi động service với PORT=8080 để tránh xung đột với frontend (port 3000)
    $env:PORT = "8080"
    $process = Start-Process -FilePath "npm" -ArgumentList "start" -PassThru -NoNewWindow
    $script:apiGatewayPid = $process.Id
    
    # Trở về thư mục gốc
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "API Gateway đã khởi động thành công (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Truy cập tại: http://localhost:8080" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không thể khởi động API Gateway" -ForegroundColor Red
    }
}

# Khởi động tất cả các service
function Start-AllServices {
    Write-Host "Đang khởi động tất cả các service..." -ForegroundColor Green
    
    # Khởi động các service theo thứ tự
    Start-UserService
    Start-TicketService
    Start-FileService
    Start-NotificationService
    Start-ReportService
    Start-AnalyticsService
    Start-APIGateway
    
    Write-Host "Tất cả các service đã được khởi động!" -ForegroundColor Green
    Write-Host "Để dừng các service, chạy: .\run_local_enhanced.ps1 stop" -ForegroundColor Yellow
}

# Dừng tất cả các service
function Stop-AllServices {
    Write-Host "Đang dừng tất cả các service..." -ForegroundColor Yellow
    
    # Dừng User Service
    if ($null -ne $script:userServicePid -and $script:userServicePid -gt 0) {
        try {
            Stop-Process -Id $script:userServicePid -Force
            Write-Host "User Service đã dừng thành công" -ForegroundColor Green
        }
        catch {
            Write-Host "Không thể dừng User Service: $_" -ForegroundColor Red
        }
    }
    
    # Dừng Ticket Service
    if ($null -ne $script:ticketServicePid -and $script:ticketServicePid -gt 0) {
        try {
            Stop-Process -Id $script:ticketServicePid -Force
            Write-Host "Ticket Service đã dừng thành công" -ForegroundColor Green
        }
        catch {
            Write-Host "Không thể dừng Ticket Service: $_" -ForegroundColor Red
        }
    }
    
    # Dừng File Service
    if ($null -ne $script:fileServicePid -and $script:fileServicePid -gt 0) {
        try {
            Stop-Process -Id $script:fileServicePid -Force
            Write-Host "File Service đã dừng thành công" -ForegroundColor Green
        }
        catch {
            Write-Host "Không thể dừng File Service: $_" -ForegroundColor Red
        }
    }
    
    # Dừng Notification Service
    if ($null -ne $script:notificationServicePid -and $script:notificationServicePid -gt 0) {
        try {
            Stop-Process -Id $script:notificationServicePid -Force
            Write-Host "Notification Service đã dừng thành công" -ForegroundColor Green
        }
        catch {
            Write-Host "Không thể dừng Notification Service: $_" -ForegroundColor Red
        }
    }
    
    # Dừng Report Service
    if ($null -ne $script:reportServicePid -and $script:reportServicePid -gt 0) {
        try {
            Stop-Process -Id $script:reportServicePid -Force
            Write-Host "Report Service đã dừng thành công" -ForegroundColor Green
        }
        catch {
            Write-Host "Không thể dừng Report Service: $_" -ForegroundColor Red
        }
    }
    
    # Dừng Analytics Service
    if ($null -ne $script:analyticsServicePid -and $script:analyticsServicePid -gt 0) {
        try {
            Stop-Process -Id $script:analyticsServicePid -Force
            Write-Host "Analytics Service đã dừng thành công" -ForegroundColor Green
        }
        catch {
            Write-Host "Không thể dừng Analytics Service: $_" -ForegroundColor Red
        }
    }
    
    # Dừng API Gateway
    if ($null -ne $script:apiGatewayPid -and $script:apiGatewayPid -gt 0) {
        try {
            Stop-Process -Id $script:apiGatewayPid -Force
            Write-Host "API Gateway đã dừng thành công" -ForegroundColor Green
        }
        catch {
            Write-Host "Không thể dừng API Gateway: $_" -ForegroundColor Red
        }
    }
    
    # Tìm và dừng các process còn chạy trên các port
    try {
        $port8000Process = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8000Process) {
            Stop-Process -Id $port8000Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 8000" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port8001Process = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8001Process) {
            Stop-Process -Id $port8001Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 8001" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port8002Process = Get-NetTCPConnection -LocalPort 8002 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8002Process) {
            Stop-Process -Id $port8002Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 8002" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port8003Process = Get-NetTCPConnection -LocalPort 8003 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8003Process) {
            Stop-Process -Id $port8003Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 8003" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port8004Process = Get-NetTCPConnection -LocalPort 8004 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8004Process) {
            Stop-Process -Id $port8004Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 8004" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port8005Process = Get-NetTCPConnection -LocalPort 8005 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8005Process) {
            Stop-Process -Id $port8005Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 8005" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port8080Process = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8080Process) {
            Stop-Process -Id $port8080Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 8080" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port3000Process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port3000Process) {
            Stop-Process -Id $port3000Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process trên port 3000" -ForegroundColor Green
        }
    } catch {}
    
    Write-Host "Tất cả các service đã dừng!" -ForegroundColor Green
}

# Hiển thị trợ giúp
function Show-Help {
    Write-Host "Sử dụng: .\run_local_enhanced.ps1 [lệnh]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Các lệnh:" -ForegroundColor White
    Write-Host "  start       Khởi động tất cả các service" -ForegroundColor Gray
    Write-Host "  stop        Dừng tất cả các service" -ForegroundColor Gray
    Write-Host "  user        Chỉ khởi động User Service" -ForegroundColor Gray
    Write-Host "  ticket      Chỉ khởi động Ticket Service" -ForegroundColor Gray
    Write-Host "  file        Chỉ khởi động File Service" -ForegroundColor Gray
    Write-Host "  notification Chỉ khởi động Notification Service" -ForegroundColor Gray
    Write-Host "  report      Chỉ khởi động Report Service" -ForegroundColor Gray
    Write-Host "  analytics   Chỉ khởi động Analytics Service" -ForegroundColor Gray
    Write-Host "  gateway     Chỉ khởi động API Gateway" -ForegroundColor Gray
    Write-Host "  help        Hiển thị thông báo trợ giúp này" -ForegroundColor Gray
}

# Xử lý lệnh
$command = $args[0]

switch ($command) {
    "start" {
        Start-AllServices
    }
    "stop" {
        Stop-AllServices
    }
    "user" {
        Start-UserService
    }
    "ticket" {
        Start-TicketService
    }
    "file" {
        Start-FileService
    }
    "notification" {
        Start-NotificationService
    }
    "report" {
        Start-ReportService
    }
    "analytics" {
        Start-AnalyticsService
    }
    "gateway" {
        Start-APIGateway
    }
    default {
        Show-Help
    }
}