# PowerShell script to start all backend microservices and frontend
# This script uses Python 3.10 for all Python services

# Set window title to make it easier to identify
$Host.UI.RawUI.WindowTitle = "All Microservices Controller"

Write-Host "Starting all backend microservices and frontend using Python 3.10..." -ForegroundColor Cyan
Write-Host "This script will start the following services in separate windows:" -ForegroundColor Yellow
Write-Host "1. User Service (Python)" -ForegroundColor White
Write-Host "2. Ticket Service (Python)" -ForegroundColor White
Write-Host "3. File Service (Python)" -ForegroundColor White
Write-Host "4. Notification Service (Python)" -ForegroundColor White
Write-Host "5. Report Service (Python)" -ForegroundColor White
Write-Host "6. Analytics Service (Python)" -ForegroundColor White
Write-Host "7. API Gateway (Node.js)" -ForegroundColor White
Write-Host "8. Frontend (if requested)" -ForegroundColor White

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
        [string]$ScriptPath,
        [string]$WindowTitle
    )
    
    Write-Host "Starting $ServiceName in a new window..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-NoExit -Command `"& {`$Host.UI.RawUI.WindowTitle = '$WindowTitle'; & '$ScriptPath'}`"" -WindowStyle Normal
    Start-Sleep -Seconds 2  # Give a small delay between starting services
}

# Start User Service
Start-ServiceInNewWindow -ServiceName "User Service" -ScriptPath "$PSScriptRoot\run_local_py310.ps1 user" -WindowTitle "User Service (8000)"

# Start Ticket Service
Start-ServiceInNewWindow -ServiceName "Ticket Service" -ScriptPath "$PSScriptRoot\run_local_py310.ps1 ticket" -WindowTitle "Ticket Service (8001)"

# Start File Service
Start-ServiceInNewWindow -ServiceName "File Service" -ScriptPath "$PSScriptRoot\run_file_service.ps1" -WindowTitle "File Service (8002)"

# Start Notification Service
Start-ServiceInNewWindow -ServiceName "Notification Service" -ScriptPath "$PSScriptRoot\run_notification_service.ps1" -WindowTitle "Notification Service (8003)"

# Start Report Service
Start-ServiceInNewWindow -ServiceName "Report Service" -ScriptPath "$PSScriptRoot\run_report_service.ps1" -WindowTitle "Report Service (8004)"

# Start Analytics Service
Start-ServiceInNewWindow -ServiceName "Analytics Service" -ScriptPath "$PSScriptRoot\run_analytics_service.ps1" -WindowTitle "Analytics Service (8005)"

# Start API Gateway
Start-ServiceInNewWindow -ServiceName "API Gateway" -ScriptPath "$PSScriptRoot\run_api_gateway.ps1" -WindowTitle "API Gateway (8080)"

# Ask if frontend should be started
$startFrontend = Read-Host "Do you want to start the frontend as well? (y/n)"
if ($startFrontend -eq "y" -or $startFrontend -eq "Y") {
    # Start frontend
    Start-ServiceInNewWindow -ServiceName "Frontend" -ScriptPath "$PSScriptRoot\ticket-frontend\manage.ps1 start" -WindowTitle "Frontend"
}

Write-Host "All services have been started in separate windows." -ForegroundColor Green
Write-Host "Service endpoints:" -ForegroundColor Cyan
Write-Host "- User Service:        http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "- Ticket Service:      http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host "- File Service:        http://localhost:8002/docs" -ForegroundColor Cyan
Write-Host "- Notification Service: http://localhost:8003/docs" -ForegroundColor Cyan
Write-Host "- Report Service:      http://localhost:8004/docs" -ForegroundColor Cyan
Write-Host "- Analytics Service:   http://localhost:8005/docs" -ForegroundColor Cyan
Write-Host "- API Gateway:         http://localhost:8080" -ForegroundColor Cyan
Write-Host "- Frontend (if started): http://localhost:3000" -ForegroundColor Cyan