# PowerShell script d? ch?y c�c microservice tr?c ti?p tr�n Windows v?i Python 3.10
# Script n�y s? ch?y c�c service m� kh�ng c?n Docker, s? d?ng database t? xa

# Bi?n luu tr? Process ID c?a c�c service
$userServicePid = $null
$ticketServicePid = $null
$fileServicePid = $null
$notificationServicePid = $null
$reportServicePid = $null
$analyticsServicePid = $null
$apiGatewayPid = $null

# �u?ng d?n d?n m�i tru?ng ?o Python 3.10
$pythonEnvPath = "$PSScriptRoot\venv_py310\Scripts\python.exe"

# Ki?m tra Python d� du?c c�i d?t chua
function Test-Python {
    try {
        $pythonVersion = & $pythonEnvPath --version
        Write-Host "Python d� du?c c�i d?t: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Python 3.10 chua du?c c�i d?t ho?c m�i tru?ng ?o kh�ng t?n t?i. Vui l�ng c�i d?t Python 3.10 v� th? l?i." -ForegroundColor Red
        return $false
    }
}

# Ki?m tra Node.js d� du?c c�i d?t chua
function Test-NodeJS {
    try {
        $nodeVersion = node --version
        Write-Host "Node.js d� du?c c�i d?t: $nodeVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Node.js chua du?c c�i d?t ho?c kh�ng c� trong PATH. Vui l�ng c�i d?t Node.js 14+ v� th? l?i." -ForegroundColor Red
        return $false
    }
}

