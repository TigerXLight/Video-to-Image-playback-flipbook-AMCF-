@echo off
setlocal

set "PY=C:\Users\fahad\AppData\Local\Programs\Python\Python311\python.exe"

"%PY%" "%~dp0amcf_tracking_test03a.py"
exit /b %ERRORLEVEL%
