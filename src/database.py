"""
Módulo de conexión y gestión de MongoDB
"""

import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from .config import MONGODB_URI, MONGODB_DB, COLLECTION_NAME

# Configurar logging
logger = logging.getLogger(__name__)


class MongoDBConnection:
    """
    Clase para gestionar la conexión a MongoDB
    Implementa el patrón Singleton para reutilizar la conexión
    """
    
    _instance: Optional['MongoDBConnection'] = None
    _client: Optional[MongoClient] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa la conexión a MongoDB si no existe"""
        if self._client is None:
            self.connect()
    
    def connect(self, uri: Optional[str] = None, db_name: Optional[str] = None) -> None:
        """
        Establece conexión con MongoDB
        
        Args:
            uri: URI de conexión (opcional, usa config por defecto)
            db_name: Nombre de la base de datos (opcional, usa config por defecto)
        """
        try:
            connection_uri = uri or MONGODB_URI
            self.db_name = db_name or MONGODB_DB
            
            logger.info(f"Conectando a MongoDB: {self.db_name}")
            
            # Crear cliente con timeout
            self._client = MongoClient(
                connection_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000
            )
            
            # Verificar conexión
            self._client.admin.command('ping')
            logger.info("✅ Conexión a MongoDB establecida exitosamente")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ Error al conectar con MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}")
            raise
    
    def get_database(self, db_name: Optional[str] = None) -> Database:
        """
        Retorna la instancia de la base de datos
        
        Args:
            db_name: Nombre de la base de datos (opcional)
            
        Returns:
            Database: Instancia de la base de datos MongoDB
        """
        if self._client is None:
            self.connect()
        
        database_name = db_name or self.db_name
        return self._client[database_name]
    
    def get_collection(
        self, 
        collection_name: str = COLLECTION_NAME,
        db_name: Optional[str] = None
    ) -> Collection:
        """
        Retorna una colección específica
        
        Args:
            collection_name: Nombre de la colección
            db_name: Nombre de la base de datos (opcional)
            
        Returns:
            Collection: Instancia de la colección MongoDB
        """
        db = self.get_database(db_name)
        return db[collection_name]
    
    def list_collections(self, db_name: Optional[str] = None) -> list:
        """
        Lista todas las colecciones en la base de datos
        
        Args:
            db_name: Nombre de la base de datos (opcional)
            
        Returns:
            list: Lista de nombres de colecciones
        """
        db = self.get_database(db_name)
        return db.list_collection_names()
    
    def create_indexes(self, collection_name: str = COLLECTION_NAME) -> None:
        """
        Crea índices optimizados para las consultas más comunes
        
        Args:
            collection_name: Nombre de la colección
        """
        collection = self.get_collection(collection_name)
        
        logger.info(f"Creando índices para {collection_name}...")
        
        # Índice simple para precio
        collection.create_index("price")
        logger.info("✅ Índice creado: price")
        
        # Índice simple para barrio
        collection.create_index("neighbourhood")
        logger.info("✅ Índice creado: neighbourhood")
        
        # Índice simple para tipo de habitación
        collection.create_index("room_type")
        logger.info("✅ Índice creado: room_type")
        
        # Índice compuesto para consultas por barrio y precio
        collection.create_index([("neighbourhood", 1), ("price", 1)])
        logger.info("✅ Índice compuesto creado: neighbourhood + price")
        
        # Índice geoespacial (si existen coordenadas)
        try:
            collection.create_index([("location", "2dsphere")])
            logger.info("✅ Índice geoespacial creado: location")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo crear índice geoespacial: {e}")
        
        # Índice de texto para búsqueda en nombre y descripción
        try:
            collection.create_index([
                ("name", "text"),
                ("description", "text")
            ])
            logger.info("✅ Índice de texto creado: name + description")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo crear índice de texto: {e}")
    
    def get_collection_stats(self, collection_name: str = COLLECTION_NAME) -> dict:
        """
        Obtiene estadísticas de la colección
        
        Args:
            collection_name: Nombre de la colección
            
        Returns:
            dict: Estadísticas de la colección
        """
        db = self.get_database()
        stats = db.command("collStats", collection_name)
        
        return {
            "count": stats.get("count", 0),
            "size": stats.get("size", 0),
            "avgObjSize": stats.get("avgObjSize", 0),
            "storageSize": stats.get("storageSize", 0),
            "indexes": stats.get("nindexes", 0),
            "indexSize": stats.get("totalIndexSize", 0)
        }
    
    def ping(self) -> bool:
        """
        Verifica si la conexión está activa
        
        Returns:
            bool: True si la conexión está activa
        """
        try:
            self._client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"Error en ping: {e}")
            return False
    
    def close(self) -> None:
        """Cierra la conexión a MongoDB"""
        if self._client is not None:
            self._client.close()
            self._client = None
            logger.info("Conexión a MongoDB cerrada")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Función helper para obtener una conexión rápidamente
def get_connection() -> MongoDBConnection:
    """
    Retorna una instancia de MongoDBConnection
    
    Returns:
        MongoDBConnection: Instancia de conexión
    """
    return MongoDBConnection()


# Función helper para obtener una colección directamente
def get_collection(collection_name: str = COLLECTION_NAME) -> Collection:
    """
    Retorna una colección directamente
    
    Args:
        collection_name: Nombre de la colección
        
    Returns:
        Collection: Instancia de la colección
    """
    conn = get_connection()
    return conn.get_collection(collection_name)


if __name__ == "__main__":
    # Test de conexión
    logging.basicConfig(level=logging.INFO)
    
    try:
        with MongoDBConnection() as conn:
            print("\n🔍 Probando conexión a MongoDB...")
            
            if conn.ping():
                print("✅ Conexión exitosa!")
                
                # Listar colecciones
                collections = conn.list_collections()
                print(f"\n📚 Colecciones disponibles: {collections}")
                
                # Estadísticas si existe la colección
                if COLLECTION_NAME in collections:
                    stats = conn.get_collection_stats()
                    print(f"\n📊 Estadísticas de {COLLECTION_NAME}:")
                    print(f"  - Documentos: {stats['count']:,}")
                    print(f"  - Tamaño: {stats['size'] / 1024 / 1024:.2f} MB")
                    print(f"  - Índices: {stats['indexes']}")
            else:
                print("❌ No se pudo conectar a MongoDB")
                
    except Exception as e:
        print(f"❌ Error: {e}")
