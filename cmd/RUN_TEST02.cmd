@echo off
setlocal EnableExtensions
set "ROOT=%~dp0.."
set "PY=python"
if exist "%ROOT%\.venv\Scripts\python.exe" set "PY=%ROOT%\.venv\Scripts\python.exe"
"%PY%" "%ROOT%\src\amcf_local_main_test02.py" --frames 288
exit /b %ERRORLEVEL%
