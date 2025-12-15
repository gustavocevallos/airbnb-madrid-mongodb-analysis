#!/usr/bin/env python3
"""
Script para importar los datos de ejemplo al contenedor Docker
"""

import sys
import json
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import MongoDBConnection
from src.crud_operations import AirbnbCRUD

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def import_sample_data():
    """Importa los datos de ejemplo a MongoDB"""
    
    print("\n" + "="*60)
    print("📥 IMPORTANDO DATOS DE EJEMPLO")
    print("="*60 + "\n")
    
    # Ruta al archivo de ejemplo
    sample_file = Path(__file__).parent.parent / "data" / "sample" / "sample_10_listings.json"
    
    if not sample_file.exists():
        logger.error(f"❌ Archivo no encontrado: {sample_file}")
        return False
    
    try:
        # Leer datos
        logger.info(f"📖 Leyendo archivo: {sample_file.name}")
        with open(sample_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"✅ Archivo cargado: {len(data)} registros")
        
        # Conectar a MongoDB
        logger.info("🔌 Conectando a MongoDB...")
        conn = MongoDBConnection()
        crud = AirbnbCRUD()
        
        # Verificar si ya hay datos
        existing_count = crud.get_total_listings()
        if existing_count > 0:
            logger.warning(f"⚠️ La base de datos ya tiene {existing_count} documentos")
            print("\n💡 Si quieres reemplazarlos, primero elimínalos:")
            print("   docker-compose exec app python -c \"from src.crud_operations import AirbnbCRUD; AirbnbCRUD().collection.delete_many({})\"")
            return False
        
        # Importar datos
        logger.info("📥 Importando datos de ejemplo...")
        result = crud.create_many_listings(data)
        
        logger.info(f"✅ {len(result.inserted_ids)} documentos importados")
        
        # Crear índices
        logger.info("📑 Creando índices...")
        conn.create_indexes()
        
        # Mostrar estadísticas
        stats = conn.get_collection_stats()
        logger.info(f"\n📊 Estadísticas:")
        logger.info(f"  - Documentos: {stats['count']:,}")
        logger.info(f"  - Tamaño: {stats['size'] / 1024:.2f} KB")
        logger.info(f"  - Índices: {stats['indexes']}")
        
        print("\n" + "="*60)
        print("🎉 ¡DATOS IMPORTADOS EXITOSAMENTE!")
        print("="*60)
        print("\n📍 Accede a Jupyter en: http://localhost:8888")
        print("📍 Mongo Express en: http://localhost:8081\n")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error al importar datos: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = import_sample_data()
    sys.exit(0 if success else 1)
