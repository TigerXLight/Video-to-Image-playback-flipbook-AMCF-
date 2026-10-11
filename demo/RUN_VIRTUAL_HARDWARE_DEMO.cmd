@echo off
setlocal
cd /d "%~dp0.."
set "PY=python"
where py >nul 2>nul
if %ERRORLEVEL%==0 set "PY=py -3"
%PY% "demo\run_virtual_hardware_demo.py"
exit /b %ERRORLEVEL%
