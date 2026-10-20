@echo off
setlocal EnableExtensions
set "ROOT=%~dp0.."
set "PY=C:\Users\fahad\AppData\Local\Programs\Python\Python311\python.exe"
if not exist "%PY%" (
  echo Python 3.11 not found at "%PY%".
  echo Install Python 3.11 or edit this launcher.
  exit /b 2
)
"%PY%" "%~dp0amcf_test02.py" --frames 288
set "RC=%ERRORLEVEL%"
echo.
echo AMCF Test 02 exited with code %RC%.
if not "%RC%"=="0" exit /b %RC%
for /f "delims=" %%D in ('powershell -NoProfile -Command "Get-ChildItem -LiteralPath '%ROOT%\Tests\Test 02' -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName"') do set "LATEST=%%D"
if not defined LATEST (
  echo Could not locate latest Test 02 output folder.
  exit /b 1
)
echo Starting local viewer for "%LATEST%\viewer"
start "AMCF Test 02 server" /min "%PY%" -m http.server 8022 --directory "%LATEST%\viewer"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:8022/"
exit /b %RC%
