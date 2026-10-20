@echo off
setlocal EnableExtensions
set "ROOT=%~dp0.."
set "PY=python"
if exist "%ROOT%\.venv\Scripts\python.exe" set "PY=%ROOT%\.venv\Scripts\python.exe"
"%PY%" "%ROOT%\src\amcf_local_main_tracking_test03a.py"
exit /b %ERRORLEVEL%
