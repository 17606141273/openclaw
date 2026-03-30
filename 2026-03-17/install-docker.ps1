#Requires -RunAsAdministrator

# Check admin rights
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Please run as administrator" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     Docker Installation Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
$dockerPath = Get-Command docker -ErrorAction SilentlyContinue
if ($dockerPath) {
    Write-Host "Docker is already installed:" -ForegroundColor Green
    docker --version
    Write-Host ""
}

# Check Windows version
Write-Host "Checking system environment..." -ForegroundColor Yellow
$osInfo = Get-CimInstance Win32_OperatingSystem
$osVersion = [System.Version]$osInfo.Version

Write-Host "OS: $($osInfo.Caption)" -ForegroundColor Gray
Write-Host "Version: $($osInfo.Version)" -ForegroundColor Gray

if ($osVersion -lt [System.Version]"10.0.19041") {
    Write-Host "Error: Windows 10 version 2004 or higher is required" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit
}

# Install WSL2
Write-Host ""
Write-Host "Step 1/4: Installing WSL2..." -ForegroundColor Green
wsl --update
wsl --install --no-distribution

# Enable container features
Write-Host ""
Write-Host "Step 2/4: Enabling container features..." -ForegroundColor Green
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Download Docker Desktop
Write-Host ""
Write-Host "Step 3/4: Downloading Docker Desktop..." -ForegroundColor Green
$dockerInstaller = "$env:TEMP\DockerDesktopInstaller.exe"

if (Test-Path $dockerInstaller) {
    Write-Host "Installer already exists, skipping download" -ForegroundColor Gray
} else {
    Write-Host "Downloading Docker Desktop (about 500MB, please wait)..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -OutFile $dockerInstaller -UseBasicParsing
        Write-Host "Download completed" -ForegroundColor Green
    } catch {
        Write-Host "Download failed, trying mirror..." -ForegroundColor Yellow
        Invoke-WebRequest -Uri "https://mirrors.aliyun.com/docker-toolbox/windows/docker-desktop/Docker%20Desktop%20Installer.exe" -OutFile $dockerInstaller -UseBasicParsing
    }
}

# Install Docker Desktop
Write-Host ""
Write-Host "Step 4/4: Installing Docker Desktop..." -ForegroundColor Green
Write-Host "Installation may take a few minutes, please wait..." -ForegroundColor Yellow

Start-Process -FilePath $dockerInstaller -ArgumentList "install --quiet --accept-license" -Wait

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "     Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Please restart your computer to complete the installation" -ForegroundColor Yellow
Write-Host ""

# Verify installation
Write-Host "Verifying Docker installation..." -ForegroundColor Yellow

$retry = 0
$maxRetries = 3
$success = $false

while ($retry -lt $maxRetries) {
    $dockerCheck = Get-Command docker -ErrorAction SilentlyContinue
    if ($dockerCheck) {
        Write-Host ""
        Write-Host "Docker version info:" -ForegroundColor Green
        docker --version
        
        Write-Host ""
        Write-Host "Running test container..." -ForegroundColor Yellow
        docker run --rm hello-world 2>$null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "Docker is installed and working correctly!" -ForegroundColor Green
            $success = $true
        } else {
            Write-Host ""
            Write-Host "Docker is installed but service may not be running" -ForegroundColor Yellow
            Write-Host "Please restart your computer and try again" -ForegroundColor Yellow
        }
        break
    } else {
        $retry = $retry + 1
        if ($retry -lt $maxRetries) {
            Write-Host "Waiting for Docker to be ready... ($retry/$maxRetries)" -ForegroundColor Gray
            Start-Sleep -Seconds 5
        }
    }
}

if ((-not $success) -and ($retry -eq $maxRetries)) {
    Write-Host ""
    Write-Host "Docker command not detected" -ForegroundColor Yellow
    Write-Host "Please restart your computer and run this script again to verify" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Common commands:" -ForegroundColor Cyan
Write-Host "  docker --version      # Check version" -ForegroundColor Gray
Write-Host "  docker ps             # List running containers" -ForegroundColor Gray
Write-Host "  docker run hello-world # Run test" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to exit"