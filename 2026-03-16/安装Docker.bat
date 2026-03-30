@echo off
chcp 65001 >nul
echo ========================================
echo      Docker 安装程序
echo ========================================
echo.

:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 需要管理员权限，正在申请...
    echo.
    :: 重新以管理员身份运行
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

echo 已获得管理员权限，正在启动安装脚本...
echo.

:: 运行 PowerShell 脚本
powershell -ExecutionPolicy Bypass -File "D:\AI_Files\install-docker.ps1"

pause