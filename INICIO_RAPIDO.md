# 🚀 Inicio Rápido - Dashboard Modbus PT100

**Laboratorio de Comunicaciones y Redes Industriales**

Esta guía te llevará paso a paso para ejecutar el Dashboard Modbus PT100 en tu computador.

---

## 📋 Paso 1: Clonar el repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/gustavoalcantara-aravena/modbus_rtu_pt100.git
cd modbus_rtu_pt100
```

---

## 🐧 Instrucciones para Linux (Ubuntu/Debian)

### Paso 2: Instalar Docker

Abre una terminal y ejecuta los siguientes comandos uno por uno:

```bash
# Actualizar repositorios
sudo apt update

# Instalar Docker
sudo apt install docker.io

# Agregar tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER
```

### Paso 3: Reiniciar sesión

**⚠️ MUY IMPORTANTE:** Debes cerrar sesión completamente y volver a entrar para que los permisos de Docker se apliquen.

- Opción 1: Cierra sesión desde el menú de tu sistema y vuelve a iniciar sesión
- Opción 2: Reinicia el computador

### Paso 4: Verificar instalación de Docker

Abre una nueva terminal y ejecuta:

```bash
docker --version
```

Deberías ver algo como: `Docker version 24.x.x`

Si aparece un error de permisos, asegúrate de haber cerrado sesión y vuelto a entrar.

### Paso 5: Cargar la imagen Docker

En la carpeta del proyecto, ejecuta:

```bash
docker load -i modbus-dashboard.tar.gz
```

Espera a que termine (puede tomar unos segundos).

### Paso 6: Conectar el hardware

1. Conecta el adaptador **USB-RS485** a un puerto USB de tu computador
2. Conecta el **transmisor PT100** al bus RS-485
3. Verifica que el transmisor tenga alimentación (LED encendido)

### Paso 7: Ejecutar el dashboard

```bash
./ejecutar.sh
```

### Paso 8: Abrir en el navegador

Abre tu navegador web y ve a: **http://localhost:5000**

---

## 🪟 Instrucciones para Windows

### Paso 2: Instalar Docker Desktop

1. Ve a la página oficial de Docker: **https://www.docker.com/products/docker-desktop/**

2. Haz clic en **"Download for Windows"**

3. Ejecuta el instalador `Docker Desktop Installer.exe`

4. Durante la instalación:
   - ✅ Marca la opción **"Use WSL 2 instead of Hyper-V"** (recomendado)
   - ✅ Marca **"Add shortcut to desktop"**

5. Haz clic en **"Ok"** y espera a que termine la instalación

6. **Reinicia el computador** cuando te lo pida

### Paso 3: Iniciar Docker Desktop

1. Después de reiniciar, abre **Docker Desktop** desde el menú de inicio o el acceso directo del escritorio

2. Espera a que Docker Desktop inicie completamente (el ícono en la barra de tareas debe mostrar "Docker Desktop is running")

3. Si es la primera vez, acepta los términos de servicio

### Paso 4: Habilitar WSL 2 (si no está habilitado)

Si Docker te pide habilitar WSL 2:

1. Abre **PowerShell como Administrador** (clic derecho → "Ejecutar como administrador")

2. Ejecuta:
   ```powershell
   wsl --install
   ```

3. Reinicia el computador

4. Abre Docker Desktop nuevamente

### Paso 5: Abrir terminal en la carpeta del proyecto

1. Abre el **Explorador de archivos**

2. Navega hasta la carpeta `modbus_rtu_pt100` que clonaste

3. Haz clic derecho en un espacio vacío y selecciona **"Abrir en Terminal"** o **"Abrir ventana de PowerShell aquí"**

### Paso 6: Cargar la imagen Docker

En la terminal de PowerShell, ejecuta:

```powershell
docker load -i modbus-dashboard.tar.gz
```

Espera a que termine de cargar la imagen.

### Paso 7: Conectar el hardware

1. Conecta el adaptador **USB-RS485** a un puerto USB de tu computador

2. Conecta el **transmisor PT100** al bus RS-485

3. Verifica que el transmisor tenga alimentación

4. **Importante:** Anota el número de puerto COM asignado:
   - Abre **Administrador de dispositivos** (busca "Administrador de dispositivos" en el menú inicio)
   - Expande **"Puertos (COM y LPT)"**
   - Busca tu adaptador USB-Serial (ejemplo: "USB-SERIAL CH340 (COM3)")
   - Anota el número (COM3, COM4, etc.)

### Paso 8: Ejecutar el dashboard

En PowerShell, ejecuta:

```powershell
docker run -it --rm --name modbus-pt100 -p 5000:5000 --privileged modbus-dashboard
```

**Nota para Windows:** El acceso a puertos COM desde Docker en Windows puede requerir configuración adicional. Si el sensor no es detectado, usa la opción alternativa (ver abajo).

### Paso 9: Abrir en el navegador

Abre tu navegador web y ve a: **http://localhost:5000**

---

## 🔄 Opción alternativa para Windows (sin Docker)

Si tienes problemas con Docker en Windows, puedes ejecutar directamente con Python:

### 1. Instalar Python

1. Ve a **https://www.python.org/downloads/**
2. Descarga Python 3.11 o superior
3. Durante la instalación, **marca la casilla "Add Python to PATH"**
4. Completa la instalación

### 2. Ejecutar el dashboard

Haz doble clic en el archivo `ejecutar_windows.bat`

El script instalará las dependencias automáticamente y ejecutará el dashboard.

---

## ❓ Solución de problemas

### Linux

| Problema | Solución |
|----------|----------|
| "Permission denied" al ejecutar docker | Ejecuta `sudo usermod -aG docker $USER` y **reinicia sesión** |
| "docker: command not found" | Ejecuta `sudo apt install docker.io` |
| "No se detectó el sensor" | Verifica conexión USB-RS485 y alimentación del transmisor |
| El script no tiene permisos | Ejecuta `chmod +x ejecutar.sh` |

### Windows

| Problema | Solución |
|----------|----------|
| Docker Desktop no inicia | Verifica que la virtualización esté habilitada en BIOS |
| "WSL 2 installation is incomplete" | Ejecuta `wsl --install` en PowerShell como administrador |
| No detecta el puerto COM | Usa la opción alternativa con Python (ejecutar_windows.bat) |
| "python: command not found" | Reinstala Python marcando "Add Python to PATH" |

---

## 🛑 Detener el dashboard

### Linux
Presiona `Ctrl + C` en la terminal

### Windows
Presiona `Ctrl + C` en PowerShell, o cierra la ventana

---

## 📞 Soporte

Si tienes problemas que no puedes resolver:

1. Revisa la documentación en [README.md](README.md)
2. Consulta con el profesor durante el laboratorio
3. Verifica que el hardware esté correctamente conectado

---

**Laboratorio de Comunicaciones y Redes Industriales**
