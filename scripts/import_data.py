#!/usr/bin/env python3
"""
Script para importar datos de Airbnb a MongoDB
"""

from src.crud_operations import AirbnbCRUD
from src.database import MongoDBConnection
from src.config import RAW_DATA_DIR, SAMPLE_SIZE
import os
import sys
import logging
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y prepara el DataFrame para importación

    Args:
        df: DataFrame original

    Returns:
        pd.DataFrame: DataFrame limpio
    """
    logger.info("🧹 Limpiando datos...")

    # Columnas importantes a mantener
    important_cols = [
        'id', 'name', 'host_id', 'host_name', 'neighbourhood',
        'latitude', 'longitude', 'room_type', 'price',
        'minimum_nights', 'number_of_reviews', 'last_review',
        'reviews_per_month', 'calculated_host_listings_count',
        'availability_365'
    ]

    # Seleccionar solo columnas que existen
    available_cols = [col for col in important_cols if col in df.columns]
    df = df[available_cols].copy()

    # Limpiar precios (remover $ y convertir a float)
    if 'price' in df.columns:
        df['price'] = df['price'].replace(
            r'[\$,]', '', regex=True).astype(float)

    # Convertir fechas
    if 'last_review' in df.columns:
        df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')

    # Rellenar valores nulos
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    df['name'] = df['name'].fillna('Sin nombre')
    df['host_name'] = df['host_name'].fillna('Sin nombre')

    # Crear campo de ubicación geoespacial
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['location'] = df.apply(
            lambda row: {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            axis=1
        )

    logger.info(
        f"✅ Datos limpios: {len(df)} registros, {len(df.columns)} columnas")

    return df


def import_data(
    csv_path: Path,
    sample_size: int = 0,
    batch_size: int = 1000
) -> None:
    """
    Importa datos del CSV a MongoDB

    Args:
        csv_path: Ruta del archivo CSV
        sample_size: Número de registros a importar (0 = todos)
        batch_size: Tamaño del lote para inserción
    """
    try:
        logger.info(f"📖 Leyendo archivo: {csv_path}")

        # Leer CSV
        df = pd.read_csv(csv_path, low_memory=False)
        logger.info(f"✅ Archivo cargado: {len(df):,} registros")

        # Aplicar sample si se especifica
        if sample_size > 0:
            df = df.sample(n=min(sample_size, len(df)), random_state=42)
            logger.info(f"📊 Usando muestra de {len(df):,} registros")

        # Limpiar datos
        df = clean_dataframe(df)

        # Conectar a MongoDB
        logger.info("🔌 Conectando a MongoDB...")
        conn = MongoDBConnection()
        crud = AirbnbCRUD()

        # Verificar si la colección ya tiene datos
        existing_count = crud.get_total_listings()
        if existing_count > 0:
            logger.warning(
                f"⚠️ La colección ya tiene {existing_count:,} documentos")
            response = input("¿Deseas eliminar los datos existentes? (s/n): ")
            if response.lower() == 's':
                crud.collection.delete_many({})
                logger.info("🗑️ Datos existentes eliminados")
            else:
                logger.info("Importación cancelada")
                return

        # Convertir a documentos
        documents = df.to_dict('records')

        # Importar en lotes
        logger.info(f"� Importando {len(documents):,} documentos...")

        total_inserted = 0
        for i in tqdm(range(0, len(documents), batch_size), desc="Importando"):
            batch = documents[i:i+batch_size]

            # Agregar metadata
            for doc in batch:
                doc['imported_at'] = datetime.now()

            result = crud.create_many_listings(batch)
            total_inserted += len(result.inserted_ids)

        logger.info(f"✅ Importación completada: {total_inserted:,} documentos")

        # Crear índices
        logger.info("📑 Creando índices...")
        conn.create_indexes()

        # Mostrar estadísticas
        stats = conn.get_collection_stats()
        logger.info("\n📊 Estadísticas de la colección:")
        logger.info(f"  - Documentos: {stats['count']:,}")
        logger.info(f"  - Tamaño: {stats['size'] / 1024 / 1024:.2f} MB")
        logger.info(f"  - Índices: {stats['indexes']}")

        # Estadísticas básicas
        logger.info("\n🔍 Estadísticas de datos:")
        price_stats = df['price'].describe()
        logger.info(f"  - Precio promedio: {price_stats['mean']:.2f}€")
        logger.info(f"  - Precio mediano: {price_stats['50%']:.2f}€")
        logger.info(f"  - Barrios únicos: {df['neighbourhood'].nunique()}")
        logger.info(f"  - Tipos de alojamiento: {df['room_type'].nunique()}")

    except FileNotFoundError:
        logger.error(f"❌ Archivo no encontrado: {csv_path}")
        logger.info("💡 Ejecuta 'python scripts/download_dataset.py' primero")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error durante la importación: {e}")
        raise


def main():
    """Función principal"""

    print("\n" + "="*60)
    print("📥 IMPORTACIÓN DE DATOS A MONGODB")
    print("="*60 + "\n")

    # Buscar archivo CSV
    csv_file = RAW_DATA_DIR / "madrid_listings.csv"

    if not csv_file.exists():
        logger.error(f"❌ No se encontró el archivo: {csv_file}")
        logger.info("💡 Ejecuta 'python scripts/download_dataset.py' primero")
        sys.exit(1)

    # Importar datos
    import_data(csv_file, sample_size=SAMPLE_SIZE)

    print("\n" + "="*60)
    print("🎉 ¡IMPORTACIÓN COMPLETADA!")
    print("="*60)
    print("\n💡 Siguiente paso: Explora los datos con los notebooks en /notebooks\n")


if __name__ == "__main__":
    main()
