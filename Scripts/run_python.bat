@echo off
setlocal

set "LOCAL_PY_HOME=%LocalAppData%\Programs\Python\Python314"
if exist "%LOCAL_PY_HOME%\Lib" (
    set "PYTHONHOME=%LOCAL_PY_HOME%"
)
set "PYTHONPATH=%CD%;%PYTHONPATH%"
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"

".venv\Scripts\python.exe" %*