# Ki?m tra c�c dependency cho Python
function Install-PythonDependencies {
    param (
        [string]$servicePath
    )
    
    if (-not (Test-Python)) { return $false }
    
    Write-Host "Ki?m tra v� c�i d?t c�c dependency Python cho $servicePath..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c service
    Set-Location -Path "$PSScriptRoot\services\$servicePath"
    
    # C�i d?t c�c dependency s? d?ng m�i tru?ng Python 3.10
    & $pythonEnvPath -m pip install -r requirements.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "�� c�i d?t th�nh c�ng c�c dependency cho $servicePath" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "L?i khi c�i d?t dependency cho $servicePath" -ForegroundColor Red
        return $false
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ki?m tra c�c dependency cho Node.js
function Install-NodeDependencies {
    param (
        [string]$servicePath
    )
    
    if (-not (Test-NodeJS)) { return $false }
    
    Write-Host "Ki?m tra v� c�i d?t c�c dependency Node.js cho $servicePath..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c service
    Set-Location -Path "$PSScriptRoot\services\$servicePath"
    
    # C�i d?t c�c dependency
    npm install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "�� c�i d?t th�nh c�ng c�c dependency cho $servicePath" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "L?i khi c�i d?t dependency cho $servicePath" -ForegroundColor Red
        return $false
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y User Service
function Start-UserService {
    if (-not (Test-Python)) { return }
    
    # C�i d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "user-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "�ang kh?i d?ng User Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c User Service
    Set-Location -Path "$PSScriptRoot\services\user-service"
    
    # Kh?i d?ng User Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:userServicePid = $process.Id
    
    if ($process) {
        Write-Host "User Service d� kh?i d?ng th�nh c�ng (PID: $userServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Kh�ng th? kh?i d?ng User Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Ticket Service
function Start-TicketService {
    if (-not (Test-Python)) { return }
    
    # C�i d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "ticket-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "�ang kh?i d?ng Ticket Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Ticket Service
    Set-Location -Path "$PSScriptRoot\services\ticket-service"
    
    # Kh?i d?ng Ticket Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:ticketServicePid = $process.Id
    
    if ($process) {
        Write-Host "Ticket Service d� kh?i d?ng th�nh c�ng (PID: $ticketServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8001/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Kh�ng th? kh?i d?ng Ticket Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y File Service
function Start-FileService {
    if (-not (Test-Python)) { return }
    
    # C�i d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "file-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "�ang kh?i d?ng File Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c File Service
    Set-Location -Path "$PSScriptRoot\services\file-service"
    
    # Kh?i d?ng File Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:fileServicePid = $process.Id
    
    if ($process) {
        Write-Host "File Service d� kh?i d?ng th�nh c�ng (PID: $fileServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8002/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Kh�ng th? kh?i d?ng File Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Notification Service
function Start-NotificationService {
    if (-not (Test-Python)) { return }
    
    # C�i d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "notification-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "�ang kh?i d?ng Notification Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Notification Service
    Set-Location -Path "$PSScriptRoot\services\notification-service"
    
    # Kh?i d?ng Notification Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:notificationServicePid = $process.Id
    
    if ($process) {
        Write-Host "Notification Service d� kh?i d?ng th�nh c�ng (PID: $notificationServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8003/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Kh�ng th? kh?i d?ng Notification Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Report Service
function Start-ReportService {
    if (-not (Test-Python)) { return }
    
    # C�i d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "report-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "�ang kh?i d?ng Report Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Report Service
    Set-Location -Path "$PSScriptRoot\services\report-service"
    
    # Kh?i d?ng Report Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:reportServicePid = $process.Id
    
    if ($process) {
        Write-Host "Report Service d� kh?i d?ng th�nh c�ng (PID: $reportServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8004/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Kh�ng th? kh?i d?ng Report Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y Analytics Service
function Start-AnalyticsService {
    if (-not (Test-Python)) { return }
    
    # C�i d?t dependencies
    $depsInstalled = Install-PythonDependencies -servicePath "analytics-service"
    if (-not $depsInstalled) { return }
    
    Write-Host "�ang kh?i d?ng Analytics Service..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c Analytics Service
    Set-Location -Path "$PSScriptRoot\services\analytics-service"
    
    # Kh?i d?ng Analytics Service
    $process = Start-Process -FilePath $pythonEnvPath -ArgumentList "main.py" -PassThru -NoNewWindow
    $script:analyticsServicePid = $process.Id
    
    if ($process) {
        Write-Host "Analytics Service d� kh?i d?ng th�nh c�ng (PID: $analyticsServicePid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8005/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Kh�ng th? kh?i d?ng Analytics Service" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# Ch?y API Gateway
function Start-ApiGateway {
    if (-not (Test-NodeJS)) { return }
    
    # C�i d?t dependencies
    $depsInstalled = Install-NodeDependencies -servicePath "api-gateway"
    if (-not $depsInstalled) { return }
    
    Write-Host "�ang kh?i d?ng API Gateway..." -ForegroundColor Yellow
    
    # Chuy?n d?n thu m?c API Gateway
    Set-Location -Path "$PSScriptRoot\services\api-gateway"
    
    # Kh?i d?ng API Gateway
    $process = Start-Process -FilePath "npm" -ArgumentList "start" -PassThru -NoNewWindow
    $script:apiGatewayPid = $process.Id
    
    if ($process) {
        Write-Host "API Gateway d� kh?i d?ng th�nh c�ng (PID: $apiGatewayPid)" -ForegroundColor Green
        Write-Host "Truy c?p t?i: http://localhost:8080" -ForegroundColor Cyan
    }
    else {
        Write-Host "Kh�ng th? kh?i d?ng API Gateway" -ForegroundColor Red
    }
    
    # Tr? v? thu m?c g?c
    Set-Location -Path $PSScriptRoot
}

# D?ng t?t c? c�c service
function Stop-AllServices {
    Write-Host "�ang d?ng t?t c? c�c service..." -ForegroundColor Yellow
    
    # D?ng t?t c? c�c process python v� node dang ch?y
    Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*$PSScriptRoot*" } | Stop-Process -Force
    Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*$PSScriptRoot*" } | Stop-Process -Force
    
    Write-Host "�� d?ng t?t c? c�c service" -ForegroundColor Green
}

# X? l� tham s? d�ng l?nh
$command = $args[0]

if ($command -eq "start") {
    # Kh?i d?ng t?t c? c�c service
    Start-UserService
    Start-TicketService
    Start-FileService
    Start-NotificationService
    Start-ReportService
    Start-AnalyticsService
    Start-ApiGateway
}
elseif ($command -eq "stop") {
    # D?ng t?t c? c�c service
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
    Write-Host "C�ch s? d?ng: .\run_local_py310.ps1 [command]" -ForegroundColor Yellow
    Write-Host "C�c l?nh h? tr?:" -ForegroundColor Yellow
    Write-Host "  start        - Kh?i d?ng t?t c? c�c service" -ForegroundColor Cyan
    Write-Host "  stop         - D?ng t?t c? c�c service" -ForegroundColor Cyan
    Write-Host "  user         - Ch? ch?y User Service" -ForegroundColor Cyan
    Write-Host "  ticket       - Ch? ch?y Ticket Service" -ForegroundColor Cyan
    Write-Host "  file         - Ch? ch?y File Service" -ForegroundColor Cyan
    Write-Host "  notification - Ch? ch?y Notification Service" -ForegroundColor Cyan
    Write-Host "  report       - Ch? ch?y Report Service" -ForegroundColor Cyan
    Write-Host "  analytics    - Ch? ch?y Analytics Service" -ForegroundColor Cyan
    Write-Host "  gateway      - Ch? ch?y API Gateway" -ForegroundColor Cyan
}
