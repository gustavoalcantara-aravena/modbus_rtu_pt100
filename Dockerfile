# Dockerfile para Dashboard Modbus RTU - Sensor PT100
FROM python:3.11-slim

# Metadatos
LABEL maintainer="Gustavo Alcántara Aravena"
LABEL description="Dashboard Modbus RTU para sensor PT100"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema para pyserial
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY dashboard.py .
COPY leer_pt100.py .
COPY diagnostico_pt100.py .
COPY templates/ templates/

# Exponer puerto del dashboard
EXPOSE 5000

# Comando por defecto: ejecutar el dashboard
CMD ["python", "dashboard.py"]
