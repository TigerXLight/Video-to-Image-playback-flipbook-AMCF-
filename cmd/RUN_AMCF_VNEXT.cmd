@echo off
setlocal
cd /d "%~dp0.."
set "PY=python"
where py >nul 2>nul
if %ERRORLEVEL%==0 set "PY=py -3"
%PY% "src\amcf_vnext.py" %*
exit /b %ERRORLEVEL%
