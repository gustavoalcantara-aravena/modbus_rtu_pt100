# Dashboard Modbus RTU - Sensor PT100

Sistema de monitoreo en tiempo real para sensor de temperatura PT100 mediante protocolo Modbus RTU.

**Laboratorio de Comunicaciones y Redes Industriales**

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![Modbus](https://img.shields.io/badge/Protocolo-Modbus%20RTU-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 📋 Descripción

Este proyecto implementa un dashboard web interactivo para la lectura y visualización de datos de un sensor de temperatura PT100 conectado a través del protocolo industrial Modbus RTU.

### Características principales:
- **Lectura en tiempo real** del sensor PT100
- **Dashboard web** con gráficos dinámicos
- **Visualización de tramas Modbus** TX/RX en vivo
- **Histórico de temperaturas** con estadísticas
- **Modo claro/oscuro** (Dark/Light mode)
- **Detección automática** del puerto serial
- **Información educativa** sobre el protocolo Modbus RTU

---

## 🚀 Instalación Rápida

### 🐧 Linux (Docker - Recomendado)

```bash
# 1. Instalar Docker (solo una vez)
sudo apt install docker.io
sudo usermod -aG docker $USER
# Cerrar sesión y volver a entrar

# 2. Cargar la imagen (si tienes el archivo .tar.gz)
docker load -i modbus-dashboard.tar.gz

# 3. Ejecutar
./ejecutar.sh
```

### 🪟 Windows

```batch
# 1. Instalar Python desde https://www.python.org/downloads/
# 2. Doble clic en ejecutar_windows.bat
```

El script instalará las dependencias automáticamente.

---

## 🛠️ Requisitos

### Hardware
- Sensor PT100 (3 hilos)
- Transmisor/Convertidor PT100 a Modbus RTU
- Adaptador USB a RS-485
- Cable de conexión

### Software

| Sistema | Requisito |
|---------|-----------|
| **Linux** | Docker |
| **Windows** | Python 3.x |

---

## 📦 Instalación Manual (sin Docker)

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/Modbus_Docker.git
cd Modbus_Docker
```

2. Instalar dependencias:
```bash
pip install pymodbus flask flask-socketio gevent gevent-websocket
```

3. Conectar el hardware:
   - Conectar el adaptador USB-RS485 al puerto USB
   - Conectar el transmisor PT100 al bus RS-485
   - Conectar el sensor PT100 al transmisor (ver [CONEXION.md](CONEXION.md))

---

## 🚀 Uso

### Lectura simple (consola)
```bash
python3 leer_pt100.py
```

### Dashboard web
```bash
python3 dashboard.py
```
Acceder a: **http://localhost:5000**

---

## 📁 Estructura del proyecto

```
Modbus_Docker/
├── README.md                  # Este archivo
├── CONEXION.md                # Guía de conexión del hardware
├── MODBUS.md                  # Documentación del protocolo Modbus
├── INSTALACION_DOCKER.md      # Guía detallada de Docker
├── dashboard.py               # Servidor web con dashboard
├── leer_pt100.py              # Script de lectura simple
├── diagnostico_pt100.py       # Herramienta de diagnóstico
├── ejecutar.sh                # Script para Linux
├── ejecutar_windows.bat       # Script para Windows
├── Dockerfile                 # Configuración Docker
├── docker-compose.yml         # Orquestación Docker
├── requirements.txt           # Dependencias Python
└── templates/
    └── index.html             # Interfaz web del dashboard
```

---

## ⚙️ Configuración

### Parámetros Modbus (en `dashboard.py` y `leer_pt100.py`)

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `PUERTO` | Auto-detectado | Puerto serial (Linux: `/dev/ttyUSB0`, Windows: `COM3`) |
| `BAUDRATE` | `9600` | Velocidad de comunicación |
| `PARIDAD` | `N` | Sin paridad |
| `BITS_DATOS` | `8` | Bits de datos |
| `BITS_PARADA` | `1` | Bits de parada |
| `DIRECCION_ESCLAVO` | `1` | Dirección del dispositivo |
| `REGISTRO_TEMPERATURA` | `0` | Registro Holding a leer |

> **Nota:** El sistema detecta automáticamente el puerto donde está conectado el sensor.

---

## 📊 Dashboard

El dashboard web incluye:

- **Temperatura actual** con indicador de tendencia (↑↓→)
- **Estadísticas**: mínima, máxima y promedio
- **Gráfico histórico** en tiempo real
- **Tramas Modbus** TX/RX en vivo
- **Configuración** del sistema
- **Información educativa** sobre Modbus RTU
- **Estructura de tramas** con explicación de campos
- **Registro de comunicaciones** (tabla)

### Temas
- 🌙 **Dark Mode** (por defecto)
- ☀️ **Light Mode**

---

## 📚 Documentación adicional

- [CONEXION.md](CONEXION.md) - Guía de conexión del sensor PT100
- [MODBUS.md](MODBUS.md) - Documentación del protocolo Modbus RTU
- [INSTALACION_DOCKER.md](INSTALACION_DOCKER.md) - Guía detallada de instalación con Docker

---

## ❓ Solución de problemas

| Problema | Solución |
|----------|----------|
| "Permission denied" en Docker | `sudo usermod -aG docker $USER` y reiniciar sesión |
| No detecta el sensor | Verificar conexión USB-RS485 y alimentación del transmisor |
| Puerto COM no encontrado (Windows) | Revisar en Administrador de dispositivos el número de puerto |
| Error de librerías (Windows) | Ejecutar `pip install -r requirements.txt` |

---

## 👥 Autor

**Gustavo Alcántara Aravena**

Laboratorio de Comunicaciones y Redes Industriales

---

## 📄 Licencia

Este proyecto es de uso educativo para el laboratorio de Comunicaciones y Redes Industriales.
