@echo off
setlocal
set "PY=%~dp0..\.venv-test03b-samurai-py311\Scripts\python.exe"
if not exist "%PY%" set "PY=C:\Users\fahad\AppData\Local\Programs\Python\Python311\python.exe"
"%PY%" "%~dp0amcf_vnext.py" %*
exit /b %ERRORLEVEL%
