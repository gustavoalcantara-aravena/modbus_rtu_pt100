# Protocolo Modbus RTU

## 📖 Introducción

**Modbus** es un protocolo de comunicación industrial desarrollado por Modicon (ahora Schneider Electric) en 1979. Es uno de los protocolos más utilizados en automatización industrial debido a su simplicidad y robustez.

**RTU (Remote Terminal Unit)** es el modo de transmisión binario, más eficiente que el modo ASCII.

---

## 🏗️ Arquitectura

### Modelo Maestro-Esclavo

```
    ┌──────────┐         ┌──────────┐
    │  MAESTRO │ ──────► │ ESCLAVO 1│  (Dirección 1)
    │   (PC)   │         └──────────┘
    │          │         ┌──────────┐
    │          │ ──────► │ ESCLAVO 2│  (Dirección 2)
    │          │         └──────────┘
    │          │         ┌──────────┐
    │          │ ──────► │ ESCLAVO N│  (Dirección N)
    └──────────┘         └──────────┘
```

- **Maestro**: Inicia todas las comunicaciones (solicitudes)
- **Esclavos**: Responden a las solicitudes del maestro
- **Direcciones**: 1-247 (0 = broadcast, 248-255 reservados)

---

## 📡 Capa Física: RS-485

### Características
- **Tipo**: Diferencial (half-duplex)
- **Líneas**: A+ y B- (par trenzado)
- **Distancia máxima**: 1200 metros
- **Dispositivos**: Hasta 32 en un bus (sin repetidores)
- **Velocidades comunes**: 9600, 19200, 38400, 115200 bps

### Formato de comunicación típico
```
8-N-1: 8 bits de datos, Sin paridad, 1 bit de parada
```

---

## 📦 Estructura de Trama RTU

```
┌─────────┬──────────┬────────────────┬─────────┐
│ Esclavo │ Función  │     Datos      │  CRC-16 │
│ (1 byte)│ (1 byte) │  (N bytes)     │(2 bytes)│
└─────────┴──────────┴────────────────┴─────────┘
```

### Delimitación de tramas
- **Silencio**: Mínimo 3.5 tiempos de carácter entre tramas
- A 9600 bps: ~3.6 ms de silencio

---

## 📊 Códigos de Función

### Funciones de lectura

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `0x01` | Read Coils | Leer salidas digitales (bobinas) |
| `0x02` | Read Discrete Inputs | Leer entradas digitales |
| `0x03` | Read Holding Registers | Leer registros de retención (16 bits) |
| `0x04` | Read Input Registers | Leer registros de entrada (16 bits) |

### Funciones de escritura

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `0x05` | Write Single Coil | Escribir una salida digital |
| `0x06` | Write Single Register | Escribir un registro (16 bits) |
| `0x0F` | Write Multiple Coils | Escribir múltiples salidas |
| `0x10` | Write Multiple Registers | Escribir múltiples registros |

---

## 📤 Ejemplo: Read Holding Registers (0x03)

### Solicitud del Maestro

```
┌────────┬────────┬─────────────┬─────────────┬──────────┐
│ Esclavo│Función │ Dir. Inicio │  Cantidad   │  CRC-16  │
│   01   │   03   │   00  00    │   00  01    │  84  0A  │
└────────┴────────┴─────────────┴─────────────┴──────────┘
```

| Campo | Bytes | Valor | Descripción |
|-------|-------|-------|-------------|
| Esclavo | 01 | 1 | Dirección del dispositivo |
| Función | 03 | 3 | Read Holding Registers |
| Dir. Inicio | 00 00 | 0 | Registro inicial (0x0000) |
| Cantidad | 00 01 | 1 | Cantidad de registros a leer |
| CRC-16 | 84 0A | - | Checksum |

### Respuesta del Esclavo

```
┌────────┬────────┬───────┬─────────────┬──────────┐
│ Esclavo│Función │ Bytes │    Datos    │  CRC-16  │
│   01   │   03   │  02   │   01  0B    │  XX  XX  │
└────────┴────────┴───────┴─────────────┴──────────┘
```

| Campo | Bytes | Valor | Descripción |
|-------|-------|-------|-------------|
| Esclavo | 01 | 1 | Dirección del dispositivo |
| Función | 03 | 3 | Read Holding Registers |
| Bytes | 02 | 2 | Cantidad de bytes de datos |
| Datos | 01 0B | 267 | Valor del registro (0x010B = 267) |
| CRC-16 | XX XX | - | Checksum |

### Interpretación del dato
```
0x010B = 267 decimal
267 ÷ 10 = 26.7 °C
```

---

## 🔢 CRC-16 (Cyclic Redundancy Check)

### Algoritmo
- Polinomio: `0xA001` (reflejado de `0x8005`)
- Valor inicial: `0xFFFF`
- Se transmite LSB primero

### Pseudocódigo
```python
def calcular_crc(datos):
    crc = 0xFFFF
    for byte in datos:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return crc
```

---

## ❌ Códigos de Excepción

Cuando ocurre un error, el esclavo responde con:
- Código de función + `0x80`
- Código de excepción

| Código | Nombre | Descripción |
|--------|--------|-------------|
| `0x01` | Illegal Function | Función no soportada |
| `0x02` | Illegal Data Address | Dirección inválida |
| `0x03` | Illegal Data Value | Valor inválido |
| `0x04` | Slave Device Failure | Error en el dispositivo |

### Ejemplo de respuesta de error
```
01 83 02 C0 F1
│  │  │  └────── CRC-16
│  │  └───────── Código de excepción (Illegal Data Address)
│  └──────────── Función + 0x80 (0x03 + 0x80 = 0x83)
└─────────────── Dirección del esclavo
```

---

## ⏱️ Tiempos

### Timeout recomendado
- **Respuesta**: 1000 ms (configurable)
- **Entre caracteres**: < 1.5 tiempos de carácter

### Cálculo de tiempo de carácter
```
Tiempo de carácter = (1 + 8 + 1 + 1) / baudrate
A 9600 bps: 11 / 9600 = 1.15 ms por carácter
```

---

## 📚 Referencias

- Modbus Organization: [modbus.org](https://modbus.org)
- Especificación Modbus RTU: Modbus Application Protocol V1.1b3
- Especificación RS-485: TIA/EIA-485

---

## 👤 Autor

**Gustavo Alcántara Aravena**

Laboratorio de Comunicaciones y Redes Industriales
