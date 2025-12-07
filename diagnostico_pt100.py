"""
Diagnóstico de sensor PT100 - Lee múltiples registros
"""
from pymodbus.client import ModbusSerialClient
import logging
import sys
import os

logging.getLogger('pymodbus').setLevel(logging.CRITICAL)

client = ModbusSerialClient(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=1
)

if client.connect():
    print("Conectado. Leyendo registros 0-9...\n")
    
    # Silenciar mensajes
    devnull = open(os.devnull, 'w')
    old_stderr = sys.stderr
    sys.stderr = devnull
    
    # Leer holding registers (función 03)
    print("HOLDING REGISTERS (Función 03):")
    print("-" * 40)
    rr = client.read_holding_registers(address=0, count=10, slave=1)
    sys.stderr = old_stderr
    devnull.close()
    
    if not rr.isError():
        for i, val in enumerate(rr.registers):
            # Mostrar valor unsigned, signed, y posibles interpretaciones
            signed = val - 65536 if val > 32767 else val
            print(f"Reg {i}: {val:5d} (unsigned) | {signed:6d} (signed) | {val/10:.1f} | {signed/10:.1f}")
    else:
        print(f"Error: {rr}")
    
    print("\n")
    
    # Leer input registers (función 04)
    print("INPUT REGISTERS (Función 04):")
    print("-" * 40)
    
    devnull = open(os.devnull, 'w')
    sys.stderr = devnull
    rr2 = client.read_input_registers(address=0, count=10, slave=1)
    sys.stderr = old_stderr
    devnull.close()
    
    if not rr2.isError():
        for i, val in enumerate(rr2.registers):
            signed = val - 65536 if val > 32767 else val
            print(f"Reg {i}: {val:5d} (unsigned) | {signed:6d} (signed) | {val/10:.1f} | {signed/10:.1f}")
    else:
        print(f"Error o no soportado: {rr2}")
    
    client.close()
else:
    print("No se pudo conectar")
