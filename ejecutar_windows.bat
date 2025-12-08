@echo off
setlocal enabledelayedexpansion
echo ============================================================
echo   DASHBOARD MODBUS RTU - SENSOR PT100
echo ============================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Descargue Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install "pymodbus>=3.0.0" flask flask-socketio gevent gevent-websocket pyserial >nul 2>&1

echo.
echo ============================================================
echo   DETECCION DE PUERTOS COM
echo ============================================================
echo.
echo [INFO] Buscando puertos COM disponibles...
echo.

REM Ejecutar seleccion de puerto
python select_port.py
if errorlevel 1 (
    pause
    exit /b 1
)

REM Leer puerto seleccionado
set /p selected_port=<_selected_port.txt

REM Limpiar archivo temporal
del _selected_port.txt 2>nul

echo.
echo [INFO] Puerto seleccionado: %selected_port%
echo.

REM Configurar variable de entorno para el puerto
set "MODBUS_PORT=%selected_port%"

echo ============================================================
echo   INICIANDO DASHBOARD
echo ============================================================
echo.
echo [INFO] Iniciando Dashboard en puerto %selected_port%...
echo Acceda a: http://localhost:5000
echo.

python dashboard.py --port %selected_port%

pause
endlocal
