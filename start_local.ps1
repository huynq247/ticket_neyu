# PowerShell script for starting services locally (without Docker)

# Global variables for process IDs
$userServicePid = $null
$apiGatewayPid = $null
$ticketServicePid = $null

# Function to check if Python is installed
function Test-Python {
    try {
        $pythonVersion = python --version
        Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Python is not installed or not in PATH. Please install Python 3.9+ and try again." -ForegroundColor Red
        return $false
    }
}

# Function to check if Node.js is installed
function Test-NodeJS {
    try {
        $nodeVersion = node --version
        Write-Host "Node.js is installed: $nodeVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Node.js is not installed or not in PATH. Please install Node.js 14+ and try again." -ForegroundColor Red
        return $false
    }
}

# Start User Service
function Start-UserService {
    if (-not (Test-Python)) { return }
    
    Write-Host "Starting User Service..." -ForegroundColor Green
    
    # Change to the user service directory
    Set-Location -Path "$PSScriptRoot\services\user-service"
    
    # Start the service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8000" -PassThru -NoNewWindow
    $script:userServicePid = $process.Id
    
    # Go back to the original directory
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "User Service started successfully (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Access at: http://localhost:8000/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Failed to start User Service" -ForegroundColor Red
    }
}

# Start Ticket Service
function Start-TicketService {
    if (-not (Test-Python)) { return }
    
    Write-Host "Starting Ticket Service..." -ForegroundColor Green
    
    # Change to the ticket service directory
    Set-Location -Path "$PSScriptRoot\services\ticket-service"
    
    # Start the service
    $process = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:app --host 0.0.0.0 --port 8001" -PassThru -NoNewWindow
    $script:ticketServicePid = $process.Id
    
    # Go back to the original directory
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "Ticket Service started successfully (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Access at: http://localhost:8001/docs" -ForegroundColor Cyan
    }
    else {
        Write-Host "Failed to start Ticket Service" -ForegroundColor Red
    }
}

# Start API Gateway
function Start-APIGateway {
    if (-not (Test-NodeJS)) { return }
    
    Write-Host "Starting API Gateway..." -ForegroundColor Green
    
    # Change to the API gateway directory
    Set-Location -Path "$PSScriptRoot\services\api-gateway"
    
    # Start the service
    $process = Start-Process -FilePath "npm" -ArgumentList "start" -PassThru -NoNewWindow
    $script:apiGatewayPid = $process.Id
    
    # Go back to the original directory
    Set-Location -Path $PSScriptRoot
    
    if ($process.Id -gt 0) {
        Write-Host "API Gateway started successfully (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "Access at: http://localhost:3000" -ForegroundColor Cyan
    }
    else {
        Write-Host "Failed to start API Gateway" -ForegroundColor Red
    }
}

# Start all services locally
function Start-LocalServices {
    Write-Host "Starting all services locally..." -ForegroundColor Green
    
    # Start services in sequence
    Start-UserService
    Start-TicketService
    Start-APIGateway
    
    Write-Host "All services started locally!" -ForegroundColor Green
    Write-Host "To stop the services, run: .\start_local.ps1 stop" -ForegroundColor Yellow
}

# Stop all services
function Stop-LocalServices {
    Write-Host "Stopping all services..." -ForegroundColor Yellow
    
    # Stop User Service
    if ($null -ne $script:userServicePid -and $script:userServicePid -gt 0) {
        try {
            Stop-Process -Id $script:userServicePid -Force
            Write-Host "User Service stopped successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to stop User Service: $_" -ForegroundColor Red
        }
    }
    
    # Stop Ticket Service
    if ($null -ne $script:ticketServicePid -and $script:ticketServicePid -gt 0) {
        try {
            Stop-Process -Id $script:ticketServicePid -Force
            Write-Host "Ticket Service stopped successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to stop Ticket Service: $_" -ForegroundColor Red
        }
    }
    
    # Stop API Gateway
    if ($null -ne $script:apiGatewayPid -and $script:apiGatewayPid -gt 0) {
        try {
            Stop-Process -Id $script:apiGatewayPid -Force
            Write-Host "API Gateway stopped successfully" -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to stop API Gateway: $_" -ForegroundColor Red
        }
    }
    
    # Also try to find and kill any lingering processes on the ports
    try {
        $port8000Process = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8000Process) {
            Stop-Process -Id $port8000Process -Force -ErrorAction SilentlyContinue
            Write-Host "Killed process on port 8000" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port8001Process = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port8001Process) {
            Stop-Process -Id $port8001Process -Force -ErrorAction SilentlyContinue
            Write-Host "Killed process on port 8001" -ForegroundColor Green
        }
    } catch {}
    
    try {
        $port3000Process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        if ($port3000Process) {
            Stop-Process -Id $port3000Process -Force -ErrorAction SilentlyContinue
            Write-Host "Killed process on port 3000" -ForegroundColor Green
        }
    } catch {}
    
    Write-Host "All services stopped!" -ForegroundColor Green
}

# Show help
function Show-LocalHelp {
    Write-Host "Usage: .\start_local.ps1 [command]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor White
    Write-Host "  start       Start all services locally" -ForegroundColor Gray
    Write-Host "  stop        Stop all local services" -ForegroundColor Gray
    Write-Host "  user        Start only the User Service" -ForegroundColor Gray
    Write-Host "  ticket      Start only the Ticket Service" -ForegroundColor Gray
    Write-Host "  gateway     Start only the API Gateway" -ForegroundColor Gray
    Write-Host "  help        Show this help message" -ForegroundColor Gray
}

# Process command
$command = $args[0]

switch ($command) {
    "start" {
        Start-LocalServices
    }
    "stop" {
        Stop-LocalServices
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
        Show-LocalHelp
    }
}