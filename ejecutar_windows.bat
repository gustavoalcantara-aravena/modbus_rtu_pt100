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
pip install pymodbus flask flask-socketio gevent gevent-websocket pyserial >nul 2>&1

echo.
echo ============================================================
echo   DETECCION DE PUERTOS COM
echo ============================================================
echo.
echo [INFO] Buscando puertos COM disponibles...
echo.

REM Crear script Python temporal para detectar puertos COM
echo import serial.tools.list_ports > _detect_ports.py
echo ports = list(serial.tools.list_ports.comports()) >> _detect_ports.py
echo if not ports: >> _detect_ports.py
echo     print("NO_PORTS") >> _detect_ports.py
echo else: >> _detect_ports.py
echo     for i, p in enumerate(ports, 1): >> _detect_ports.py
echo         print(f"{i}. {p.device} - {p.description}") >> _detect_ports.py

REM Ejecutar deteccion y mostrar puertos
echo Puertos COM detectados:
echo ------------------------------------------------------------
python _detect_ports.py > _ports_output.txt 2>&1
type _ports_output.txt

REM Verificar si hay puertos
findstr /C:"NO_PORTS" _ports_output.txt >nul 2>&1
if not errorlevel 1 (
    echo [ADVERTENCIA] No se detectaron puertos COM.
    echo Verifique que el dispositivo USB-RS485 este conectado.
    echo.
    echo Puede abrir el Administrador de Dispositivos con:
    echo   devmgmt.msc
    echo.
    del _detect_ports.py _ports_output.txt 2>nul
    pause
    exit /b 1
)

echo ------------------------------------------------------------
echo.

REM Contar puertos disponibles
set "port_count=0"
for /f "tokens=1 delims=." %%a in (_ports_output.txt) do (
    set /a port_count+=1
)

REM Solicitar seleccion de puerto
set /p "port_selection=Seleccione el numero del puerto COM a usar (1-%port_count%): "

REM Obtener el puerto seleccionado
set "selected_port="
set "current=0"
for /f "tokens=1,2 delims=. " %%a in (_ports_output.txt) do (
    set /a current+=1
    if !current! equ %port_selection% (
        set "selected_port=%%b"
    )
)

REM Limpiar archivos temporales
del _detect_ports.py _ports_output.txt 2>nul

if "%selected_port%"=="" (
    echo [ERROR] Seleccion invalida.
    pause
    exit /b 1
)

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
