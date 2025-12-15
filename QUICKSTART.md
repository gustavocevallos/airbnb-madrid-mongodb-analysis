# 🚀 Guía Rápida de Inicio

## Setup en 5 Minutos

### 1️⃣ Clonar e Instalar

```bash
# Clonar repositorio
git clone https://github.com/tuusername/airbnb-madrid-mongodb-analysis.git
cd airbnb-madrid-mongodb-analysis

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Iniciar MongoDB

**Opción A: Docker (Recomendado)**
```bash
docker-compose up -d
```

**Opción B: MongoDB Atlas**
1. Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crear cluster
3. Copiar connection string

### 3️⃣ Configurar Variables

```bash
cp .env.example .env
nano .env  # Editar con tus credenciales
```

### 4️⃣ Descargar e Importar Datos

```bash
# Descargar dataset de Airbnb
python scripts/download_dataset.py

# Importar a MongoDB
python scripts/import_data.py
```

### 5️⃣ ¡Listo! Empezar a Explorar

```bash
# Iniciar Jupyter
jupyter notebook

# Abrir notebooks/01_crud_operations.ipynb
```

## 📝 Notas Importantes

- **MongoDB**: Debe estar corriendo antes de importar datos
- **Dataset**: ~18,000 listings de Madrid (último update: Dic 2024)
- **Tiempo de importación**: 2-5 minutos dependiendo de tu conexión

## 🆘 Problemas Comunes

### MongoDB no conecta
```bash
# Verificar que Docker esté corriendo
docker ps

# Reiniciar contenedor
docker-compose restart
```

### Error al importar
```bash
# Verificar que el archivo existe
ls data/raw/madrid_listings.csv

# Descargar nuevamente
python scripts/download_dataset.py
```

## 🎯 Estructura del Proyecto

```
.
├── notebooks/          # Jupyter notebooks (¡EMPIEZA AQUÍ!)
├── src/               # Código fuente
├── scripts/           # Scripts de utilidad
├── data/              # Datos (se crea automáticamente)
└── reports/           # Reportes generados
```

## 📚 Siguientes Pasos

1. ✅ Completar setup inicial
2. 📖 Abrir `notebooks/01_crud_operations.ipynb`
3. 📊 Continuar con `notebooks/02_data_visualization.ipynb`
4. 🎨 Explorar y crear tus propios análisis

## 💡 Tips

- Usa `SAMPLE_SIZE=1000` en `.env` para importar solo 1000 registros (más rápido para pruebas)
- MongoDB Express está disponible en http://localhost:8081 (user: admin, pass: admin123)
- Los gráficos se guardan automáticamente en `reports/`

---

**¿Tienes preguntas?** Abre un [issue](https://github.com/tuusername/airbnb-madrid-mongodb-analysis/issues) en GitHub
