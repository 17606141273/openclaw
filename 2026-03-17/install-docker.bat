@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo      Docker Installer
echo ========================================
echo.

:: Check admin rights
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

echo Administrator privileges granted.
echo Starting installation...
echo.

:: Run PowerShell script
powershell -ExecutionPolicy Bypass -Command "& 'D:\AI_Files\install-docker.ps1'"

pause