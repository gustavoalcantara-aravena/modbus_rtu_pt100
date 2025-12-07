#!/bin/bash
# =============================================================
# Script de ejecución - Dashboard Modbus PT100
# Laboratorio de Comunicaciones y Redes Industriales
# =============================================================

echo "============================================================"
echo "  DASHBOARD MODBUS RTU - SENSOR PT100"
echo "============================================================"

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker no está instalado"
    echo ""
    echo "Instale Docker con:"
    echo "  sudo apt update && sudo apt install docker.io"
    echo "  sudo usermod -aG docker \$USER"
    echo ""
    echo "Luego cierre sesión y vuelva a entrar"
    exit 1
fi

# Verificar permisos de Docker
if ! docker info &> /dev/null; then
    echo "[ERROR] No tiene permisos para ejecutar Docker"
    echo ""
    echo "Ejecute: sudo usermod -aG docker \$USER"
    echo "Luego cierre sesión y vuelva a entrar"
    exit 1
fi

# Detener contenedor anterior si existe
if docker ps -a --format '{{.Names}}' | grep -q '^modbus-pt100$'; then
    echo "[INFO] Deteniendo contenedor anterior..."
    docker stop modbus-pt100 &> /dev/null
    docker rm modbus-pt100 &> /dev/null
fi

echo "[INFO] Iniciando Dashboard Modbus..."
echo ""

# Ejecutar contenedor
docker run -it --rm \
    --name modbus-pt100 \
    -p 5000:5000 \
    --privileged \
    -v /dev:/dev \
    modbus-dashboard

echo ""
echo "[INFO] Dashboard detenido"
