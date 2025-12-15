#!/usr/bin/env python3
import os
import sys
import logging
import pandas as pd
import math
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def clean_document(doc):
    """Limpia un documento de valores NaT/NaN"""
    cleaned = {}
    for key, value in doc.items():
        # Chequear NaT, NaN, inf
        if pd.isna(value):
            cleaned[key] = None
        elif isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            cleaned[key] = None
        elif hasattr(value, '__class__') and 'NaTType' in str(value.__class__):
            cleaned[key] = None
        else:
            cleaned[key] = value
    return cleaned


def main():
    logger.info("📖 Leyendo CSV...")
    df = pd.read_csv('data/raw/listings.csv', low_memory=False)
    logger.info(f"✅ {len(df):,} registros cargados")

    # Limpiar precios
    logger.info("💰 Limpiando precios...")
    df['price'] = df['price'].replace(r'[\$,]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

    # Convertir fechas
    logger.info("📅 Convirtiendo fechas...")
    date_cols = ['last_scraped', 'host_since', 'first_review', 'last_review',
                 'calendar_updated', 'calendar_last_scraped']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            df[col] = df[col].where(pd.notna(df[col]), None)

    # Crear location
    logger.info("🗺️ Creando campo geoespacial...")
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['location'] = df.apply(
            lambda row: {
                'type': 'Point',
                'coordinates': [float(row['longitude']), float(row['latitude'])]
            } if pd.notna(row['latitude']) and pd.notna(row['longitude']) else None,
            axis=1
        )
        df = df[df['location'].notna()]

    logger.info(f"✅ Datos preparados: {len(df):,} registros")

    # Convertir a documentos y limpiar
    logger.info("📄 Convirtiendo a documentos...")
    documents = df.to_dict('records')

    logger.info("🧹 Limpiando valores especiales...")
    cleaned_documents = [clean_document(doc)
                         for doc in tqdm(documents, desc="Limpiando")]

    # Conectar a MongoDB
    logger.info("🔌 Conectando a MongoDB...")
    client = MongoClient('mongodb://localhost:27018/')
    db = client['airbnb_madrid']
    collection = db['listings']

    # Limpiar colección existente
    existing = collection.count_documents({})
    if existing > 0:
        logger.info(f"🗑️ Eliminando {existing:,} documentos existentes...")
        collection.delete_many({})

    # Importar en lotes
    logger.info("📥 Importando a MongoDB...")
    batch_size = 1000
    for i in tqdm(range(0, len(cleaned_documents), batch_size), desc="Importando"):
        batch = cleaned_documents[i:i+batch_size]
        for doc in batch:
            doc['imported_at'] = datetime.now()
        collection.insert_many(batch)

    total = collection.count_documents({})
    logger.info(f"\n✅ ¡Importación completada: {total:,} documentos!")

    # Estadísticas
    logger.info(f"\n📊 ESTADÍSTICAS:")
    logger.info(f"  - Total documentos: {total:,}")
    logger.info(f"  - Precio promedio: {df['price'].mean():.2f}€")
    if 'neighbourhood_cleansed' in df.columns:
        logger.info(
            f"  - Barrios únicos: {df['neighbourhood_cleansed'].nunique()}")


if __name__ == "__main__":
    main()
