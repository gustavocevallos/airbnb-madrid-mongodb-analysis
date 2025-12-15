#!/usr/bin/env python3
"""
Script para importar TU PROPIO dataset de Airbnb
Soporta CSV con cualquier número de columnas
"""

from src.crud_operations import AirbnbCRUD
from src.database import MongoDBConnection
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


def analyze_columns(df: pd.DataFrame) -> dict:
    """
    Analiza las columnas del CSV y devuelve información útil

    Args:
        df: DataFrame de Pandas

    Returns:
        dict: Información sobre las columnas
    """
    info = {
        'total_columns': len(df.columns),
        'total_rows': len(df),
        'columns': list(df.columns),
        'has_location': 'latitude' in df.columns and 'longitude' in df.columns,
        'has_price': 'price' in df.columns,
        'has_reviews': 'number_of_reviews' in df.columns
    }

    return info


def clean_custom_dataframe(df: pd.DataFrame, keep_all_columns: bool = False) -> pd.DataFrame:
    """
    Limpia y prepara TU DataFrame personalizado

    Args:
        df: DataFrame original
        keep_all_columns: Si True, mantiene TODAS las columnas del CSV original

    Returns:
        pd.DataFrame: DataFrame limpio
    """
    import pandas as pd
    logger.info("🧹 Limpiando datos personalizados...")

    # Si keep_all_columns es True, usar todas las columnas
    if keep_all_columns:
        logger.info(
            f"📊 Manteniendo TODAS las columnas: {len(df.columns)} columnas")
    else:
        # Columnas importantes estándar de Airbnb
        important_cols = [
            'id', 'listing_url', 'scrape_id', 'last_scraped',
            'name', 'description', 'neighborhood_overview', 'picture_url',
            'host_id', 'host_url', 'host_name', 'host_since', 'host_location',
            'host_about', 'host_response_time', 'host_response_rate',
            'host_acceptance_rate', 'host_is_superhost', 'host_thumbnail_url',
            'host_picture_url', 'host_neighbourhood', 'host_listings_count',
            'host_total_listings_count', 'host_verifications',
            'host_has_profile_pic', 'host_identity_verified',
            'neighbourhood', 'neighbourhood_cleansed', 'neighbourhood_group_cleansed',
            'latitude', 'longitude', 'property_type', 'room_type',
            'accommodates', 'bathrooms', 'bathrooms_text', 'bedrooms', 'beds',
            'amenities', 'price', 'minimum_nights', 'maximum_nights',
            'minimum_minimum_nights', 'maximum_minimum_nights',
            'minimum_maximum_nights', 'maximum_maximum_nights',
            'minimum_nights_avg_ntm', 'maximum_nights_avg_ntm',
            'calendar_updated', 'has_availability', 'availability_30',
            'availability_60', 'availability_90', 'availability_365',
            'calendar_last_scraped', 'number_of_reviews', 'number_of_reviews_ltm',
            'number_of_reviews_l30d', 'first_review', 'last_review',
            'review_scores_rating', 'review_scores_accuracy',
            'review_scores_cleanliness', 'review_scores_checkin',
            'review_scores_communication', 'review_scores_location',
            'review_scores_value', 'license', 'instant_bookable',
            'calculated_host_listings_count', 'calculated_host_listings_count_entire_homes',
            'calculated_host_listings_count_private_rooms',
            'calculated_host_listings_count_shared_rooms',
            'reviews_per_month'
        ]

        # Seleccionar solo columnas que existen
        available_cols = [col for col in important_cols if col in df.columns]
        df = df[available_cols].copy()
        logger.info(
            f"📊 Columnas seleccionadas: {len(available_cols)} de {len(important_cols)} estándar")

    # LIMPIEZA UNIVERSAL (aplica a cualquier dataset)

    # 1. Limpiar precios (remover $ y convertir a float)
    if 'price' in df.columns:
        logger.info("💰 Limpiando campo 'price'...")
        # FIX: Agregar r antes del string
        df['price'] = df['price'].replace(r'[\$,]', '', regex=True)
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['price'] = df['price'].fillna(0)

    # 2. Convertir fechas
    date_columns = ['last_scraped', 'host_since', 'calendar_updated',
                    'first_review', 'last_review', 'calendar_last_scraped']
    for col in date_columns:
        if col in df.columns:
            logger.info(f"📅 Convirtiendo fecha: {col}")
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 3. Convertir booleanos
    boolean_columns = ['host_is_superhost', 'host_has_profile_pic',
                       'host_identity_verified', 'has_availability', 'instant_bookable']
    for col in boolean_columns:
        if col in df.columns:
            logger.info(f"✓ Convirtiendo booleano: {col}")
            df[col] = df[col].map({'t': True, 'f': False})

    # 4. Convertir porcentajes a float
    percentage_columns = ['host_response_rate', 'host_acceptance_rate']
    for col in percentage_columns:
        if col in df.columns:
            logger.info(f"% Convirtiendo porcentaje: {col}")
            df[col] = df[col].replace('%', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce') / 100

    # 5. Rellenar valores nulos comunes
    if 'reviews_per_month' in df.columns:
        df['reviews_per_month'] = df['reviews_per_month'].fillna(0)

    if 'name' in df.columns:
        df['name'] = df['name'].fillna('Sin nombre')

    if 'host_name' in df.columns:
        df['host_name'] = df['host_name'].fillna('Sin nombre')

    # 6. Crear campo de ubicación geoespacial (GeoJSON)
    if 'latitude' in df.columns and 'longitude' in df.columns:
        logger.info("🗺️ Creando campo geoespacial 'location'...")
        df['location'] = df.apply(
            lambda row: {
                "type": "Point",
                "coordinates": [float(row['longitude']), float(row['latitude'])]
            } if pd.notna(row['latitude']) and pd.notna(row['longitude']) else None,
            axis=1
        )
        # Filtrar registros sin coordenadas válidas
        original_count = len(df)
        df = df[df['location'].notna()]
        removed = original_count - len(df)
        if removed > 0:
            logger.warning(
                f"⚠️ Removidos {removed} registros sin coordenadas válidas")

    # 7. CRÍTICO: Convertir NaT/NaN a None para MongoDB
    logger.info("🔧 Convirtiendo valores NaT/NaN a None para MongoDB...")

    # Convertir fechas NaT a None
    date_columns = ['last_scraped', 'host_since', 'calendar_updated',
                    'first_review', 'last_review', 'calendar_last_scraped']
    for col in date_columns:
        if col in df.columns:
            # Reemplazar NaT con None
            df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

    # Convertir NaN numéricos a None
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        df[col] = df[col].apply(lambda x: None if pd.isna(x) else x)

    logger.info(
        f"✅ Datos limpios: {len(df)} registros, {len(df.columns)} columnas")

    return df


def import_custom_data(
    csv_path: Path,
    collection_name: str = "listings",
    sample_size: int = 0,
    batch_size: int = 1000,
    keep_all_columns: bool = False,
    clear_existing: bool = True
) -> None:
    """
    Importa TU dataset personalizado de Airbnb a MongoDB

    Args:
        csv_path: Ruta del archivo CSV
        collection_name: Nombre de la colección en MongoDB
        sample_size: Número de registros a importar (0 = todos)
        batch_size: Tamaño del lote para inserción
        keep_all_columns: Si True, mantiene todas las columnas del CSV
        clear_existing: Si True, elimina datos existentes antes de importar
    """
    try:
        logger.info(f"📖 Leyendo archivo: {csv_path}")

        # Leer CSV
        df = pd.read_csv(csv_path, low_memory=False)
        logger.info(f"✅ Archivo cargado: {len(df):,} registros")

        # Analizar columnas
        info = analyze_columns(df)
        logger.info(f"\n📊 ANÁLISIS DEL DATASET:")
        logger.info(f"  - Total de filas: {info['total_rows']:,}")
        logger.info(f"  - Total de columnas: {info['total_columns']}")
        logger.info(
            f"  - Tiene coordenadas: {'✅ Sí' if info['has_location'] else '❌ No'}")
        logger.info(
            f"  - Tiene precios: {'✅ Sí' if info['has_price'] else '❌ No'}")
        logger.info(
            f"  - Tiene reviews: {'✅ Sí' if info['has_reviews'] else '❌ No'}")

        # Mostrar primeras columnas
        logger.info(f"\n📋 Primeras 10 columnas: {info['columns'][:10]}")

        # Aplicar sample si se especifica
        if sample_size > 0:
            df = df.sample(n=min(sample_size, len(df)), random_state=42)
            logger.info(f"📊 Usando muestra de {len(df):,} registros")

        # Limpiar datos
        df = clean_custom_dataframe(df, keep_all_columns=keep_all_columns)

        # Conectar a MongoDB
        logger.info("🔌 Conectando a MongoDB...")
        conn = MongoDBConnection()
        crud = AirbnbCRUD(collection_name=collection_name)

        # Verificar si la colección ya tiene datos
        existing_count = crud.get_total_listings()
        if existing_count > 0:
            logger.warning(
                f"⚠️ La colección '{collection_name}' ya tiene {existing_count:,} documentos")
            if clear_existing:
                logger.info("🗑️ Eliminando datos existentes...")
                crud.collection.delete_many({})
                logger.info("✅ Datos existentes eliminados")
            else:
                logger.info("⏭️ Agregando datos sin eliminar existentes")

        # Convertir a documentos
        documents = df.to_dict('records')

        # Importar en lotes
        logger.info(f"📥 Importando {len(documents):,} documentos...")

        total_inserted = 0
        for i in tqdm(range(0, len(documents), batch_size), desc="Importando"):
            batch = documents[i:i+batch_size]

            # Agregar metadata
            for doc in batch:
                doc['imported_at'] = datetime.now()
                doc['source'] = 'custom_import'

            result = crud.create_many_listings(batch)
            total_inserted += len(result.inserted_ids)

        logger.info(f"✅ Importación completada: {total_inserted:,} documentos")

        # Crear índices
        logger.info("📑 Creando índices...")
        conn.create_indexes(collection_name)

        # Mostrar estadísticas
        stats = conn.get_collection_stats(collection_name)
        logger.info(f"\n📊 ESTADÍSTICAS DE LA COLECCIÓN '{collection_name}':")
        logger.info(f"  - Documentos: {stats['count']:,}")
        logger.info(f"  - Tamaño: {stats['size'] / 1024 / 1024:.2f} MB")
        logger.info(f"  - Índices: {stats['indexes']}")

        # Estadísticas de datos
        if 'price' in df.columns:
            logger.info(f"\n💰 ESTADÍSTICAS DE PRECIOS:")
            price_stats = df['price'].describe()
            logger.info(f"  - Promedio: {price_stats['mean']:.2f}€")
            logger.info(f"  - Mediana: {price_stats['50%']:.2f}€")
            logger.info(f"  - Mínimo: {price_stats['min']:.2f}€")
            logger.info(f"  - Máximo: {price_stats['max']:.2f}€")

        if 'neighbourhood' in df.columns or 'neighbourhood_cleansed' in df.columns:
            col = 'neighbourhood_cleansed' if 'neighbourhood_cleansed' in df.columns else 'neighbourhood'
            logger.info(f"\n🏘️ BARRIOS:")
            logger.info(f"  - Barrios únicos: {df[col].nunique()}")

        if 'room_type' in df.columns:
            logger.info(f"\n🏠 TIPOS DE ALOJAMIENTO:")
            logger.info(f"  - Tipos únicos: {df['room_type'].nunique()}")
            logger.info(f"  - Distribución:")
            for room_type, count in df['room_type'].value_counts().head(5).items():
                logger.info(
                    f"    • {room_type}: {count:,} ({count/len(df)*100:.1f}%)")

        logger.info(f"\n🎉 ¡IMPORTACIÓN EXITOSA!")
        logger.info(f"📝 Colección: {collection_name}")
        logger.info(f"📊 Total documentos: {total_inserted:,}")
        logger.info(f"📁 Columnas: {len(df.columns)}")

    except FileNotFoundError:
        logger.error(f"❌ Archivo no encontrado: {csv_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error durante la importación: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Función principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Importar tu propio dataset de Airbnb a MongoDB'
    )
    parser.add_argument(
        'csv_file',
        help='Ruta al archivo CSV de Airbnb'
    )
    parser.add_argument(
        '--collection',
        default='listings',
        help='Nombre de la colección (default: listings)'
    )
    parser.add_argument(
        '--sample',
        type=int,
        default=0,
        help='Número de registros a importar (0 = todos)'
    )
    parser.add_argument(
        '--keep-all',
        action='store_true',
        help='Mantener TODAS las columnas del CSV'
    )
    parser.add_argument(
        '--no-clear',
        action='store_true',
        help='NO eliminar datos existentes antes de importar'
    )

    args = parser.parse_args()

    print("\n" + "="*70)
    print("📥 IMPORTACIÓN DE DATASET PERSONALIZADO DE AIRBNB")
    print("="*70 + "\n")

    csv_path = Path(args.csv_file)

    if not csv_path.exists():
        logger.error(f"❌ El archivo no existe: {csv_path}")
        sys.exit(1)

    # Importar datos
    import_custom_data(
        csv_path=csv_path,
        collection_name=args.collection,
        sample_size=args.sample,
        keep_all_columns=args.keep_all,
        clear_existing=not args.no_clear
    )

    print("\n" + "="*70)
    print("🎉 ¡IMPORTACIÓN COMPLETADA!")
    print("="*70)
    print(f"\n💡 Siguiente paso: jupyter notebook notebooks/01_crud_operations.ipynb\n")


if __name__ == "__main__":
    main()
