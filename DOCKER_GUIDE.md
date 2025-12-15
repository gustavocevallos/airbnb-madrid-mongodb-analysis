# 🐳 Guía Docker - Inicio Rápido en 2 Comandos

## 🚀 Inicio Ultra Rápido

### Para Usuarios (Sin instalar nada excepto Docker)

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USERNAME/airbnb-madrid-mongodb-analysis.git
cd airbnb-madrid-mongodb-analysis

# 2. Levantar TODO con Docker Compose
docker-compose up -d

# 3. Importar datos de ejemplo (10 listings)
docker-compose exec app python scripts/import_sample_data.py

# ¡LISTO! Accede a:
# 📓 Jupyter: http://localhost:8888
# 🗄️ Mongo Express: http://localhost:8081 (user: admin, pass: admin123)
```

**¡En menos de 5 minutos tienes el proyecto completo funcionando!** ⚡

---

## 🎯 ¿Qué incluye?

Cuando ejecutas `docker-compose up`, se levantan automáticamente:

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **MongoDB** | 27017 | Base de datos NoSQL |
| **Jupyter Notebook** | 8888 | Notebooks interactivos (sin password) |
| **Mongo Express** | 8081 | Interface web para MongoDB |
| **App Python** | - | Código fuente y scripts |

---

## 📦 Servicios Incluidos

### 1. MongoDB (Base de Datos)
```bash
# Ver logs de MongoDB
docker-compose logs -f mongodb

# Conectar directamente
docker-compose exec mongodb mongosh -u admin -p admin123
```

### 2. Jupyter Notebook (Interfaz Principal)
```bash
# Acceder a Jupyter
http://localhost:8888

# Ver logs
docker-compose logs -f app

# Ejecutar comandos Python
docker-compose exec app python -c "from src.crud_operations import AirbnbCRUD; print(f'Total: {AirbnbCRUD().get_total_listings()}')"
```

### 3. Mongo Express (Admin UI)
```bash
# Acceder a Mongo Express
http://localhost:8081

# Credenciales:
# Usuario: admin
# Password: admin123
```

---

## 📊 Opciones de Datos

### Opción 1: Datos de Ejemplo (Rápido - 10 listings)

```bash
# Importar 10 listings de ejemplo
docker-compose exec app python scripts/import_sample_data.py
```

**Ventajas:**
- ⚡ Súper rápido (< 1 segundo)
- 💾 Ligero (solo 10 documentos)
- 🎯 Perfecto para probar el proyecto

### Opción 2: Datos Completos (~18,000 listings)

```bash
# Descargar datos reales de Inside Airbnb
docker-compose exec app python scripts/download_dataset.py

# Importar a MongoDB
docker-compose exec app python scripts/import_data.py
```

**Ventajas:**
- 📊 Dataset completo de Madrid
- 🔍 Análisis más profundos
- 📈 Visualizaciones más ricas

### Opción 3: Tus Propios Datos

```bash
# 1. Copiar tu CSV al contenedor
docker cp tu_archivo.csv airbnb_app:/app/data/raw/

# 2. Importar con el script personalizado
docker-compose exec app python scripts/import_custom_data.py \
    data/raw/tu_archivo.csv \
    --keep-all
```

---

## 🎓 Uso del Proyecto

### 1. Abrir Jupyter Notebook

```bash
# El servidor Jupyter está en http://localhost:8888
# No requiere password
```

**Notebooks disponibles:**
- `01_crud_operations.ipynb` - Tutorial de operaciones CRUD
- `02_data_visualization.ipynb` - Visualizaciones interactivas
- Crea los tuyos! Se guardan automáticamente

### 2. Ejecutar Scripts Python

```bash
# Ejecutar script directamente
docker-compose exec app python scripts/import_sample_data.py

# Python interactivo
docker-compose exec app python

# Ver estadísticas rápidas
docker-compose exec app python -c "
from src.crud_operations import AirbnbCRUD
crud = AirbnbCRUD()
print(f'Total listings: {crud.get_total_listings():,}')
print(f'Barrios: {len(crud.get_distinct_values(\"neighbourhood\"))}')
"
```

### 3. Explorar MongoDB

```bash
# Opción A: Mongo Express (Web UI)
# http://localhost:8081

