# 🏠 MongoDB Airbnb Madrid - CRUD Operations & Data Visualization

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 📋 Descripción

Proyecto completo de análisis de datos de Airbnb en Madrid utilizando MongoDB. El proyecto está dividido en dos partes principales:

**Parte 1:** Operaciones CRUD (Create, Read, Update, Delete) en MongoDB con datos reales de listings de Airbnb en Madrid, demostrando consultas avanzadas, agregaciones y optimización de queries.

**Parte 2:** Análisis exploratorio de datos (EDA) utilizando PyMongo para extraer insights y crear visualizaciones interactivas con Plotly, Matplotlib y Seaborn, revelando patrones de precios, disponibilidad y distribución geográfica de alojamientos.

Este proyecto es ideal para quienes buscan aprender MongoDB en un contexto real de análisis de datos, combinando operaciones de base de datos NoSQL con técnicas modernas de visualización de datos.

## ✨ Características Principales

### Parte 1: CRUD Operations
- 🔍 **Consultas Básicas y Avanzadas**: Filtrado, proyección y ordenamiento
- 📊 **Agregaciones MongoDB**: Pipeline de agregación para análisis complejos
- ✏️ **Operaciones de Escritura**: Inserción, actualización y eliminación de documentos
- 🚀 **Indexación**: Creación de índices para optimizar rendimiento
- 🔎 **Búsquedas Geoespaciales**: Queries basadas en ubicación

### Parte 2: Visualización & Analytics
- 📈 **Análisis de Precios**: Distribución, tendencias y outliers
- 🗺️ **Mapas Interactivos**: Visualización geográfica con Plotly
- 📊 **Dashboards**: Gráficos interactivos de métricas clave
- 🏘️ **Análisis por Barrios**: Comparativas entre zonas de Madrid
- ⭐ **Reviews y Ratings**: Análisis de satisfacción de usuarios

## 🎥 Demo

![Dashboard Preview](assets/dashboard_preview.png)
*Dashboard interactivo mostrando distribución de precios por barrio en Madrid*

![Mapa Geoespacial](assets/map_madrid.png)
*Mapa interactivo de listings de Airbnb en Madrid*

## 🛠️ Tecnologías Utilizadas

### Base de Datos
- **MongoDB 4.4+**: Base de datos NoSQL principal
- **MongoDB Atlas**: Cloud database (opcional)
- **PyMongo**: Driver oficial de Python para MongoDB

### Análisis y Visualización
- **Python 3.9+**: Lenguaje de programación
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Operaciones numéricas
- **Plotly**: Visualizaciones interactivas
- **Matplotlib**: Gráficos estáticos
- **Seaborn**: Visualizaciones estadísticas
- **Folium**: Mapas interactivos (opcional)

### Desarrollo
- **Jupyter Notebook**: Análisis exploratorio
- **Docker**: Containerización de MongoDB
- **Python dotenv**: Gestión de variables de entorno

## 🏗️ Arquitectura del Proyecto

```
┌─────────────┐
│   Python    │
│  (PyMongo)  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐      ┌──────────────────┐
│  MongoDB Local  │◄────►│  MongoDB Atlas   │
│   (Docker)      │      │    (Cloud)       │
└─────────────────┘      └──────────────────┘
       │
       ▼
┌─────────────────┐
│  Visualización  │
│ Plotly/Seaborn  │
└─────────────────┘
```

## 🚀 Inicio Rápido con Docker (Recomendado)

**¿Solo quieres probar el proyecto sin instalar nada?** ¡Usa Docker! 🐳

```bash
# 1. Clonar repositorio
git clone https://github.com/tuusername/airbnb-madrid-mongodb-analysis.git
cd airbnb-madrid-mongodb-analysis

# 2. Levantar servicios (MongoDB + Jupyter + Mongo Express)
docker-compose up -d

# 3. Importar datos de ejemplo (10 listings)
docker-compose exec app python scripts/import_sample_data.py

# ¡LISTO! Accede a Jupyter en: http://localhost:8888
```

**Todo funciona en Docker, sin instalar Python, MongoDB ni dependencias** ✨

📖 [Guía completa de Docker](DOCKER_GUIDE.md)

---

## 📦 Instalación Manual (Alternativa)

Si prefieres instalar localmente:

### Prerrequisitos

```bash
- Python 3.9 o superior
- MongoDB 4.4+ (local o Atlas)
- pip (gestor de paquetes de Python)
```

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/tuusername/airbnb-madrid-mongodb-analysis.git
cd airbnb-madrid-mongodb-analysis
```

### Paso 2: Crear Entorno Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar MongoDB

#### Opción A: MongoDB Local con Docker (Recomendado)

```bash
# Iniciar MongoDB con Docker Compose
docker-compose up -d

