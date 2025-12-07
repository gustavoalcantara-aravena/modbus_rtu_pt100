@echo off
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
pip install pymodbus flask flask-socketio gevent gevent-websocket

echo.
echo [INFO] Iniciando Dashboard...
echo Acceda a: http://localhost:5000
echo.

python dashboard.py

pause
