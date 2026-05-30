@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul

echo.
echo =========================================================
echo   Marketplace Financial AI Engine v3.5
echo   Marketplace Conciliation Center
echo =========================================================
echo.
echo  [>>] Iniciando motor financiero...

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] No existe el entorno virtual en .venv
    echo Recrealo con: python -m venv .venv
    pause
    exit /b 1
)

if not exist "Scripts\run_python.bat" (
    echo [ERROR] Falta Scripts\run_python.bat
    pause
    exit /b 1
)

if not exist "run_app.py" (
    echo [ERROR] Falta run_app.py
    pause
    exit /b 1
)

if not exist "logs" (
    mkdir "logs"
)

echo [OK] Entorno y entrypoints detectados.
start "Meli Financial API" cmd /c "chcp 65001>nul && cd /d %~dp0 && Scripts\run_python.bat run_app.py >> logs\backend.log 2>&1"

echo [OK] Esperando disponibilidad real del backend...

set "HEALTH_URL=http://127.0.0.1:8003/api/v4/cierre"
set "MAX_RETRIES=20"
set /a COUNT=0

:wait_loop
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri '%HEALTH_URL%' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }"

if %ERRORLEVEL%==0 goto ready

set /a COUNT+=1
if %COUNT% geq %MAX_RETRIES% goto timeout_err

ping 127.0.0.1 -n 2 > nul
goto wait_loop

:ready
echo [OK] Backend disponible. Abriendo panel...
start http://127.0.0.1:8003/app
echo.
echo =========================================================
echo   SISTEMA ACTIVO: http://127.0.0.1:3001/app
echo =========================================================
echo.
exit /b 0

:timeout_err
echo [ERROR] El backend no respondio a tiempo en %HEALTH_URL%
echo Revisa logs\backend.log para diagnostico.
pause
exit /b 1
