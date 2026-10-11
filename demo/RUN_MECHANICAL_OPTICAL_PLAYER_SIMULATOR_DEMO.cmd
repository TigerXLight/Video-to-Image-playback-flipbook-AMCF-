@echo off
setlocal
cd /d "%~dp0\.."
py -3 demo\run_mechanical_optical_player_simulator_demo.py
if errorlevel 1 python demo\run_mechanical_optical_player_simulator_demo.py
endlocal
