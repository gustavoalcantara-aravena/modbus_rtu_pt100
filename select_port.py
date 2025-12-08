"""
Script auxiliar para detectar y seleccionar puerto COM en Windows
"""
import serial.tools.list_ports
import sys

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
        print(f"{i}. {p.device} - {p.description}")
    print("-" * 60)
    
    while True:
        try:
            sel = input(f"\nSeleccione el puerto (1-{len(ports)}): ")
            idx = int(sel) - 1
            if 0 <= idx < len(ports):
                selected = ports[idx].device
                # Guardar en archivo para que batch lo lea
                with open("_selected_port.txt", "w") as f:
                    f.write(selected)
                print(f"\n[OK] Puerto seleccionado: {selected}")
                sys.exit(0)
            else:
                print("Numero fuera de rango, intente de nuevo.")
        except ValueError:
            print("Ingrese un numero valido.")
        except KeyboardInterrupt:
            print("\nCancelado.")
            sys.exit(1)

if __name__ == "__main__":
    main()
