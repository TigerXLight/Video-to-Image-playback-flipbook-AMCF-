@echo off
setlocal
cd /d "%~dp0\.."
py -3 demo\run_source_frames_to_amcf_digital_demo.py
if errorlevel 1 python demo\run_source_frames_to_amcf_digital_demo.py
endlocal