# Opción B: Línea de comandos
docker-compose exec mongodb mongosh -u admin -p admin123 airbnb_madrid

# Ejemplo de queries:
db.listings.countDocuments()
db.listings.find({neighbourhood: "Centro"}).limit(5)
db.listings.aggregate([
  {$group: {_id: "$neighbourhood", count: {$sum: 1}}},
  {$sort: {count: -1}},
  {$limit: 5}
])
```

---

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f app
docker-compose logs -f mongodb

# Detener servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar TODO (incluyendo volúmenes/datos)
docker-compose down -v

# Reiniciar un servicio
docker-compose restart app

# Ver estado
docker-compose ps
```

### Acceso a Contenedores

```bash
# Bash en el contenedor de la app
docker-compose exec app bash

# MongoDB shell
docker-compose exec mongodb mongosh -u admin -p admin123

# Ver archivos en el contenedor
docker-compose exec app ls -la
```

### Gestión de Datos

```bash
# Backup de MongoDB
docker-compose exec mongodb mongodump \
    --username admin \
    --password admin123 \
    --authenticationDatabase admin \
    --db airbnb_madrid \
    --out /data/backup

# Restore de MongoDB
docker-compose exec mongodb mongorestore \
    --username admin \
    --password admin123 \
    --authenticationDatabase admin \
    --db airbnb_madrid \
    /data/backup/airbnb_madrid

# Limpiar base de datos
docker-compose exec app python -c "
from src.crud_operations import AirbnbCRUD
AirbnbCRUD().collection.delete_many({})
print('✅ Base de datos limpiada')
"
```

### Debugging

```bash
# Ver uso de recursos
docker stats

# Inspeccionar contenedor
docker inspect airbnb_app

# Ver variables de entorno
docker-compose exec app env

# Verificar conectividad
docker-compose exec app ping mongodb

# Test de conexión MongoDB
docker-compose exec app python -c "
from src.database import MongoDBConnection
conn = MongoDBConnection()
print('✅ Conexión exitosa' if conn.ping() else '❌ Error')
"
```

---

## 🔧 Personalización

### Cambiar Puertos

Edita `docker-compose.yml`:

```yaml
services:
  app:
    ports:
      - "9999:8888"  # Jupyter en puerto 9999
  
  mongo-express:
    ports:
      - "9000:8081"  # Mongo Express en puerto 9000
```

### Variables de Entorno

Crea un archivo `.env` en la raíz:

```env
# MongoDB
MONGODB_ROOT_USER=admin
MONGODB_ROOT_PASSWORD=admin123
MONGODB_DATABASE=airbnb_madrid

# Application
SAMPLE_SIZE=1000
LOG_LEVEL=DEBUG
```

Luego modifica `docker-compose.yml`:

```yaml
services:
  mongodb:
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGODB_ROOT_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_ROOT_PASSWORD}
```

### Agregar Dependencias

```bash
# Agregar a requirements.txt
echo "streamlit==1.29.0" >> requirements.txt

# Rebuild imagen
docker-compose build app

# Reiniciar
docker-compose up -d app
```

---

## 🚨 Solución de Problemas

### "Port already in use"

```bash
# Ver qué proceso usa el puerto 8888
lsof -i :8888

# Cambiar puerto en docker-compose.yml o detener el proceso
```

### "Cannot connect to MongoDB"

```bash
# Verificar que MongoDB esté corriendo
docker-compose ps

# Ver logs de MongoDB
docker-compose logs mongodb

# Reiniciar MongoDB
docker-compose restart mongodb
```

### "No space left on device"

```bash
# Limpiar imágenes y contenedores no usados
docker system prune -a

# Ver uso de disco
docker system df
```

### Jupyter no se conecta

```bash
# Verificar logs
docker-compose logs app

# Reiniciar servicio
docker-compose restart app

# Acceder directamente al contenedor
docker-compose exec app bash
jupyter notebook list
```

### Datos no persisten

```bash
# Verificar volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect airbnb-madrid-mongodb-analysis_mongodb_data

# Asegurar que no usas -v al bajar
docker-compose down  # ✅ Correcto (mantiene datos)
docker-compose down -v  # ❌ Elimina datos
```

