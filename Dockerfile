# Dockerfile para Airbnb Madrid MongoDB Analysis
FROM python:3.9-slim

# Metadata
LABEL maintainer="GCP <tu-email@ejemplo.com>"
LABEL description="Airbnb Madrid MongoDB Analysis - Análisis de datos con MongoDB y Python"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/raw data/processed data/sample reports/figures

# Exponer puertos
# 8888 para Jupyter
# 8000 para Streamlit (si se implementa)
EXPOSE 8888 8000

# Script de inicio
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["jupyter"]
