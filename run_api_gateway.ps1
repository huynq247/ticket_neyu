# PowerShell script to start the api gateway with Node.js
# This script addresses potential connection issues

# Change directory to api gateway service
Set-Location -Path "$PSScriptRoot\services\api-gateway"

# Install dependencies
Write-Host "Installing dependencies for api-gateway..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
    
    # Start api gateway with explicit port setting in a way that doesn't terminate when script completes
    Write-Host "Starting API Gateway on port 8080..." -ForegroundColor Yellow
    $env:PORT = 8080
    
    # Start Node.js in a new PowerShell window to keep it running
    Start-Process powershell.exe -ArgumentList "-NoExit -Command `"cd '$PSScriptRoot\services\api-gateway'; `$env:PORT = 8080; npm start`"" -WindowStyle Normal
    
    Write-Host "API Gateway has been started in a new window" -ForegroundColor Green
    Write-Host "Access at: http://localhost:8080" -ForegroundColor Cyan
}
else {
    Write-Host "Failed to install dependencies for api-gateway" -ForegroundColor Red
}

# Return to the original directory
Set-Location -Path $PSScriptRoot