# 🚀 Inicio Rápido - Dashboard Modbus PT100

## Paso 1: Instalar Docker

```bash
sudo apt update
sudo apt install docker.io
sudo usermod -aG docker $USER
```

**⚠️ Importante:** Cierra sesión y vuelve a entrar para que los cambios surtan efecto.

---

## Paso 2: Cargar la imagen

```bash
docker load -i modbus-dashboard.tar.gz
```

---

## Paso 3: Conectar el hardware

1. Conectar el adaptador **USB-RS485** al puerto USB
2. Conectar el **transmisor PT100** al bus RS-485
3. Verificar alimentación del transmisor

---

## Paso 4: Ejecutar

```bash
./ejecutar.sh
```

---

## Paso 5: Abrir el dashboard

Abre en tu navegador: **http://localhost:5000**

---

## ❓ Problemas comunes

| Problema | Solución |
|----------|----------|
| "Permission denied" | Ejecuta `sudo usermod -aG docker $USER` y reinicia sesión |
| "No se detectó el sensor" | Verifica la conexión del cable USB-RS485 |
| Docker no encontrado | Ejecuta `sudo apt install docker.io` |

---

## 📞 Soporte

Si tienes problemas, consulta con el profesor o revisa la documentación en [README.md](README.md).
