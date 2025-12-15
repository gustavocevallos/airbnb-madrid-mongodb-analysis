#!/usr/bin/env python3
"""
Script para descargar el dataset de Airbnb Madrid desde Inside Airbnb
"""

import os
import sys
import logging
import requests
from pathlib import Path
from tqdm import tqdm

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import RAW_DATA_DIR, AIRBNB_DATA_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def download_file(url: str, destination: Path, chunk_size: int = 8192) -> bool:
    """
    Descarga un archivo con barra de progreso
    
    Args:
        url: URL del archivo
        destination: Ruta de destino
        chunk_size: Tamaño de chunk para descarga
        
    Returns:
        bool: True si se descargó exitosamente
    """
    try:
        logger.info(f"Descargando desde: {url}")
        logger.info(f"Destino: {destination}")
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(destination, 'wb') as file, tqdm(
            desc=destination.name,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                size = file.write(chunk)
                progress_bar.update(size)
        
        logger.info(f"✅ Archivo descargado: {destination}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error al descargar archivo: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}")
        return False


def decompress_gzip(gzip_file: Path) -> Path:
    """
    Descomprime un archivo .gz
    
    Args:
        gzip_file: Ruta del archivo .gz
        
    Returns:
        Path: Ruta del archivo descomprimido
    """
    import gzip
    import shutil
    
    output_file = gzip_file.with_suffix('')
    
    try:
        logger.info(f"Descomprimiendo: {gzip_file.name}")
        
        with gzip.open(gzip_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        logger.info(f"✅ Archivo descomprimido: {output_file}")
        
        # Eliminar archivo .gz
        gzip_file.unlink()
        logger.info(f"🗑️ Archivo .gz eliminado")
        
        return output_file
        
    except Exception as e:
        logger.error(f"❌ Error al descomprimir: {e}")
        raise


def main():
    """Función principal"""
    
    print("\n" + "="*60)
    print("📥 DESCARGA DE DATASET DE AIRBNB MADRID")
    print("="*60 + "\n")
    
    # Crear directorio si no existe
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Archivo de destino
    filename = "madrid_listings.csv.gz"
    destination = RAW_DATA_DIR / filename
    
    # Verificar si ya existe
    csv_file = RAW_DATA_DIR / "madrid_listings.csv"
    if csv_file.exists():
        logger.warning(f"⚠️ El archivo ya existe: {csv_file}")
        response = input("¿Deseas descargarlo nuevamente? (s/n): ")
        if response.lower() != 's':
            logger.info("Descarga cancelada")
            return
        csv_file.unlink()
    
    # Descargar archivo
    success = download_file(AIRBNB_DATA_URL, destination)
    
    if not success:
        logger.error("❌ No se pudo descargar el dataset")
        sys.exit(1)
    
    # Descomprimir
    logger.info("\n📦 Descomprimiendo archivo...")
    csv_file = decompress_gzip(destination)
    
    # Verificar archivo
    file_size_mb = csv_file.stat().st_size / (1024 * 1024)
    logger.info(f"\n✅ Dataset descargado exitosamente!")
    logger.info(f"📄 Archivo: {csv_file.name}")
    logger.info(f"📊 Tamaño: {file_size_mb:.2f} MB")
    
    print("\n" + "="*60)
    print("🎉 ¡DESCARGA COMPLETADA!")
    print("="*60)
    print(f"\n📍 Ubicación: {csv_file}")
    print("\n💡 Siguiente paso: Ejecuta 'python scripts/import_data.py' para importar a MongoDB\n")


if __name__ == "__main__":
    main()
