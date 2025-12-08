"""
Script auxiliar para detectar y seleccionar puerto COM en Windows
"""
import serial.tools.list_ports
import sys
import os

def main():
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("\n[ADVERTENCIA] No se detectaron puertos COM.")
        print("Verifique que el dispositivo USB-RS485 este conectado.")
        print("\nPuede abrir el Administrador de Dispositivos con:")
        print("  devmgmt.msc\n")
        sys.exit(1)
    
    print("Puertos COM detectados:")
    print("-" * 60)
    for i, p in enumerate(ports, 1):
        print(f"  {i}. {p.device} - {p.description}")
    print("-" * 60)
    
    # Si solo hay un puerto, usarlo directamente
    if len(ports) == 1:
        selected = ports[0].device
        print(f"\n[INFO] Solo hay un puerto disponible, usando: {selected}")
        with open("_selected_port.txt", "w", encoding="utf-8") as f:
            f.write(selected)
        sys.exit(0)
    
    # Multiples puertos, pedir seleccion
    print(f"\nIngrese el numero del puerto (1-{len(ports)})")
    
    while True:
        try:
            sys.stdout.write("Opcion: ")
            sys.stdout.flush()
            sel = sys.stdin.readline()
            
            if not sel:
                continue
            
            # Limpiar entrada: solo digitos
            sel_clean = ''.join(c for c in sel if c.isdigit())
            
            if not sel_clean:
                print("Ingrese un numero.")
                continue
            
            idx = int(sel_clean) - 1
            
            if 0 <= idx < len(ports):
                selected = ports[idx].device
                with open("_selected_port.txt", "w", encoding="utf-8") as f:
                    f.write(selected)
                print(f"\n[OK] Puerto seleccionado: {selected}")
                sys.exit(0)
            else:
                print(f"Numero fuera de rango (debe ser 1-{len(ports)}).")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nCancelado.")
            sys.exit(1)
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