# Verificar que está corriendo
docker ps
```

#### Opción B: MongoDB Atlas (Cloud)

1. Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crear un cluster gratuito
3. Obtener connection string
4. Configurar en `.env`

### Paso 5: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

Contenido del `.env`:
```env
# MongoDB Local
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=airbnb_madrid

# O MongoDB Atlas
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
# MONGODB_DB=airbnb_madrid
```

### Paso 6: Cargar Datos de Airbnb

```bash
# Descargar dataset (si no está incluido)
python scripts/download_dataset.py

# Importar datos a MongoDB
python scripts/import_data.py
```

## 🚀 Uso

### Parte 1: CRUD Operations

#### Ejecutar Notebook Interactivo

```bash
jupyter notebook notebooks/01_crud_operations.ipynb
```

#### Ejemplos de Código - CRUD

**CREATE - Insertar documentos**
```python
from src.crud_operations import AirbnbCRUD

crud = AirbnbCRUD()

# Insertar un nuevo listing
new_listing = {
    "name": "Acogedor apartamento en Malasaña",
    "neighbourhood": "Centro",
    "room_type": "Entire home/apt",
    "price": 75,
    "minimum_nights": 2,
    "availability_365": 300
}

result = crud.create_listing(new_listing)
print(f"Listing creado con ID: {result.inserted_id}")
```

**READ - Consultas**
```python
# Buscar apartamentos en Centro con precio < 100€
listings = crud.find_listings({
    "neighbourhood": "Centro",
    "price": {"$lt": 100}
})

for listing in listings:
    print(f"{listing['name']} - {listing['price']}€")
```

**UPDATE - Actualizar documentos**
```python
# Actualizar precio de un listing
crud.update_listing(
    listing_id="12345",
    update_data={"price": 80}
)
```

**DELETE - Eliminar documentos**
```python
# Eliminar listings no disponibles
crud.delete_unavailable_listings()
```

#### Agregaciones Avanzadas

```python
# Precio promedio por barrio
pipeline = [
    {"$group": {
        "_id": "$neighbourhood",
        "avg_price": {"$avg": "$price"},
        "count": {"$sum": 1}
    }},
    {"$sort": {"avg_price": -1}}
]

results = crud.aggregate(pipeline)
```

### Parte 2: Visualización y Análisis

#### Ejecutar Análisis Completo

```bash
jupyter notebook notebooks/02_data_visualization.ipynb
```

#### Ejemplos de Visualizaciones

**Distribución de Precios**
```python
from src.visualizations import AirbnbVisualizer

viz = AirbnbVisualizer()

# Histograma de precios
fig = viz.price_distribution()
fig.show()

