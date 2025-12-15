"""
Airbnb Madrid MongoDB Analysis Package
"""

from .config import *
from .database import MongoDBConnection, get_connection, get_collection
from .crud_operations import AirbnbCRUD
from .visualizations import AirbnbVisualizer

__version__ = "1.0.0"
__author__ = "GCP - Tax & Data Science Consultant"

__all__ = [
    "MongoDBConnection",
    "get_connection",
    "get_collection",
    "AirbnbCRUD",
    "AirbnbVisualizer"
]
