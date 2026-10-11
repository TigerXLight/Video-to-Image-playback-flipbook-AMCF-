@echo off
setlocal
cd /d "%~dp0.."
set "PY=python"
where py >nul 2>nul
if %ERRORLEVEL%==0 set "PY=py -3"
%PY% "tests\test_release_package.py"
exit /b %ERRORLEVEL%
