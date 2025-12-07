# Instalación con Docker - Dashboard Modbus PT100

## Requisitos previos

### 1. Instalar Docker
```bash
sudo apt update
sudo apt install docker.io
sudo usermod -aG docker $USER
```
**Importante:** Cierre sesión y vuelva a entrar para que los cambios surtan efecto.

### 2. Verificar instalación
```bash
docker --version
```

---

## Opción A: Descargar imagen (más rápido)

Si el profesor les proporcionó el archivo `modbus-dashboard.tar.gz`:

```bash
# 1. Cargar la imagen
docker load -i modbus-dashboard.tar.gz

# 2. Ejecutar
./ejecutar.sh
```

---

## Opción B: Construir desde código fuente

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/Modbus_Docker.git
cd Modbus_Docker

# 2. Construir imagen
docker build -t modbus-dashboard .

# 3. Ejecutar
./ejecutar.sh
```

---

## Uso manual (sin script)

```bash
docker run -it --rm \
    --name modbus-pt100 \
    -p 5000:5000 \
    --privileged \
    -v /dev:/dev \
    modbus-dashboard
```

Acceder al dashboard: **http://localhost:5000**

---

## Solución de problemas

### "Permission denied" al ejecutar Docker
```bash
sudo usermod -aG docker $USER
# Cerrar sesión y volver a entrar
```

### No detecta el sensor
- Verificar que el adaptador USB-RS485 esté conectado
- Verificar conexión física al transmisor PT100
- El sistema probará automáticamente todos los puertos disponibles

### Ver logs del contenedor
```bash
docker logs modbus-pt100
```

---

## Detener el dashboard

Presionar `Ctrl+C` en la terminal, o:
```bash
docker stop modbus-pt100
```
