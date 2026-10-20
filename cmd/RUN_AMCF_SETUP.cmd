@echo off
setlocal
cd /d "%~dp0.."
if not "%AMCF_PYTHON%"=="" (
  "%AMCF_PYTHON%" "src\amcf_setup.py" %*
) else (
  python "src\amcf_setup.py" %*
)
exit /b %ERRORLEVEL%
