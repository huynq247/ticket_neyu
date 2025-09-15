# PowerShell script d? ch?y các microservice tr?c ti?p trên Windows v?i Python 3.10
# Script này s? ch?y các service mà không c?n Docker, s? d?ng database t? xa

# Bi?n luu tr? Process ID c?a các service
$userServicePid = $null
$ticketServicePid = $null
$fileServicePid = $null
$notificationServicePid = $null
$reportServicePid = $null
$analyticsServicePid = $null
$apiGatewayPid = $null

# Ðu?ng d?n d?n môi tru?ng ?o Python 3.10
$pythonEnvPath = "$PSScriptRoot\venv_py310\Scripts\python.exe"

# Ki?m tra Python dã du?c cài d?t chua
function Test-Python {
    try {
        $pythonVersion = & $pythonEnvPath --version
        Write-Host "Python dã du?c cài d?t: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Python 3.10 chua du?c cài d?t ho?c môi tru?ng ?o không t?n t?i. Vui lòng cài d?t Python 3.10 và th? l?i." -ForegroundColor Red
        return $false
    }
}

# Ki?m tra Node.js dã du?c cài d?t chua
function Test-NodeJS {
    try {
        $nodeVersion = node --version
        Write-Host "Node.js dã du?c cài d?t: $nodeVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Node.js chua du?c cài d?t ho?c không có trong PATH. Vui lòng cài d?t Node.js 14+ và th? l?i." -ForegroundColor Red
        return $false
    }
}