---

## 📊 Volúmenes y Persistencia

Los datos persisten en volúmenes Docker:

```bash
# Ver volúmenes
docker volume ls

# Inspeccionar volumen de MongoDB
docker volume inspect airbnb-madrid-mongodb-analysis_mongodb_data

# Backup del volumen
docker run --rm \
    -v airbnb-madrid-mongodb-analysis_mongodb_data:/data \
    -v $(pwd):/backup \
    busybox tar -czf /backup/mongodb_backup.tar.gz /data
```

**Directorios sincronizados con el host:**
- `./notebooks` → `/app/notebooks` (notebooks se guardan localmente)
- `./data` → `/app/data` (datos accesibles desde el host)
- `./reports` → `/app/reports` (reportes generados)
- `./src` → `/app/src` (edita código en vivo)

---

## 🎯 Workflows Comunes

### Workflow 1: Desarrollador

```bash
# 1. Levantar servicios
docker-compose up -d

# 2. Importar datos de ejemplo
docker-compose exec app python scripts/import_sample_data.py

# 3. Abrir Jupyter
# http://localhost:8888

# 4. Desarrollar notebooks...

# 5. Editar código en ./src (se refleja automáticamente)

# 6. Reiniciar si es necesario
docker-compose restart app
```

### Workflow 2: Demo/Presentación

```bash
# 1. Levantar TODO
docker-compose up -d

# 2. Importar datos completos
docker-compose exec app python scripts/download_dataset.py
docker-compose exec app python scripts/import_data.py

# 3. Abrir Jupyter y ejecutar notebooks
# http://localhost:8888

# 4. Mostrar Mongo Express
# http://localhost:8081
```

### Workflow 3: Análisis con Datos Propios

```bash
# 1. Levantar servicios
docker-compose up -d

# 2. Copiar tu dataset
docker cp mi_dataset.csv airbnb_app:/app/data/raw/

# 3. Importar
docker-compose exec app python scripts/import_custom_data.py \
    data/raw/mi_dataset.csv --keep-all

# 4. Analizar en Jupyter
# http://localhost:8888
```

---

## 🎓 Para Enseñanza/Workshops

Si usas este proyecto para enseñar:

```bash
# 1. Los estudiantes clonan el repo
git clone https://github.com/TU-USERNAME/airbnb-madrid-mongodb-analysis.git
cd airbnb-madrid-mongodb-analysis

# 2. Levantan los servicios
docker-compose up -d

# 3. Importan datos de ejemplo
docker-compose exec app python scripts/import_sample_data.py

# 4. Acceden a Jupyter
# http://localhost:8888

# ¡Sin instalar nada más!
```

---

## 📝 Notas Importantes

### Seguridad

⚠️ **Este setup es para desarrollo/educación**

Para producción:
- Cambia passwords por defecto
- Usa variables de entorno
- No expongas puertos innecesarios
- Configura authentication en Jupyter
- Usa HTTPS

### Performance

- MongoDB usa un volumen para persistencia
- Primera importación de datos grandes puede tardar 2-5 min
- Notebooks se ejecutan en el contenedor (CPU/RAM del host)

### Compatibilidad

Funciona en:
- ✅ Linux (x86_64, ARM64)
- ✅ macOS (Intel, Apple Silicon)
- ✅ Windows (WSL2 requerido)

---

## 🆘 Ayuda

### Recursos

- [Docker Docs](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [MongoDB Docker](https://hub.docker.com/_/mongo)
- [Jupyter Docker](https://jupyter-docker-stacks.readthedocs.io/)

### Comunidad

- GitHub Issues: [Reportar problema]
- Discussions: [Hacer preguntas]

---

## 🎉 ¡Listo!

Con estos comandos, **cualquier persona puede usar tu proyecto** sin instalar:
- ❌ Python
- ❌ MongoDB
- ❌ Pandas/Plotly/etc
- ❌ Jupyter

**Solo necesitan Docker** 🐳

---

**Desarrollado por:** GCP - Tax & Data Science Consultant  
**Licencia:** MIT
