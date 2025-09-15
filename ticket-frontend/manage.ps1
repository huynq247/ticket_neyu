# PowerShell script để giúp quản lý dự án Ticket Frontend
# Script này cung cấp các lệnh để chạy các tác vụ phổ biến và hiển thị thông tin hữu ích

param (
    [string]$Command = "help",
    [string]$Param1 = ""
)

$ProjectRoot = $PSScriptRoot
$EnvFile = Join-Path -Path $ProjectRoot -ChildPath ".env"
$EnvExampleFile = Join-Path -Path $ProjectRoot -ChildPath ".env.example"
$PackageJsonFile = Join-Path -Path $ProjectRoot -ChildPath "package.json"

# Kiểm tra xem Node.js đã được cài đặt chưa
function Test-NodeJS {
    try {
        $nodeVersion = node --version
        return $true
    }
    catch {
        return $false
    }
}

# Khởi động môi trường phát triển
function Start-DevEnvironment {
    Write-Host "Đang khởi động môi trường phát triển..." -ForegroundColor Cyan
    
    # Kiểm tra file .env
    if (-not (Test-Path -Path $EnvFile)) {
        Write-Host "File .env không tồn tại, đang tạo từ file mẫu..." -ForegroundColor Yellow
        Copy-Item -Path $EnvExampleFile -Destination $EnvFile
    }
    
    # Chạy npm dev
    npm run dev
}

# Kiểm tra trạng thái các service
function Check-Services {
    Write-Host "Đang kiểm tra trạng thái các service..." -ForegroundColor Cyan
    
    # Chạy script kiểm tra kết nối
    npm run check-connections
}

# Build dự án
function Build-Project {
    param (
        [string]$Mode = "production"
    )
    
    Write-Host "Đang build dự án cho môi trường $Mode..." -ForegroundColor Cyan
    
    if ($Mode -eq "production") {
        npm run build
    }
    else {
        # Với môi trường khác, có thể thêm xử lý đặc biệt ở đây
        npm run build
    }
}

# Hiển thị thông tin dự án
function Show-ProjectInfo {
    Write-Host "=== THÔNG TIN DỰ ÁN ===" -ForegroundColor Cyan
    
    # Đọc thông tin từ package.json
    $packageJson = Get-Content -Path $PackageJsonFile -Raw | ConvertFrom-Json
    
    Write-Host "Tên dự án: $($packageJson.name)" -ForegroundColor White
    Write-Host "Phiên bản: $($packageJson.version)" -ForegroundColor White
    Write-Host "Mô tả: $($packageJson.description)" -ForegroundColor White
    
    # Hiển thị scripts có sẵn
    Write-Host "`nScripts có sẵn:" -ForegroundColor Cyan
    $packageJson.scripts.PSObject.Properties | ForEach-Object {
        Write-Host "  - $($_.Name): $($_.Value)" -ForegroundColor Gray
    }
    
    # Hiển thị thông tin môi trường
    Write-Host "`nCấu hình môi trường:" -ForegroundColor Cyan
    if (Test-Path -Path $EnvFile) {
        Get-Content -Path $EnvFile | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '\S' } | ForEach-Object {
            $parts = $_ -split '=', 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                Write-Host "  - $key = $value" -ForegroundColor Gray
            }
        }
    }
    else {
        Write-Host "  File .env không tồn tại!" -ForegroundColor Yellow
    }
}

# Hiển thị trợ giúp
function Show-Help {
    Write-Host "=== TICKET FRONTEND DEVELOPMENT HELPER ===" -ForegroundColor Cyan
    Write-Host "Sử dụng: .\manage.ps1 [lệnh] [tham số]" -ForegroundColor White
    Write-Host "`nCác lệnh:" -ForegroundColor Cyan
    Write-Host "  dev          Khởi động môi trường phát triển" -ForegroundColor Gray
    Write-Host "  check        Kiểm tra trạng thái các service" -ForegroundColor Gray
    Write-Host "  build        Build dự án (mặc định cho production)" -ForegroundColor Gray
    Write-Host "  info         Hiển thị thông tin dự án" -ForegroundColor Gray
    Write-Host "  help         Hiển thị trợ giúp này" -ForegroundColor Gray
    
    Write-Host "`nVí dụ:" -ForegroundColor Cyan
    Write-Host "  .\manage.ps1 dev" -ForegroundColor Gray
    Write-Host "  .\manage.ps1 build production" -ForegroundColor Gray
}

# Thực thi lệnh
if (-not (Test-NodeJS)) {
    Write-Host "Node.js chưa được cài đặt. Vui lòng cài đặt Node.js để sử dụng script này." -ForegroundColor Red
    exit 1
}

switch ($Command.ToLower()) {
    "dev" {
        Start-DevEnvironment
    }
    "check" {
        Check-Services
    }
    "build" {
        Build-Project -Mode $Param1
    }
    "info" {
        Show-ProjectInfo
    }
    default {
        Show-Help
    }
}