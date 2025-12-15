"""
Operaciones CRUD para la colección de Airbnb Madrid
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult
from bson import ObjectId

from .database import get_collection
from .config import COLLECTION_NAME

logger = logging.getLogger(__name__)


class AirbnbCRUD:
    """
    Clase para realizar operaciones CRUD en la colección de Airbnb
    """
    
    def __init__(self, collection_name: str = COLLECTION_NAME):
        """
        Inicializa la clase con la colección especificada
        
        Args:
            collection_name: Nombre de la colección
        """
        self.collection: Collection = get_collection(collection_name)
        self.collection_name = collection_name
        logger.info(f"CRUD operations initialized for collection: {collection_name}")
    
    # ===== CREATE OPERATIONS =====
    
    def create_listing(self, listing_data: Dict[str, Any]) -> InsertOneResult:
        """
        Crea un nuevo listing en la base de datos
        
        Args:
            listing_data: Diccionario con los datos del listing
            
        Returns:
            InsertOneResult: Resultado de la inserción
        """
        try:
            # Agregar timestamp de creación
            listing_data['created_at'] = datetime.now()
            listing_data['updated_at'] = datetime.now()
            
            result = self.collection.insert_one(listing_data)
            logger.info(f"✅ Listing creado con ID: {result.inserted_id}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al crear listing: {e}")
            raise
    
    def create_many_listings(self, listings_data: List[Dict[str, Any]]) -> InsertManyResult:
        """
        Crea múltiples listings en la base de datos
        
        Args:
            listings_data: Lista de diccionarios con datos de listings
            
        Returns:
            InsertManyResult: Resultado de la inserción múltiple
        """
        try:
            # Agregar timestamps a todos los documentos
            now = datetime.now()
            for listing in listings_data:
                listing['created_at'] = now
                listing['updated_at'] = now
            
            result = self.collection.insert_many(listings_data)
            logger.info(f"✅ {len(result.inserted_ids)} listings creados")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al crear listings: {e}")
            raise
    
    # ===== READ OPERATIONS =====
    
    def find_listing_by_id(self, listing_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca un listing por su ID
        
        Args:
            listing_id: ID del listing (puede ser ObjectId o string)
            
        Returns:
            Dict o None: Documento encontrado o None
        """
        try:
            # Convertir a ObjectId si es string
            if isinstance(listing_id, str):
                listing_id = ObjectId(listing_id)
            
            result = self.collection.find_one({"_id": listing_id})
            
            if result:
                logger.info(f"✅ Listing encontrado: {listing_id}")
            else:
                logger.warning(f"⚠️ Listing no encontrado: {listing_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al buscar listing: {e}")
            raise
    
    def find_listings(
        self,
        filter_query: Dict[str, Any] = {},
        projection: Optional[Dict[str, int]] = None,
        limit: int = 0,
        sort: Optional[List[tuple]] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca listings según filtros
        
        Args:
            filter_query: Query de filtrado MongoDB
            projection: Campos a incluir/excluir
            limit: Número máximo de resultados (0 = sin límite)
            sort: Lista de tuplas (field, direction) para ordenamiento
            
        Returns:
            List[Dict]: Lista de documentos encontrados
        """
        try:
            cursor = self.collection.find(filter_query, projection)
            
            if sort:
                cursor = cursor.sort(sort)
            
            if limit > 0:
                cursor = cursor.limit(limit)
            
            results = list(cursor)
            logger.info(f"✅ {len(results)} listings encontrados")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error al buscar listings: {e}")
            raise
    
    def find_by_neighbourhood(
        self,
        neighbourhood: str,
        limit: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Busca listings por barrio
        
        Args:
            neighbourhood: Nombre del barrio
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Listings del barrio
        """
        query = {"neighbourhood": neighbourhood}
        return self.find_listings(query, limit=limit)
    
    def find_by_price_range(
        self,
        min_price: float,
        max_price: float,
        limit: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Busca listings en un rango de precios
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Listings en el rango de precio
        """
        query = {
            "price": {
                "$gte": min_price,
                "$lte": max_price
            }
        }
        return self.find_listings(query, limit=limit, sort=[("price", 1)])
    
    def find_by_room_type(
        self,
        room_type: str,
        limit: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Busca listings por tipo de habitación
        
        Args:
            room_type: Tipo de habitación
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Listings del tipo especificado
        """
        query = {"room_type": room_type}
        return self.find_listings(query, limit=limit)
    
    def search_by_name(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Busca listings por nombre usando regex
        
        Args:
            search_term: Término de búsqueda
            limit: Número máximo de resultados
            
        Returns:
            List[Dict]: Listings que coinciden con la búsqueda
        """
        query = {
            "name": {
                "$regex": search_term,
                "$options": "i"  # Case insensitive
            }
        }
        return self.find_listings(query, limit=limit)
    
    # ===== UPDATE OPERATIONS =====
    
    def update_listing(
        self,
        listing_id: str,
        update_data: Dict[str, Any]
    ) -> UpdateResult:
        """
        Actualiza un listing por su ID
        
        Args:
            listing_id: ID del listing
            update_data: Datos a actualizar
            
        Returns:
            UpdateResult: Resultado de la actualización
        """
        try:
            # Convertir a ObjectId si es string
            if isinstance(listing_id, str):
                listing_id = ObjectId(listing_id)
            
            # Agregar timestamp de actualización
            update_data['updated_at'] = datetime.now()
            
            result = self.collection.update_one(
                {"_id": listing_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"✅ Listing actualizado: {listing_id}")
            else:
                logger.warning(f"⚠️ No se modificó ningún documento")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al actualizar listing: {e}")
            raise
    
    def update_many_listings(
        self,
        filter_query: Dict[str, Any],
        update_data: Dict[str, Any]
    ) -> UpdateResult:
        """
        Actualiza múltiples listings que coincidan con el filtro
        
        Args:
            filter_query: Query de filtrado
            update_data: Datos a actualizar
            
        Returns:
            UpdateResult: Resultado de la actualización
        """
        try:
            update_data['updated_at'] = datetime.now()
            
            result = self.collection.update_many(
                filter_query,
                {"$set": update_data}
            )
            
            logger.info(f"✅ {result.modified_count} listings actualizados")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al actualizar listings: {e}")
            raise
    
    def increment_field(
        self,
        listing_id: str,
        field: str,
        increment: int = 1
    ) -> UpdateResult:
        """
        Incrementa un campo numérico de un listing
        
        Args:
            listing_id: ID del listing
            field: Nombre del campo a incrementar
            increment: Valor a incrementar (puede ser negativo)
            
        Returns:
            UpdateResult: Resultado de la actualización
        """
        try:
            if isinstance(listing_id, str):
                listing_id = ObjectId(listing_id)
            
            result = self.collection.update_one(
                {"_id": listing_id},
                {"$inc": {field: increment}}
            )
            
            logger.info(f"✅ Campo {field} incrementado en {increment}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al incrementar campo: {e}")
            raise
    
    # ===== DELETE OPERATIONS =====
    
    def delete_listing(self, listing_id: str) -> DeleteResult:
        """
        Elimina un listing por su ID
        
        Args:
            listing_id: ID del listing a eliminar
            
        Returns:
            DeleteResult: Resultado de la eliminación
        """
        try:
            if isinstance(listing_id, str):
                listing_id = ObjectId(listing_id)
            
            result = self.collection.delete_one({"_id": listing_id})
            
            if result.deleted_count > 0:
                logger.info(f"✅ Listing eliminado: {listing_id}")
            else:
                logger.warning(f"⚠️ Listing no encontrado: {listing_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al eliminar listing: {e}")
            raise
    
    def delete_many_listings(self, filter_query: Dict[str, Any]) -> DeleteResult:
        """
        Elimina múltiples listings que coincidan con el filtro
        
        Args:
            filter_query: Query de filtrado
            
        Returns:
            DeleteResult: Resultado de la eliminación
        """
        try:
            result = self.collection.delete_many(filter_query)
            logger.info(f"✅ {result.deleted_count} listings eliminados")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error al eliminar listings: {e}")
            raise
    
    def delete_unavailable_listings(self) -> DeleteResult:
        """
        Elimina listings que no tienen disponibilidad
        
        Returns:
            DeleteResult: Resultado de la eliminación
        """
        query = {"availability_365": 0}
        return self.delete_many_listings(query)
    
    # ===== AGGREGATION OPERATIONS =====
    
    def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ejecuta un pipeline de agregación
        
        Args:
            pipeline: Pipeline de agregación MongoDB
            
        Returns:
            List[Dict]: Resultados de la agregación
        """
        try:
            results = list(self.collection.aggregate(pipeline))
            logger.info(f"✅ Agregación completada: {len(results)} resultados")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error en agregación: {e}")
            raise
    
    def get_price_stats_by_neighbourhood(self) -> List[Dict[str, Any]]:
        """
        Obtiene estadísticas de precios por barrio
        
        Returns:
            List[Dict]: Estadísticas por barrio
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$neighbourhood",
                    "avg_price": {"$avg": "$price"},
                    "min_price": {"$min": "$price"},
                    "max_price": {"$max": "$price"},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"avg_price": -1}}
        ]
        return self.aggregate(pipeline)
    
    def get_listings_count_by_room_type(self) -> List[Dict[str, Any]]:
        """
        Cuenta listings por tipo de habitación
        
        Returns:
            List[Dict]: Conteo por tipo
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$room_type",
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"count": -1}}
        ]
        return self.aggregate(pipeline)
    
    # ===== UTILITY METHODS =====
    
    def count_documents(self, filter_query: Dict[str, Any] = {}) -> int:
        """
        Cuenta documentos que coinciden con el filtro
        
        Args:
            filter_query: Query de filtrado
            
        Returns:
            int: Número de documentos
        """
        return self.collection.count_documents(filter_query)
    
    def get_total_listings(self) -> int:
        """
        Obtiene el total de listings en la colección
        
        Returns:
            int: Total de listings
        """
        return self.count_documents()
    
    def get_distinct_values(self, field: str) -> List[Any]:
        """
        Obtiene valores únicos de un campo
        
        Args:
            field: Nombre del campo
            
        Returns:
            List: Valores únicos
        """
        return self.collection.distinct(field)


if __name__ == "__main__":
    # Test de operaciones CRUD
    logging.basicConfig(level=logging.INFO)
    
    crud = AirbnbCRUD()
    
    print(f"\n📊 Total de listings: {crud.get_total_listings():,}")
    print(f"\n🏘️ Barrios únicos: {len(crud.get_distinct_values('neighbourhood'))}")
    print(f"\n🏠 Tipos de habitación: {crud.get_distinct_values('room_type')}")
