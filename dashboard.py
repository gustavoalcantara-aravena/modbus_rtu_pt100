"""
Dashboard Web para Lectura de Sensor PT100 via Modbus RTU
=========================================================
Laboratorio de Comunicaciones y Redes Industriales

Este dashboard muestra en tiempo real la lectura de temperatura
de un sensor PT100 conectado via protocolo Modbus RTU.
"""

from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from pymodbus.client import ModbusSerialClient
import threading
import time
from datetime import datetime
from collections import deque
import logging
import sys
import os
import glob

# Desactivar mensajes de pymodbus
logging.getLogger('pymodbus').setLevel(logging.CRITICAL)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'laboratorio_modbus'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', ping_timeout=5, ping_interval=1)

# Configuración Modbus
PUERTO = None  # Se detectará automáticamente
BAUDRATE = 9600
PARIDAD = 'N'
BITS_PARADA = 1
BITS_DATOS = 8
TIMEOUT = 1
DIRECCION_ESCLAVO = 1
REGISTRO_TEMPERATURA = 0

# Almacenamiento de datos históricos (últimos 500 puntos para más fluidez)
historico = deque(maxlen=500)
ultima_trama_tx = ""
ultima_trama_rx = ""
estado_conexion = False

def valor_a_temperatura(valor_raw):
    """Convierte valor crudo a temperatura en °C"""
    return valor_raw / 10.0

def formato_trama_hex(data):
    """Formatea bytes como string hexadecimal"""
    if isinstance(data, (list, tuple)):
        return ' '.join([f'{b:02X}' for b in data])
    return str(data)

def detectar_puertos_seriales():
    """Detecta todos los puertos seriales disponibles en el sistema"""
    puertos = []
    
    # Detectar sistema operativo
    if sys.platform.startswith('win'):
        # Windows: probar COM1 a COM20
        for i in range(1, 21):
            puertos.append(f'COM{i}')
    else:
        # Linux/Mac: patrones comunes de puertos seriales
        patrones = [
            '/dev/ttyUSB*',    # Adaptadores USB-Serial
            '/dev/ttyACM*',    # Arduino y similares
            '/dev/ttyS*',      # Puertos seriales nativos
            '/dev/ttyAMA*',    # Raspberry Pi
            '/dev/serial*',    # Enlaces simbólicos
        ]
        
        for patron in patrones:
            puertos.extend(glob.glob(patron))
    
    # Ordenar para consistencia
    return sorted(set(puertos))

def probar_sensor_en_puerto(puerto):
    """
    Intenta conectar y leer del sensor en un puerto específico.
    Retorna True si detecta el sensor, False en caso contrario.
    """
    try:
        client = ModbusSerialClient(
            port=puerto,
            baudrate=BAUDRATE,
            parity=PARIDAD,
            stopbits=BITS_PARADA,
            bytesize=BITS_DATOS,
            timeout=TIMEOUT
        )
        
        if client.connect():
            # Silenciar stderr
            devnull = open(os.devnull, 'w')
            old_stderr = sys.stderr
            sys.stderr = devnull
            
            # Intentar leer el registro de temperatura
            rr = client.read_holding_registers(
                address=REGISTRO_TEMPERATURA,
                count=1,
                slave=DIRECCION_ESCLAVO
            )
            
            sys.stderr = old_stderr
            devnull.close()
            client.close()
            
            # Verificar si la lectura fue exitosa
            if not rr.isError():
                valor = rr.registers[0]
                # Validar que el valor sea razonable para temperatura (-50 a 500 °C)
                temp = valor / 10.0
                if -500 <= temp <= 5000:  # Rango amplio para ser flexible
                    return True
        
        return False
        
    except Exception:
        return False

