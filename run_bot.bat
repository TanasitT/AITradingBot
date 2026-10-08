@echo off
REM Launches the scheduler from the folder this file lives in.
REM Set PYTHON_EXE to a full interpreter path if `python` on your PATH is not the right one.
cd /d "%~dp0"
if not exist logs mkdir logs
if "%PYTHON_EXE%"=="" set "PYTHON_EXE=python"
"%PYTHON_EXE%" main.py >> logs\launcher.log 2>&1
