# PowerShell script để chạy các microservice trong môi trường ảo

# Biến lưu trữ Process ID của các service
$userServicePid = $null
$apiGatewayPid = $null
$ticketServicePid = $null

# Đường dẫn tới môi trường ảo
$venvPath = ".\venv\Scripts\activate"

# Kích hoạt môi trường ảo
function Activate-Venv {
    if (Test-Path -Path ".\venv\Scripts\activate.ps1") {
        Write-Host "Kích hoạt môi trường ảo..." -ForegroundColor Green
        & ".\venv\Scripts\activate.ps1"
        return $true
    } else {
        Write-Host "Không tìm thấy môi trường ảo. Vui lòng chạy setup_venv.bat trước." -ForegroundColor Red
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

# Chạy User Service
function Start-UserService {
    if (-not (Activate-Venv)) { return }
    
    Write-Host "Đang khởi động User Service..." -ForegroundColor Green
    
    # Khởi động service trong terminal mới
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; .\venv\Scripts\activate.ps1; cd services\user-service; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    
    Write-Host "User Service đã khởi động" -ForegroundColor Green
    Write-Host "Truy cập tại: http://localhost:8000/docs" -ForegroundColor Cyan
}

# Chạy Ticket Service
function Start-TicketService {
    if (-not (Activate-Venv)) { return }
    
    Write-Host "Đang khởi động Ticket Service..." -ForegroundColor Green
    
    # Khởi động service trong terminal mới
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; .\venv\Scripts\activate.ps1; cd services\ticket-service; python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload"
    
    Write-Host "Ticket Service đã khởi động" -ForegroundColor Green
    Write-Host "Truy cập tại: http://localhost:8001/docs" -ForegroundColor Cyan
}

# Chạy API Gateway
function Start-APIGateway {
    if (-not (Test-NodeJS)) { return }
    
    Write-Host "Đang khởi động API Gateway..." -ForegroundColor Green
    
    # Khởi động service trong terminal mới
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\services\api-gateway'; npm start"
    
    Write-Host "API Gateway đã khởi động" -ForegroundColor Green
    Write-Host "Truy cập tại: http://localhost:3000" -ForegroundColor Cyan
}

# Khởi động tất cả các service
function Start-AllServices {
    Write-Host "Đang khởi động tất cả các service..." -ForegroundColor Green
    
    # Khởi động các service theo thứ tự
    Start-UserService
    Start-TicketService
    Start-APIGateway
    
    Write-Host "Tất cả các service đã được khởi động!" -ForegroundColor Green
    Write-Host "Để dừng các service, chạy: .\run_venv.ps1 stop" -ForegroundColor Yellow
}

# Dừng tất cả các service
function Stop-AllServices {
    Write-Host "Đang dừng tất cả các service..." -ForegroundColor Yellow
    
    # Tìm và dừng các process chạy trên các port
    try {
        $port8000Process = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8000Process) {
            Stop-Process -Id $port8000Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng User Service (PID: $port8000Process)" -ForegroundColor Green
        }
    } catch {
        Write-Host "Không tìm thấy User Service đang chạy" -ForegroundColor Yellow
    }
    
    try {
        $port8001Process = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8001Process) {
            Stop-Process -Id $port8001Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng Ticket Service (PID: $port8001Process)" -ForegroundColor Green
        }
    } catch {
        Write-Host "Không tìm thấy Ticket Service đang chạy" -ForegroundColor Yellow
    }
    
    try {
        $port3000Process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port3000Process) {
            Stop-Process -Id $port3000Process -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng API Gateway (PID: $port3000Process)" -ForegroundColor Green
        }
    } catch {
        Write-Host "Không tìm thấy API Gateway đang chạy" -ForegroundColor Yellow
    }
    
    # Dừng tất cả các window PowerShell chạy uvicorn hoặc npm
    try {
        $uvicornProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" }
        foreach ($process in $uvicornProcesses) {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process Python/Uvicorn (PID: $($process.Id))" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $npmProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*npm*" }
        foreach ($process in $npmProcesses) {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            Write-Host "Đã dừng process Node/npm (PID: $($process.Id))" -ForegroundColor Green
        }
    } catch {}
    
    Write-Host "Tất cả các service đã dừng!" -ForegroundColor Green
}

# Hiển thị trợ giúp
function Show-Help {
    Write-Host "Sử dụng: .\run_venv.ps1 [lệnh]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Các lệnh:" -ForegroundColor White
    Write-Host "  start       Khởi động tất cả các service" -ForegroundColor Gray
    Write-Host "  stop        Dừng tất cả các service" -ForegroundColor Gray
    Write-Host "  user        Chỉ khởi động User Service" -ForegroundColor Gray
    Write-Host "  ticket      Chỉ khởi động Ticket Service" -ForegroundColor Gray
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
    "gateway" {
        Start-APIGateway
    }
    default {
        Show-Help
    }
}