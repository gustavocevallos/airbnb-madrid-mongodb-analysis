"""
Configuración de la aplicación
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27018/')
MONGODB_DB = os.getenv('MONGODB_DB', 'airbnb_madrid')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'listings')

# Application Settings
APP_ENV = os.getenv('APP_ENV', 'development')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Data Settings
DATA_PATH = os.getenv('DATA_PATH', './data/raw')
SAMPLE_SIZE = int(os.getenv('SAMPLE_SIZE', '0'))

# Visualization Settings
COLOR_PALETTE = {
    'primary': '#FF5A5F',      # Airbnb red
    'secondary': '#00A699',    # Airbnb teal
    'accent': '#FC642D',       # Airbnb orange
    'neutral': '#484848',      # Dark gray
    'light': '#767676',        # Light gray
    'background': '#FFFFFF'    # White
}

PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
}

ROOM_TYPE_MAPPING = {
    'Entire home/apt': 'Vivienda completa',
    'Private room': 'Habitación privada',
    'Shared room': 'Habitación compartida',
    'Hotel room': 'Habitación de hotel'
}

# Plotly Renderer
PLOTLY_RENDERER = os.getenv('PLOTLY_RENDERER', 'browser')

# Export Format
EXPORT_FORMAT = os.getenv('EXPORT_FORMAT', 'html')

# Print config for debugging
if __name__ == "__main__":
    print("=== CONFIGURACIÓN ===")
    print(f"MONGODB_URI: {MONGODB_URI}")
    print(f"MONGODB_DB: {MONGODB_DB}")
    print(f"COLLECTION_NAME: {COLLECTION_NAME}")
    print(f"APP_ENV: {APP_ENV}")
    print(f"LOG_LEVEL: {LOG_LEVEL}")
