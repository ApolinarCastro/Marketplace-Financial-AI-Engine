@echo off
setlocal EnableExtensions
cd /d "%~dp0"
chcp 65001 >nul

title Marketplace Financial AI Engine v1.0

echo.
echo =========================================================
echo   Marketplace Financial AI Engine v1.0
echo   Marketplace Auditor v3.5
echo   Reporte Gerencial UX1.2
echo =========================================================
echo.
echo [>>] Iniciando motor financiero...
echo.

set "PYTHON=%~dp0.venv\Scripts\python.exe"
set "ENTRYPOINT=%~dp0run_app.py"
set "LOG_DIR=%~dp0logs"
set "BACKEND_LOG=%LOG_DIR%\backend.log"
set "APP_URL=http://127.0.0.1:3001/app"
set "HOST=127.0.0.1"
set "PORT=3001"
set "MAX_RETRIES=30"

if not exist "%PYTHON%" (
    echo [ERROR] No existe el entorno virtual:
    echo         %PYTHON%
    echo.
    echo Recrealo con:
    echo python -m venv .venv
    pause
    exit /b 1
)

if not exist "%ENTRYPOINT%" (
    echo [ERROR] No existe el entrypoint:
    echo         %ENTRYPOINT%
    pause
    exit /b 1
)

if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
)

echo [OK] Entorno virtual detectado.
echo [OK] Entry point detectado.
echo [OK] Log: %BACKEND_LOG%
echo.

rem Verificar si el puerto ya esta operativo
"%PYTHON%" -c "import socket; s=socket.socket(); s.settimeout(1); r=s.connect_ex(('%HOST%',%PORT%)); s.close(); raise SystemExit(0 if r==0 else 1)" >nul 2>&1

if not errorlevel 1 (
    echo [OK] El backend ya se encuentra activo.
    goto ready
)

echo [>>] Lanzando backend...

start "Marketplace Financial API" /min cmd.exe /d /c ^
""%PYTHON%" "%ENTRYPOINT%" >> "%BACKEND_LOG%" 2>&1"

echo [>>] Esperando disponibilidad en %HOST%:%PORT%...

set /a COUNT=0

:wait_loop
"%PYTHON%" -c "import socket; s=socket.socket(); s.settimeout(1); r=s.connect_ex(('%HOST%',%PORT%)); s.close(); raise SystemExit(0 if r==0 else 1)" >nul 2>&1

if not errorlevel 1 goto ready

set /a COUNT+=1

if %COUNT% geq %MAX_RETRIES% goto timeout_err

timeout /t 1 /nobreak >nul
goto wait_loop

:ready
echo.
echo [OK] Backend disponible.
echo [OK] Abriendo Marketplace Auditor v3.5...
echo.

start "" "%APP_URL%"

echo =========================================================
echo   SISTEMA ACTIVO
echo.
echo   Producto:   Marketplace Financial AI Engine v1.0
echo   Auditor:    Marketplace Auditor v3.5
echo   Ejecutivo:  Reporte Gerencial UX1.2
echo.
echo   URL: %APP_URL%
echo =========================================================
echo.

exit /b 0

:timeout_err
echo.
echo [ERROR] El backend no respondio en %HOST%:%PORT%
echo.
echo === ULTIMAS 30 LINEAS DEL LOG ===

if exist "%BACKEND_LOG%" (
    powershell -NoProfile -Command ^
    "Get-Content -LiteralPath '%BACKEND_LOG%' -Tail 30"
) else (
    echo No se genero el archivo backend.log
)

echo ==================================
echo.
pause
exit /b 1