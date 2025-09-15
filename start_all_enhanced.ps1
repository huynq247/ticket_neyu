# PowerShell script to start all microservices with Python 3.10
# This script starts all backend services in separate windows for easier monitoring

# Path to Python 3.10 environment
$pythonPath = "$PSScriptRoot\venv_py310\Scripts\python.exe"

# Check if Python 3.10 is available
$pythonExists = Test-Path -Path $pythonPath
if (-not $pythonExists) {
    Write-Host "Python 3.10 environment not found at $pythonPath" -ForegroundColor Red
    Write-Host "Please make sure you have set up the Python 3.10 environment." -ForegroundColor Red
    exit 1
}

# Function to start a service in a new PowerShell window
function Start-ServiceInNewWindow {
    param (
        [string]$ServiceName,
        [string]$ScriptPath
    )
    
    Write-Host "Starting $ServiceName in a new window..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoExit -File `"$ScriptPath`"" -WindowStyle Normal
    Start-Sleep -Seconds 2  # Give a small delay between starting services
}

# Start User Service
Start-ServiceInNewWindow -ServiceName "User Service" -ScriptPath "$PSScriptRoot\run_local_py310.ps1 user"

# Start Ticket Service
Start-ServiceInNewWindow -ServiceName "Ticket Service" -ScriptPath "$PSScriptRoot\run_local_py310.ps1 ticket"

# Start File Service
Start-ServiceInNewWindow -ServiceName "File Service" -ScriptPath "$PSScriptRoot\run_file_service.ps1"

# Start Notification Service
Start-ServiceInNewWindow -ServiceName "Notification Service" -ScriptPath "$PSScriptRoot\run_notification_service.ps1"

# Start Report Service
Start-ServiceInNewWindow -ServiceName "Report Service" -ScriptPath "$PSScriptRoot\run_report_service.ps1"

# Start Analytics Service
Start-ServiceInNewWindow -ServiceName "Analytics Service" -ScriptPath "$PSScriptRoot\run_analytics_service.ps1"

# Start API Gateway
Start-ServiceInNewWindow -ServiceName "API Gateway" -ScriptPath "$PSScriptRoot\run_api_gateway.ps1"

Write-Host "All services have been started in separate windows." -ForegroundColor Green
Write-Host "Service endpoints:" -ForegroundColor Cyan
Write-Host "- User Service:        http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "- Ticket Service:      http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "- File Service:        http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "- Notification Service: http://localhost:8003/docs" -ForegroundColor Cyan
Write-Host "- Report Service:      http://localhost:8004/docs" -ForegroundColor Cyan
Write-Host "- Analytics Service:   http://localhost:8005/docs" -ForegroundColor Cyan
Write-Host "- API Gateway:         http://localhost:8080" -ForegroundColor Cyan