# Boxplot por tipo de habitación
fig = viz.price_by_room_type()
fig.show()
```

**Mapa Geoespacial**
```python
# Mapa interactivo de Madrid
fig = viz.create_map()
fig.show()
```

**Dashboard Completo**
```python
# Generar dashboard HTML interactivo
viz.create_dashboard(output_path="reports/dashboard.html")
```

## 📊 Análisis y Resultados

### Insights Principales

1. **Distribución de Precios**
   - Precio promedio: 85€/noche
   - Rango más común: 50-100€
   - Outliers: Listings de lujo >300€

2. **Barrios Más Caros**
   - Salamanca: 120€/noche promedio
   - Chamberí: 95€/noche promedio
   - Centro: 90€/noche promedio

3. **Tipos de Alojamiento**
   - 65% Apartamentos completos
   - 25% Habitaciones privadas
   - 10% Habitaciones compartidas

4. **Disponibilidad**
   - 45% disponibles >200 días/año
   - Mayor ocupación en verano
   - Estancias mínimas: 2-3 noches promedio

### Visualizaciones Generadas

Ver carpeta `reports/` para dashboards HTML interactivos y gráficos en alta resolución.

## 📁 Estructura del Proyecto

```
airbnb-madrid-mongodb-analysis/
│
├── README.md                          # Este archivo
├── LICENSE                            # Licencia MIT
├── .gitignore                        # Archivos a ignorar
├── requirements.txt                   # Dependencias Python
├── docker-compose.yml                 # Configuración Docker
├── .env.example                      # Variables de entorno ejemplo
│
├── data/                             # Datos del proyecto
│   ├── raw/                          # Datos originales
│   │   └── madrid_listings.csv
│   ├── processed/                    # Datos procesados
│   │   └── cleaned_listings.json
│   └── sample/                       # Datos de ejemplo
│       └── sample_10_listings.json
│
├── notebooks/                        # Jupyter Notebooks
│   ├── 01_crud_operations.ipynb      # Parte 1: CRUD
│   ├── 02_data_visualization.ipynb   # Parte 2: Visualización
│   └── 03_advanced_analytics.ipynb   # Análisis avanzado
│
├── src/                              # Código fuente
│   ├── __init__.py
│   ├── config.py                     # Configuración
│   ├── database.py                   # Conexión MongoDB
│   ├── crud_operations.py            # Operaciones CRUD
│   ├── visualizations.py             # Funciones de visualización
│   ├── analytics.py                  # Análisis de datos
│   └── utils.py                      # Utilidades
│
├── scripts/                          # Scripts utilitarios
│   ├── download_dataset.py           # Descargar datos Airbnb
│   ├── import_data.py               # Importar a MongoDB
│   ├── create_indexes.py            # Crear índices
│   └── export_results.py            # Exportar resultados
│
├── tests/                            # Tests unitarios
│   ├── test_crud.py
│   ├── test_visualizations.py
│   └── test_database.py
│
├── reports/                          # Reportes generados
│   ├── dashboard.html               # Dashboard interactivo
│   └── figures/                     # Gráficos estáticos
│
├── assets/                           # Recursos multimedia
│   ├── dashboard_preview.png
│   ├── map_madrid.png
│   └── architecture_diagram.png
│
└── docs/                             # Documentación adicional
    ├── CRUD_GUIDE.md                # Guía de operaciones CRUD
    ├── VISUALIZATION_GUIDE.md       # Guía de visualizaciones
    └── MONGODB_TIPS.md              # Tips de MongoDB
```

## 🧪 Tests

Ejecutar todos los tests:

```bash
pytest tests/ -v
```

Tests específicos:

```bash
# Test CRUD operations
pytest tests/test_crud.py

# Test visualizations
pytest tests/test_visualizations.py
```

## 📚 Recursos de Aprendizaje

Este proyecto incluye:

- 📖 **Notebooks documentados**: Cada celda explicada paso a paso
- 💡 **Mejores prácticas**: Código limpio y optimizado
- 🎓 **Conceptos teóricos**: Explicación de agregaciones y queries
- 🔍 **Casos de uso reales**: Análisis de negocio aplicado

### Conceptos MongoDB Cubiertos

- Modelado de datos NoSQL
- Queries y proyecciones
- Aggregation Framework
- Índices y optimización
- Operadores de consulta ($gt, $in, $regex, etc.)
- Operadores de actualización ($set, $inc, $push, etc.)
- Geospatial queries
- Text search

## 🗺️ Roadmap

- [x] Implementar operaciones CRUD básicas
- [x] Crear visualizaciones con Plotly
- [x] Análisis de precios por barrio
- [x] Mapa geoespacial interactivo
- [ ] Implementar búsqueda de texto completo
- [ ] Añadir predicción de precios con ML
- [ ] Dashboard en tiempo real con Streamlit
- [ ] API REST con FastAPI
- [ ] Análisis de sentimiento de reviews

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**GCP - Tax & Data Science Consultant**

- 🎓 MSc Data Science & Big Data - Universidad Complutense Madrid
- 💼 Tax Consultant | Data Scientist | AI Specialist
- 🌍 Madrid, España
- LinkedIn: https://www.linkedin.com/in/gustavocevallosp/
- GitHub: @gustavocevallos | https://github.com/gustavocevallos
- Email: gcevallos@dattax.ec

## 🙏 Agradecimientos

- **Inside Airbnb**: Por proveer los datos abiertos de Airbnb
- **MongoDB**: Por su excelente documentación
- **Plotly**: Por la increíble librería de visualización

## 📊 Dataset

Los datos utilizados provienen de [Inside Airbnb](http://insideairbnb.com/get-the-data.html) - Madrid, España.

**Última actualización**: 2025 
**Registros**: ~18,000 listings  
**Campos principales**: name, neighbourhood, room_type, price, availability, reviews, coordinates

---

⭐ **Si este proyecto te resultó útil, considera darle una estrella en GitHub**

🐛 **¿Encontraste un bug?** [Reporta un issue](https://github.com/gustavocevallos/airbnb-madrid-mongodb-analysis/issues)

💬 **¿Tienes preguntas?** [Inicia una discusión](https://github.com/gustavocevallos/airbnb-madrid-mongodb-analysis/discussions)
