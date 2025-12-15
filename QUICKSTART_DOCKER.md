# 🎯 INICIO ULTRA RÁPIDO - 3 Comandos

## Para Usuarios Finales (Sin conocimiento técnico)

### Método 1: Con Make (Más Simple) ⭐

```bash
# 1. Clonar proyecto
git clone https://github.com/TU-USERNAME/airbnb-madrid-mongodb-analysis.git
cd airbnb-madrid-mongodb-analysis

# 2. Levantar servicios
make up

# 3. Importar datos de ejemplo
make sample

# ¡LISTO! Abre: http://localhost:8888
```

### Método 2: Con Docker Compose (Estándar)

```bash
# 1. Clonar proyecto
git clone https://github.com/TU-USERNAME/airbnb-madrid-mongodb-analysis.git
cd airbnb-madrid-mongodb-analysis

# 2. Levantar servicios
docker-compose up -d

# 3. Importar datos
docker-compose exec app python scripts/import_sample_data.py

# ¡LISTO! Abre: http://localhost:8888
```

---

## 📍 URLs de Acceso

Una vez levantado:

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **📓 Jupyter Notebook** | http://localhost:8888 | Sin password |
| **🗄️ Mongo Express** | http://localhost:8081 | user: `admin`<br>pass: `admin123` |

---

## 🎓 Comandos Útiles (Con Make)

```bash
make help           # Ver todos los comandos disponibles
make up             # Levantar servicios
make down           # Detener servicios
make restart        # Reiniciar servicios
make logs           # Ver logs
make shell          # Acceder a terminal
make jupyter        # Abrir Jupyter en navegador
make mongo-express  # Abrir Mongo Express en navegador
make sample         # Importar datos de ejemplo (10 listings)
make full           # Importar datos completos (18k listings)
make stats          # Ver estadísticas de la DB
make clean          # Limpiar todo
```

---

## 🎓 Comandos Útiles (Con Docker Compose)

```bash
# Ver comandos disponibles
docker-compose --help

# Levantar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reiniciar un servicio
docker-compose restart app

# Acceder a shell
docker-compose exec app bash

# Ejecutar scripts Python
docker-compose exec app python scripts/import_sample_data.py

# Ver estado
docker-compose ps
```

---

## 📊 Opciones de Datos

### Opción 1: Datos de Ejemplo (Recomendado para empezar)

**10 listings ficticios - Súper rápido**

```bash
# Con Make
make sample

# Con Docker Compose
docker-compose exec app python scripts/import_sample_data.py
```

⏱️ Tiempo: < 5 segundos
💾 Tamaño: ~30 KB

### Opción 2: Datos Completos

**~18,000 listings reales de Madrid**

```bash
# Con Make
make full

# Con Docker Compose
docker-compose exec app python scripts/download_dataset.py
docker-compose exec app python scripts/import_data.py
```

⏱️ Tiempo: 2-5 minutos
💾 Tamaño: ~50 MB

### Opción 3: Tus Propios Datos

**Tu CSV personalizado de Airbnb**

```bash
# Con Make
make data-custom
# Luego ingresa la ruta a tu CSV cuando te lo pida

# Con Docker Compose
docker cp tu_archivo.csv airbnb_app:/app/data/raw/
docker-compose exec app python scripts/import_custom_data.py \
    data/raw/tu_archivo.csv --keep-all
```

---

## 🚨 Solución Rápida de Problemas

### "Port 8888 already in use"

```bash
# Opción 1: Cambiar puerto en docker-compose.yml
# Cambiar "8888:8888" por "9999:8888"

# Opción 2: Detener proceso que usa el puerto
lsof -i :8888  # Ver qué usa el puerto
kill -9 [PID]  # Matar proceso
```

### "Cannot connect to Docker daemon"

```bash
# Iniciar Docker Desktop o daemon
sudo systemctl start docker  # Linux
# O abre Docker Desktop en Mac/Windows
```

### No hay datos en Jupyter

```bash
# Importar datos de ejemplo
make sample
# O
docker-compose exec app python scripts/import_sample_data.py
```

### "docker-compose: command not found"

```bash
# Instalar Docker Compose
# Linux:
sudo apt-get install docker-compose

# O usar docker compose (sin guión)
docker compose up -d
```

---

## 🎯 Flujo de Trabajo Típico

```bash
# 1. Primera vez
git clone [URL]
cd airbnb-madrid-mongodb-analysis
make up
make sample

# 2. Trabajar con notebooks
# Abre http://localhost:8888
# Edita notebooks...
# Se guardan automáticamente

# 3. Detener al finalizar
make down

# 4. Siguiente sesión
make up
# (Los datos persisten automáticamente)
```

---

## 💡 Tips

### Para Estudiantes/Principiantes

1. Empieza con `make sample` (datos de ejemplo)
2. Explora los notebooks en Jupyter
3. Cuando te sientas cómodo, usa `make full` (datos completos)

### Para Desarrollo

1. Edita archivos en `./src/` - se reflejan automáticamente
2. Crea notebooks en `./notebooks/` - se guardan localmente
3. Usa `make restart-app` si cambias código Python

### Para Presentaciones

1. `make up` antes de la presentación
2. Importa datos con `make full` (más impresionante)
3. Abre Jupyter y Mongo Express en pestañas separadas
4. `make down` al terminar

---

## 📱 Requisitos Mínimos

- **Sistema Operativo:** Linux, macOS, Windows (con WSL2)
- **Docker:** Versión 20.10+
- **Docker Compose:** Versión 2.0+
- **RAM:** Mínimo 4 GB
- **Disco:** 2 GB libres

---

## ✅ Checklist de Instalación

- [ ] Docker instalado y corriendo
- [ ] Git instalado
- [ ] Repositorio clonado
- [ ] `make up` ejecutado exitosamente
- [ ] Jupyter accesible en http://localhost:8888
- [ ] Datos importados (`make sample`)
- [ ] Notebooks funcionando

---

## 🆘 ¿Necesitas Ayuda?

1. **Revisa logs:** `make logs` o `docker-compose logs -f`
2. **Lee la guía completa:** [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
3. **Documentación oficial:** [Docker Docs](https://docs.docker.com/)
4. **Issues en GitHub:** [Reportar problema](https://github.com/TU-USERNAME/airbnb-madrid-mongodb-analysis/issues)

---

## 🎉 ¡Eso es Todo!

**En menos de 5 minutos deberías tener:**
- ✅ MongoDB corriendo
- ✅ Jupyter Notebook accesible
- ✅ Datos cargados
- ✅ Listo para explorar

**Sin instalar:**
- ❌ Python
- ❌ MongoDB
- ❌ Dependencias

**Solo necesitas Docker** 🐳

---

**Happy Coding!** 🚀

*Proyecto creado por GCP - Tax & Data Science Consultant*
