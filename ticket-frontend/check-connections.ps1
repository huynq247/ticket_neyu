# check-connections.ps1
# PowerShell script để kiểm tra kết nối đến các microservices

Write-Host "Đang kiểm tra kết nối đến các microservices..." -ForegroundColor Cyan

# Tạo thư mục scripts nếu chưa tồn tại
$scriptDir = Join-Path -Path $PSScriptRoot -ChildPath "scripts"
if (-not (Test-Path -Path $scriptDir)) {
    New-Item -Path $scriptDir -ItemType Directory | Out-Null
}

# Kiểm tra xem Node.js đã được cài đặt chưa
try {
    $nodeVersion = node --version
    Write-Host "Node.js đã được cài đặt: $nodeVersion" -ForegroundColor Green
}
catch {
    Write-Host "Node.js chưa được cài đặt. Vui lòng cài đặt Node.js để chạy script này." -ForegroundColor Red
    exit 1
}

# Kiểm tra các package cần thiết
$requiredPackages = @("axios", "dotenv")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    try {
        $null = npm list --depth=0 $package
        if ($LASTEXITCODE -ne 0) {
            $missingPackages += $package
        }
    }
    catch {
        $missingPackages += $package
    }
}

# Cài đặt các package thiếu
if ($missingPackages.Count -gt 0) {
    Write-Host "Đang cài đặt các package cần thiết: $($missingPackages -join ', ')" -ForegroundColor Yellow
    npm install --no-save $missingPackages
}

# Chạy script kiểm tra kết nối
try {
    $checkScriptPath = Join-Path -Path $scriptDir -ChildPath "check-connections.js"
    node $checkScriptPath
}
catch {
    Write-Host "Lỗi khi chạy script kiểm tra kết nối: $_" -ForegroundColor Red
    exit 1
}