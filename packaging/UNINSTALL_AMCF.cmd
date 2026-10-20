@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0uninstall_amcf.ps1" %*
if errorlevel 1 (
  echo AMCF uninstallation failed.
  exit /b 1
)
echo AMCF uninstalled successfully.