# Ki?m tra các dependency cho Python
function Install-PythonDependencies {
    param (
        [string]$servicePath
    )
    
    if (-not (Test-Python)) { return $false }
    
    Write-Host "Ki?m tra và cài d?t các dependency Python cho $servicePath..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c service
    Set-Location -Path "$PSScriptRoot\services\$servicePath"
    
    # Cài d?t các dependency s? d?ng môi tru?ng Python 3.10
    & $pythonEnvPath -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Ðã cài d?t thành công các dependency cho $servicePath" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "L?i khi cài d?t dependency cho $servicePath" -ForegroundColor Red
        return $false
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ki?m tra các dependency cho Node.js
function Install-NodeDependencies {
    param (
        [string]$servicePath
    )
    
    if (-not (Test-NodeJS)) { return $false }
    
    Write-Host "Ki?m tra và cài d?t các dependency Node.js cho $servicePath..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c service
    Set-Location -Path "$PSScriptRoot\services\$servicePath"
    
    # Cài d?t các dependency
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Ðã cài d?t thành công các dependency cho $servicePath" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "L?i khi cài d?t dependency cho $servicePath" -ForegroundColor Red
        return $false
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y User Service
function Start-UserService {
    if (-not (Test-Python)) { return }
    
    # Cài d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "user-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "Ðang kh?i d?ng User Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c User Service
    Set-Location -Path "$PSScriptRoot\services\user-service"
    
    # Kh?i d?ng User Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:userServicePid = $process.Id
    
    if ($process) {
        Write-Host "User Service dã kh?i d?ng thành công (PID: $userServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không th? kh?i d?ng User Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Ticket Service
function Start-TicketService {
    if (-not (Test-Python)) { return }
    
    # Cài d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "ticket-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "Ðang kh?i d?ng Ticket Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Ticket Service
    Set-Location -Path "$PSScriptRoot\services\ticket-service"
    
    # Kh?i d?ng Ticket Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:ticketServicePid = $process.Id
    
    if ($process) {
        Write-Host "Ticket Service dã kh?i d?ng thành công (PID: $ticketServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8001/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không th? kh?i d?ng Ticket Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y File Service
function Start-FileService {
    if (-not (Test-Python)) { return }
    
    # Cài d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "file-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "Ðang kh?i d?ng File Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c File Service
    Set-Location -Path "$PSScriptRoot\services\file-service"
    
    # Kh?i d?ng File Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:fileServicePid = $process.Id
    
    if ($process) {
        Write-Host "File Service dã kh?i d?ng thành công (PID: $fileServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8002/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không th? kh?i d?ng File Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Notification Service
function Start-NotificationService {
    if (-not (Test-Python)) { return }
    
    # Cài d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "notification-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "Ðang kh?i d?ng Notification Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Notification Service
    Set-Location -Path "$PSScriptRoot\services\notification-service"
    
    # Kh?i d?ng Notification Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:notificationServicePid = $process.Id
    
    if ($process) {
        Write-Host "Notification Service dã kh?i d?ng thành công (PID: $notificationServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8003/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không th? kh?i d?ng Notification Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Report Service
function Start-ReportService {
    if (-not (Test-Python)) { return }
    
    # Cài d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "report-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "Ðang kh?i d?ng Report Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Report Service
    Set-Location -Path "$PSScriptRoot\services\report-service"
    
    # Kh?i d?ng Report Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:reportServicePid = $process.Id
    
    if ($process) {
        Write-Host "Report Service dã kh?i d?ng thành công (PID: $reportServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8004/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không th? kh?i d?ng Report Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Analytics Service
function Start-AnalyticsService {
    if (-not (Test-Python)) { return }
    
    # Cài d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "analytics-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "Ðang kh?i d?ng Analytics Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Analytics Service
    Set-Location -Path "$PSScriptRoot\services\analytics-service"
    
    # Kh?i d?ng Analytics Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:analyticsServicePid = $process.Id
    
    if ($process) {
        Write-Host "Analytics Service dã kh?i d?ng thành công (PID: $analyticsServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8005/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không th? kh?i d?ng Analytics Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y API Gateway
function Start-ApiGateway {
    if (-not (Test-NodeJS)) { return }
    
    # Cài d?t dependencies
    $depsInstalled = Install-NodeDependencies -servicePath "api-gateway"
    if (-not $depsInstalled) { return }
    
    Write-Host "Ðang kh?i d?ng API Gateway..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c API Gateway
    Set-Location -Path "$PSScriptRoot\services\api-gateway"
    
    # Kh?i d?ng API Gateway
    $process = Start-Process -FilePath "npm" -ArgumentList "start" -PassThru -NoNewWindow
    $script:apiGatewayPid = $process.Id
    
    if ($process) {
        Write-Host "API Gateway dã kh?i d?ng thành công (PID: $apiGatewayPid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8080" -ForegroundColor Cyan
    }
    else {
        Write-Host "Không th? kh?i d?ng API Gateway" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# D?ng t?t c? các service
function Stop-AllServices {
    Write-Host "Ðang d?ng t?t c? các service..." -ForegroundColor Yellow
    
    # D?ng t?t c? các process python và node dang ch?y
    Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*$PSScriptRoot*" } | Stop-Process -Force
    Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*$PSScriptRoot*" } | Stop-Process -Force
    
    Write-Host "Ðã d?ng t?t c? các service" -ForegroundColor Green
}

# X? lý tham s? dòng l?nh
$command = $args[0]

if ($command -eq "start") {
    # Kh?i d?ng t?t c? các service
    Start-UserService
    Start-TicketService
    Start-FileService
    Start-NotificationService
    Start-ReportService
    Start-AnalyticsService
    Start-ApiGateway
}
elseif ($command -eq "stop") {
    # D?ng t?t c? các service
    Stop-AllServices
}
elseif ($command -eq "user") {
    # Ch? ch?y User Service
    Start-UserService
}
elseif ($command -eq "ticket") {
    # Ch? ch?y Ticket Service
    Start-TicketService
}
elseif ($command -eq "file") {
    # Ch? ch?y File Service
    Start-FileService
}
elseif ($command -eq "notification") {
    # Ch? ch?y Notification Service
    Start-NotificationService
}
elseif ($command -eq "report") {
    # Ch? ch?y Report Service
    Start-ReportService
}
elseif ($command -eq "analytics") {
    # Ch? ch?y Analytics Service
    Start-AnalyticsService
}
elseif ($command -eq "gateway") {
    # Ch? ch?y API Gateway
    Start-ApiGateway
}
else {
    Write-Host "Cách s? d?ng: .\run_local_py310.ps1 [command]" -ForegroundColor Yellow
    Write-Host "Các l?nh h? tr?:" -ForegroundColor Yellow
    Write-Host "  start        - Kh?i d?ng t?t c? các service" -ForegroundColor Cyan
    Write-Host "  stop         - D?ng t?t c? các service" -ForegroundColor Cyan
    Write-Host "  user         - Ch? ch?y User Service" -ForegroundColor Cyan
    Write-Host "  ticket       - Ch? ch?y Ticket Service" -ForegroundColor Cyan
    Write-Host "  file         - Ch? ch?y File Service" -ForegroundColor Cyan
    Write-Host "  notification - Ch? ch?y Notification Service" -ForegroundColor Cyan
    Write-Host "  report       - Ch? ch?y Report Service" -ForegroundColor Cyan
    Write-Host "  analytics    - Ch? ch?y Analytics Service" -ForegroundColor Cyan
    Write-Host "  gateway      - Ch? ch?y API Gateway" -ForegroundColor Cyan
}
