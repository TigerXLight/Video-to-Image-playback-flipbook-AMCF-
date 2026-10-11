@echo off
setlocal
cd /d "%~dp0\.."
py -3 demo\run_virtual_reader_recovery_export_demo.py
if errorlevel 1 python demo\run_virtual_reader_recovery_export_demo.py
endlocal
