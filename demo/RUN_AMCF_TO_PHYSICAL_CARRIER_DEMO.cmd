@echo off
setlocal
cd /d "%~dp0\.."
py -3 demo\run_amcf_to_physical_carrier_demo.py
if errorlevel 1 python demo\run_amcf_to_physical_carrier_demo.py
endlocal
