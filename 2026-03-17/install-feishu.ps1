#Requires -RunAsAdministrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     Feishu (Lark) Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
Write-Host "Checking if Feishu is already installed..." -ForegroundColor Yellow
$feishuPath = "${env:LOCALAPPDATA}\Programs\Lark\Lark.exe"
$feishuPath2 = "${env:ProgramFiles(x86)}\Lark\Lark.exe"
$feishuPath3 = "${env:ProgramFiles}\Lark\Lark.exe"

$installed = $false
$installLocation = ""

if (Test-Path $feishuPath) {
    $installed = $true
    $installLocation = $feishuPath
} elseif (Test-Path $feishuPath2) {
    $installed = $true
    $installLocation = $feishuPath2
} elseif (Test-Path $feishuPath3) {
    $installed = $true
    $installLocation = $feishuPath3
}

if ($installed) {
    Write-Host "Feishu is already installed at:" -ForegroundColor Green
    Write-Host "  $installLocation" -ForegroundColor Gray
    Write-Host ""
    $reinstall = Read-Host "Do you want to reinstall? (y/N)"
    if ($reinstall -ne "y" -and $reinstall -ne "Y") {
        Write-Host "Skipping installation. Launching Feishu..." -ForegroundColor Yellow
        Start-Process $installLocation
        Read-Host "Press Enter to exit"
        exit
    }
}

# Download Feishu
Write-Host ""
Write-Host "Step 1/2: Downloading Feishu..." -ForegroundColor Green

$downloadUrl = "https://www.feishu.cn/api/download?type=exe"
$installerPath = "$env:TEMP\FeishuInstaller.exe"

if (Test-Path $installerPath) {
    Write-Host "Installer already exists, skipping download" -ForegroundColor Gray
} else {
    Write-Host "Downloading Feishu installer..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing -MaximumRedirection 10
        Write-Host "Download completed" -ForegroundColor Green
    } catch {
        Write-Host "Download failed from official site, trying mirror..." -ForegroundColor Yellow
        # Alternative download link
        $altUrl = "https://sf3-cn.feishucdn.com/obj/ee-appcenter/5d3d8d/Feishu-win32_ia32-7.32.6.exe"
        try {
            Invoke-WebRequest -Uri $altUrl -OutFile $installerPath -UseBasicParsing
            Write-Host "Download completed from mirror" -ForegroundColor Green
        } catch {
            Write-Host "Download failed. Please download manually from:" -ForegroundColor Red
            Write-Host "  https://www.feishu.cn/download" -ForegroundColor Yellow
            Read-Host "Press Enter to exit"
            exit
        }
    }
}

# Install Feishu
Write-Host ""
Write-Host "Step 2/2: Installing Feishu..." -ForegroundColor Green
Write-Host "Installation may take a few minutes..." -ForegroundColor Yellow

try {
    Start-Process -FilePath $installerPath -ArgumentList "/S" -Wait
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "     Installation Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "Installation may require manual steps." -ForegroundColor Yellow
    Write-Host "Please complete the installation wizard." -ForegroundColor Yellow
    Start-Process -FilePath $installerPath
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow

Start-Sleep -Seconds 3

$feishuPath = "${env:LOCALAPPDATA}\Programs\Lark\Lark.exe"
if (Test-Path $feishuPath) {
    Write-Host "Feishu installed successfully!" -ForegroundColor Green
    Write-Host "Location: $feishuPath" -ForegroundColor Gray
    
    $launch = Read-Host "Do you want to launch Feishu now? (Y/n)"
    if ($launch -ne "n" -and $launch -ne "N") {
        Start-Process $feishuPath
        Write-Host "Feishu is starting..." -ForegroundColor Green
    }
} else {
    Write-Host "Installation verification failed." -ForegroundColor Yellow
    Write-Host "Please check Start Menu for Feishu." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"