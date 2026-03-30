#Requires -RunAsAdministrator

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     Docker Installation Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Docker command exists
Write-Host "[1/5] Checking if Docker command exists..." -ForegroundColor Yellow
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if ($dockerCmd) {
    Write-Host "      PASS - Docker command found" -ForegroundColor Green
    Write-Host "      Location: $($dockerCmd.Source)" -ForegroundColor Gray
} else {
    Write-Host "      FAIL - Docker command not found" -ForegroundColor Red
    Write-Host "      Docker may not be installed or not in PATH" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit
}

# Check 2: Docker version
Write-Host ""
Write-Host "[2/5] Checking Docker version..." -ForegroundColor Yellow
try {
    $version = docker --version 2>&1
    Write-Host "      PASS - $version" -ForegroundColor Green
} catch {
    Write-Host "      FAIL - Cannot get Docker version" -ForegroundColor Red
    Write-Host "      Error: $_" -ForegroundColor Yellow
}

# Check 3: Docker Desktop service
Write-Host ""
Write-Host "[3/5] Checking Docker Desktop service..." -ForegroundColor Yellow
$service = Get-Service -Name "com.docker.service" -ErrorAction SilentlyContinue
if ($service) {
    Write-Host "      Service found: $($service.Status)" -ForegroundColor $(if ($service.Status -eq "Running") { "Green" } else { "Yellow" })
    if ($service.Status -ne "Running") {
        Write-Host "      Starting service..." -ForegroundColor Yellow
        Start-Service -Name "com.docker.service" -ErrorAction SilentlyContinue
    }
} else {
    Write-Host "      Service not found (may use WSL2 backend)" -ForegroundColor Gray
}

# Check 4: Docker info
Write-Host ""
Write-Host "[4/5] Checking Docker daemon..." -ForegroundColor Yellow
try {
    $info = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      PASS - Docker daemon is running" -ForegroundColor Green
        # Extract some useful info
        $os = $info | Select-String "OS Type"
        $serverVersion = $info | Select-String "Server Version"
        if ($os) { Write-Host "      $os" -ForegroundColor Gray }
        if ($serverVersion) { Write-Host "      $serverVersion" -ForegroundColor Gray }
    } else {
        Write-Host "      FAIL - Docker daemon not responding" -ForegroundColor Red
        Write-Host "      Please start Docker Desktop" -ForegroundColor Yellow
    }
} catch {
    Write-Host "      FAIL - Cannot connect to Docker daemon" -ForegroundColor Red
    Write-Host "      Error: $_" -ForegroundColor Yellow
}

# Check 5: Run test container
Write-Host ""
Write-Host "[5/5] Running test container..." -ForegroundColor Yellow
try {
    $testResult = docker run --rm hello-world 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "      PASS - Test container ran successfully" -ForegroundColor Green
        $msg = $testResult | Select-String "Hello from Docker"
        if ($msg) { Write-Host "      $msg" -ForegroundColor Gray }
    } else {
        Write-Host "      FAIL - Test container failed" -ForegroundColor Red
    }
} catch {
    Write-Host "      FAIL - Cannot run test container" -ForegroundColor Red
    Write-Host "      Error: $_" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "     Check Complete" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check WSL
Write-Host "WSL Status:" -ForegroundColor Yellow
$wsl = wsl --status 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "$wsl" -ForegroundColor Gray
} else {
    Write-Host "WSL not configured" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Common Docker commands:" -ForegroundColor Cyan
Write-Host "  docker --version          # Check version" -ForegroundColor Gray
Write-Host "  docker info               # Show system info" -ForegroundColor Gray
Write-Host "  docker ps                 # List running containers" -ForegroundColor Gray
Write-Host "  docker images             # List images" -ForegroundColor Gray
Write-Host "  docker run hello-world    # Run test" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to exit"