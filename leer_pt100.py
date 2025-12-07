"""
Lectura de sensor PT100 via Modbus RTU
======================================
Protocolo: Modbus RTU (RS-485)
Dispositivo: Transmisor de temperatura PT100
Registro: 0 (Holding Register)
Dirección esclavo: 1

Autor: Laboratorio de Automatización Industrial
"""

from pymodbus.client import ModbusSerialClient
import time
from datetime import datetime
import logging
import sys
import os

# Desactivar TODOS los mensajes de pymodbus
logging.getLogger('pymodbus').setLevel(logging.CRITICAL)
logging.getLogger('pymodbus.logging').setLevel(logging.CRITICAL)

# Configuración del puerto serial
PUERTO = '/dev/ttyUSB0'
BAUDRATE = 9600
PARIDAD = 'N'
BITS_PARADA = 1
BITS_DATOS = 8
TIMEOUT = 1

# Configuración Modbus
DIRECCION_ESCLAVO = 1
REGISTRO_TEMPERATURA = 0

def valor_a_temperatura(valor_raw):
    """
    Convierte el valor crudo del registro a temperatura en °C.
    El transmisor envía el valor en décimas de grado (x10).
    Ejemplo: 268 = 26.8 °C
    """
    return valor_raw / 10.0

def main():
    print("=" * 50)
    print("  LECTURA DE SENSOR PT100 - MODBUS RTU")
    print("=" * 50)
    print(f"Puerto: {PUERTO}")
    print(f"Baudrate: {BAUDRATE}")
    print(f"Esclavo: {DIRECCION_ESCLAVO}")
    print(f"Registro: {REGISTRO_TEMPERATURA}")
    print("=" * 50)
    
    client = ModbusSerialClient(
        port=PUERTO,
        baudrate=BAUDRATE,
        parity=PARIDAD,
        stopbits=BITS_PARADA,
        bytesize=BITS_DATOS,
        timeout=TIMEOUT
    )

    if client.connect():
        print("\n[OK] Conexión establecida")
        print("Presione Ctrl+C para detener la lectura\n")
        print("-" * 65)
        print(f"{'HORA':<12} {'VALOR RAW':<12} {'TEMPERATURA':<15} {'PROTOCOLO':<20}")
        print("-" * 65)
        
        try:
            while True:
                # Silenciar mensajes internos de pymodbus
                devnull = open(os.devnull, 'w')
                old_stderr = sys.stderr
                sys.stderr = devnull
                
                rr = client.read_holding_registers(
                    address=REGISTRO_TEMPERATURA, 
                    count=1, 
                    slave=DIRECCION_ESCLAVO
                )
                
                # Restaurar stderr
                sys.stderr = old_stderr
                devnull.close()
                
                hora = datetime.now().strftime("%H:%M:%S")
                
                if rr.isError():
                    print(f"{hora:<12} {'ERROR':<12} {str(rr):<15}")
                else:
                    valor_raw = rr.registers[0]
                    temperatura = valor_a_temperatura(valor_raw)
                    print(f"{hora:<12} {valor_raw:<12} {temperatura:>6.1f} °C       MODBUS RTU")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n" + "-" * 50)
            print("[INFO] Lectura detenida por el usuario")
        finally:
            client.close()
            print("[OK] Conexión cerrada")
    else:
        print("[ERROR] No se pudo conectar al dispositivo")
        print("Verifique:")
        print("  - Conexión física del cable RS-485")
        print("  - Puerto serial correcto")
        print("  - Configuración de baudrate y paridad")

if __name__ == "__main__":
    main()
