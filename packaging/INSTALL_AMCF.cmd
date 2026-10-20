@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_amcf.ps1" %*
if errorlevel 1 (
  echo AMCF installation failed.
  exit /b 1
)
echo AMCF installed successfully.
