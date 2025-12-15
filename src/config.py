"""
Configuración del proyecto Airbnb Madrid MongoDB Analysis
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Directorios del proyecto
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Crear directorios si no existen
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR, REPORTS_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuración de MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://admin:admin123@localhost:27017/")
MONGODB_DB = os.getenv("MONGODB_DB", "airbnb_madrid")
COLLECTION_NAME = "listings"

# Configuración de la aplicación
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configuración de datos
DATA_PATH = os.getenv("DATA_PATH", str(RAW_DATA_DIR / "madrid_listings.csv"))
SAMPLE_SIZE = int(os.getenv("SAMPLE_SIZE", "0"))  # 0 = importar todos

# Configuración de visualización
PLOTLY_RENDERER = os.getenv("PLOTLY_RENDERER", "browser")
EXPORT_FORMAT = os.getenv("EXPORT_FORMAT", "html")

# Configuración de colores para visualizaciones
COLOR_PALETTE = {
    "primary": "#FF385C",      # Airbnb Red
    "secondary": "#00A699",    # Teal
    "accent": "#FC642D",       # Orange
    "background": "#FFFFFF",   # White
    "text": "#484848",         # Dark Gray
    "light_gray": "#EBEBEB"
}

# Mapeo de tipos de habitación
ROOM_TYPE_MAPPING = {
    "Entire home/apt": "Apartamento completo",
    "Private room": "Habitación privada",
    "Shared room": "Habitación compartida",
    "Hotel room": "Habitación de hotel"
}

# Configuración de Plotly
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
}

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console']
    }
}

# URLs útiles
AIRBNB_DATA_URL = "http://data.insideairbnb.com/spain/comunidad-de-madrid/madrid/2024-12-18/data/listings.csv.gz"

def get_mongodb_connection_string() -> str:
    """Retorna el string de conexión de MongoDB"""
    return MONGODB_URI

def get_database_name() -> str:
    """Retorna el nombre de la base de datos"""
    return MONGODB_DB

def get_collection_name() -> str:
    """Retorna el nombre de la colección"""
    return COLLECTION_NAME

# Validación de configuración
def validate_config():
    """Valida que la configuración sea correcta"""
    errors = []
    
    if not MONGODB_URI:
        errors.append("MONGODB_URI no está configurado")
    
    if not MONGODB_DB:
        errors.append("MONGODB_DB no está configurado")
    
    if errors:
        raise ValueError(f"Errores de configuración: {', '.join(errors)}")
    
    return True

if __name__ == "__main__":
    validate_config()
    print("✅ Configuración validada correctamente")
    print(f"📊 Base de datos: {MONGODB_DB}")
    print(f"📁 Directorio de datos: {DATA_DIR}")
