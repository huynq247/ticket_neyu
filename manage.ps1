# PowerShell script for managing ticket system services

# Check Docker installation
function Test-Docker {
    try {
        $dockerVersion = docker --version
        Write-Host "Docker is installed: $dockerVersion" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Docker is not installed or not in PATH. Please install Docker Desktop for Windows." -ForegroundColor Red
        return $false
    }
}

# Check if docker-compose or docker compose is available
function Get-DockerComposeCommand {
    try {
        # Try the newer format first (Docker Compose V2)
        docker compose version | Out-Null
        Write-Host "Using Docker Compose V2 command format" -ForegroundColor Green
        return "docker compose"
    }
    catch {
        try {
            # Try the older format
            docker-compose --version | Out-Null
            Write-Host "Using Docker Compose V1 command format" -ForegroundColor Green
            return "docker-compose"
        }
        catch {
            Write-Host "Docker Compose is not available. Please install Docker Desktop with Docker Compose." -ForegroundColor Red
            return $null
        }
    }
}

# Start services
function Start-Services {
    Write-Host "Starting ticket management system services..." -ForegroundColor Green
    
    if (-not (Test-Docker)) { return }
    
    $composeCmd = Get-DockerComposeCommand
    if ($null -eq $composeCmd) { return }
    
    Invoke-Expression "$composeCmd up -d"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Services started successfully!" -ForegroundColor Green
        Write-Host "API Gateway: http://localhost:3000" -ForegroundColor Cyan
        Write-Host "User Service: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "Ticket Service: http://localhost:8001" -ForegroundColor Cyan
    }
    else {
        Write-Host "Failed to start services. Check the Docker logs for more details." -ForegroundColor Red
    }
}

# Stop services
function Stop-Services {
    Write-Host "Stopping ticket management system services..." -ForegroundColor Yellow
    
    if (-not (Test-Docker)) { return }
    
    $composeCmd = Get-DockerComposeCommand
    if ($null -eq $composeCmd) { return }
    
    Invoke-Expression "$composeCmd down"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Services stopped successfully!" -ForegroundColor Green
    }
    else {
        Write-Host "Failed to stop services. Check the Docker logs for more details." -ForegroundColor Red
    }
}

# View logs
function Show-Logs {
    param (
        [string]$service
    )
    
    if (-not (Test-Docker)) { return }
    
    $composeCmd = Get-DockerComposeCommand
    if ($null -eq $composeCmd) { return }
    
    if ([string]::IsNullOrEmpty($service)) {
        Invoke-Expression "$composeCmd logs -f"
    } else {
        Invoke-Expression "$composeCmd logs -f $service"
    }
}

# Show help
function Show-Help {
    Write-Host "Usage: .\manage.ps1 [command]" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor White
    Write-Host "  start       Start all services" -ForegroundColor Gray
    Write-Host "  stop        Stop all services" -ForegroundColor Gray
    Write-Host "  restart     Restart all services" -ForegroundColor Gray
    Write-Host "  logs        View logs for all services" -ForegroundColor Gray
    Write-Host "  logs [name] View logs for a specific service (e.g., logs api-gateway)" -ForegroundColor Gray
    Write-Host "  help        Show this help message" -ForegroundColor Gray
}

# Process command
$command = $args[0]

switch ($command) {
    "start" {
        Start-Services
    }
    "stop" {
        Stop-Services
    }
    "restart" {
        Stop-Services
        Start-Services
    }
    "logs" {
        $service = $args[1]
        Show-Logs -service $service
    }
    default {
        Show-Help
    }
}