@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo      Docker Installation Check
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
echo.

:: Run PowerShell check script
powershell -ExecutionPolicy Bypass -Command "& 'D:\AI_Files\check-docker.ps1'"

pause