def detectar_puerto_sensor():
    """
    Itera sobre todos los puertos seriales disponibles
    y retorna el primero donde detecte el sensor PT100.
    """
    global PUERTO
    
    print("\n" + "=" * 60)
    print("  DETECCIÓN AUTOMÁTICA DE PUERTO SERIAL")
    print("=" * 60)
    
    puertos = detectar_puertos_seriales()
    
    if not puertos:
        print("[!] No se encontraron puertos seriales disponibles")
        print("    Verifique que el adaptador USB-RS485 esté conectado")
        return None
    
    print(f"\nPuertos encontrados: {len(puertos)}")
    print("-" * 40)
    
    for puerto in puertos:
        print(f"  Probando {puerto}...", end=" ", flush=True)
        
        if probar_sensor_en_puerto(puerto):
            print("✓ SENSOR DETECTADO")
            PUERTO = puerto
            print("-" * 40)
            print(f"\n[OK] Sensor PT100 encontrado en: {puerto}")
            return puerto
        else:
            print("✗ No detectado")
    
    print("-" * 40)
    print("\n[!] No se detectó el sensor en ningún puerto")
    print("    Verifique:")
    print("    - Conexión física del cable RS-485")
    print("    - Alimentación del transmisor PT100")
    print("    - Configuración de baudrate y dirección esclavo")
    return None

def leer_modbus():
    """Hilo que lee continuamente del sensor Modbus"""
    global ultima_trama_tx, ultima_trama_rx, estado_conexion
    
    client = ModbusSerialClient(
        port=PUERTO,
        baudrate=BAUDRATE,
        parity=PARIDAD,
        stopbits=BITS_PARADA,
        bytesize=BITS_DATOS,
        timeout=TIMEOUT
    )
    
    while True:
        try:
            if client.connect():
                estado_conexion = True
                
                # Silenciar stderr
                devnull = open(os.devnull, 'w')
                old_stderr = sys.stderr
                sys.stderr = devnull
                
                rr = client.read_holding_registers(
                    address=REGISTRO_TEMPERATURA,
                    count=1,
                    slave=DIRECCION_ESCLAVO
                )
                
                sys.stderr = old_stderr
                devnull.close()
                
                if not rr.isError():
                    valor_raw = rr.registers[0]
                    temperatura = valor_a_temperatura(valor_raw)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    # Construir representación de tramas Modbus RTU
                    # Trama TX: [Slave Addr] [Function] [Start Addr Hi] [Start Addr Lo] [Quantity Hi] [Quantity Lo] [CRC]
                    ultima_trama_tx = f"01 03 00 00 00 01 [CRC]"
                    # Trama RX: [Slave Addr] [Function] [Byte Count] [Data Hi] [Data Lo] [CRC]
                    data_hi = (valor_raw >> 8) & 0xFF
                    data_lo = valor_raw & 0xFF
                    ultima_trama_rx = f"01 03 02 {data_hi:02X} {data_lo:02X} [CRC]"
                    
                    # Guardar en histórico
                    dato = {
                        'timestamp': timestamp,
                        'valor_raw': valor_raw,
                        'temperatura': temperatura,
                        'trama_tx': ultima_trama_tx,
                        'trama_rx': ultima_trama_rx
                    }
                    historico.append(dato)
                    
                    # Enviar a clientes web via WebSocket
                    socketio.emit('nuevo_dato', dato)
                
            else:
                estado_conexion = False
                
        except Exception as e:
            estado_conexion = False
            print(f"Error: {e}")
        
        time.sleep(0.1)  # 100ms para actualización instantánea

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/historico')
def get_historico():
    return jsonify(list(historico))

@app.route('/api/estado')
def get_estado():
    return jsonify({
        'conectado': estado_conexion,
        'puerto': PUERTO,
        'baudrate': BAUDRATE,
        'esclavo': DIRECCION_ESCLAVO
    })

if __name__ == '__main__':
    print("=" * 60)
    print("  DASHBOARD MODBUS RTU - LABORATORIO DE REDES INDUSTRIALES")
    print("=" * 60)
    
    # Detectar automáticamente el puerto del sensor
    puerto_detectado = detectar_puerto_sensor()
    
    if puerto_detectado:
        # Iniciar hilo de lectura Modbus solo si se detectó el sensor
        hilo_modbus = threading.Thread(target=leer_modbus, daemon=True)
        hilo_modbus.start()
        
        print(f"\n  Accede al dashboard en: http://localhost:5000")
        print("=" * 60)
        
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    else:
        print("\n[!] No se puede iniciar el dashboard sin sensor conectado")
        print("    Conecte el sensor y vuelva a ejecutar el programa")
        print("=" * 60)
        sys.exit(1)
