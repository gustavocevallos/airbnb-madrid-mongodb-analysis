"""
Módulo de visualizaciones para análisis de Airbnb Madrid
"""

import logging
from typing import List, Dict, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

from .database import get_collection
from .config import COLOR_PALETTE, PLOTLY_CONFIG, ROOM_TYPE_MAPPING, COLLECTION_NAME

logger = logging.getLogger(__name__)


class AirbnbVisualizer:
    """
    Clase para crear visualizaciones de datos de Airbnb
    """
    
    def __init__(self, collection_name: str = COLLECTION_NAME):
        """
        Inicializa el visualizador
        
        Args:
            collection_name: Nombre de la colección MongoDB
        """
        self.collection = get_collection(collection_name)
        self.colors = COLOR_PALETTE
        logger.info(f"Visualizer initialized for collection: {collection_name}")
    
    def _get_dataframe(
        self,
        query: Dict[str, Any] = {},
        fields: Optional[List[str]] = None,
        limit: int = 0
    ) -> pd.DataFrame:
        """
        Obtiene datos de MongoDB como DataFrame
        
        Args:
            query: Query de filtrado
            fields: Campos a incluir
            limit: Límite de registros
            
        Returns:
            pd.DataFrame: Datos en formato DataFrame
        """
        try:
            projection = {field: 1 for field in fields} if fields else None
            cursor = self.collection.find(query, projection)
            
            if limit > 0:
                cursor = cursor.limit(limit)
            
            df = pd.DataFrame(list(cursor))
            
            # Eliminar _id si no se solicitó explícitamente
            if fields and '_id' not in fields and '_id' in df.columns:
                df = df.drop('_id', axis=1)
            
            logger.info(f"✅ DataFrame creado con {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error al crear DataFrame: {e}")
            raise
    
    # ===== DISTRIBUCIÓN DE PRECIOS =====
    
    def price_distribution(
        self,
        bins: int = 50,
        max_price: float = 500
    ) -> go.Figure:
        """
        Crea histograma de distribución de precios
        
        Args:
            bins: Número de bins para el histograma
            max_price: Precio máximo a mostrar (filtrar outliers)
            
        Returns:
            go.Figure: Figura de Plotly
        """
        df = self._get_dataframe(
            query={"price": {"$lte": max_price}},
            fields=["price"]
        )
        
        fig = px.histogram(
            df,
            x="price",
            nbins=bins,
            title="Distribución de Precios de Airbnb en Madrid",
            labels={"price": "Precio (€/noche)", "count": "Frecuencia"},
            color_discrete_sequence=[self.colors["primary"]]
        )
        
        fig.update_layout(
            showlegend=False,
            hovermode='x unified',
            plot_bgcolor='white'
        )
        
        return fig
    
    def price_boxplot_by_room_type(self) -> go.Figure:
        """
        Crea boxplot de precios por tipo de habitación
        
        Returns:
            go.Figure: Figura de Plotly
        """
        df = self._get_dataframe(
            query={"price": {"$lte": 500}},
            fields=["price", "room_type"]
        )
        
        # Traducir tipos de habitación
        df['room_type_es'] = df['room_type'].map(ROOM_TYPE_MAPPING)
        
        fig = px.box(
            df,
            x="room_type_es",
            y="price",
            title="Distribución de Precios por Tipo de Alojamiento",
            labels={"price": "Precio (€/noche)", "room_type_es": "Tipo de Alojamiento"},
            color="room_type_es",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_layout(showlegend=False, plot_bgcolor='white')
        
        return fig
    
    # ===== ANÁLISIS POR BARRIO =====
    
    def avg_price_by_neighbourhood(self, top_n: int = 20) -> go.Figure:
        """
        Gráfico de barras de precio promedio por barrio
        
        Args:
            top_n: Número de barrios a mostrar
            
        Returns:
            go.Figure: Figura de Plotly
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$neighbourhood",
                    "avg_price": {"$avg": "$price"},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"avg_price": -1}},
            {"$limit": top_n}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        df = pd.DataFrame(results)
        df.rename(columns={"_id": "neighbourhood"}, inplace=True)
        
        fig = px.bar(
            df,
            x="avg_price",
            y="neighbourhood",
            orientation='h',
            title=f"Top {top_n} Barrios por Precio Promedio",
            labels={"avg_price": "Precio Promedio (€/noche)", "neighbourhood": "Barrio"},
            text="avg_price",
            color="avg_price",
            color_continuous_scale="Reds"
        )
        
        fig.update_traces(texttemplate='%{text:.0f}€', textposition='outside')
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    def listings_count_by_neighbourhood(self, top_n: int = 15) -> go.Figure:
        """
        Gráfico de barras de cantidad de listings por barrio
        
        Args:
            top_n: Número de barrios a mostrar
            
        Returns:
            go.Figure: Figura de Plotly
        """
        pipeline = [
            {"$group": {"_id": "$neighbourhood", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": top_n}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        df = pd.DataFrame(results)
        df.rename(columns={"_id": "neighbourhood"}, inplace=True)
        
        fig = px.bar(
            df,
            x="neighbourhood",
            y="count",
            title=f"Top {top_n} Barrios con Más Listings",
            labels={"count": "Número de Listings", "neighbourhood": "Barrio"},
            text="count",
            color="count",
            color_continuous_scale="Blues"
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            xaxis_tickangle=-45
        )
        
        return fig
    
    # ===== ANÁLISIS DE TIPOS DE HABITACIÓN =====
    
    def room_type_pie_chart(self) -> go.Figure:
        """
        Gráfico de torta de distribución por tipo de habitación
        
        Returns:
            go.Figure: Figura de Plotly
        """
        pipeline = [
            {"$group": {"_id": "$room_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        df = pd.DataFrame(results)
        df.rename(columns={"_id": "room_type"}, inplace=True)
        df['room_type_es'] = df['room_type'].map(ROOM_TYPE_MAPPING)
        
        fig = px.pie(
            df,
            values="count",
            names="room_type_es",
            title="Distribución de Tipos de Alojamiento",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        return fig
    
    # ===== ANÁLISIS DE DISPONIBILIDAD =====
    
    def availability_distribution(self) -> go.Figure:
        """
        Histograma de disponibilidad anual
        
        Returns:
            go.Figure: Figura de Plotly
        """
        df = self._get_dataframe(fields=["availability_365"])
        
        fig = px.histogram(
            df,
            x="availability_365",
            nbins=50,
            title="Distribución de Disponibilidad Anual",
            labels={"availability_365": "Días Disponibles al Año", "count": "Frecuencia"},
            color_discrete_sequence=[self.colors["secondary"]]
        )
        
        fig.update_layout(showlegend=False, plot_bgcolor='white')
        
        return fig
    
    # ===== ANÁLISIS DE REVIEWS =====
    
    def reviews_vs_price_scatter(self, sample_size: int = 1000) -> go.Figure:
        """
        Scatter plot de reviews vs precio
        
        Args:
            sample_size: Número de puntos a mostrar
            
        Returns:
            go.Figure: Figura de Plotly
        """
        pipeline = [
            {"$match": {"number_of_reviews": {"$gt": 0}, "price": {"$lte": 500}}},
            {"$sample": {"size": sample_size}},
            {"$project": {"price": 1, "number_of_reviews": 1, "room_type": 1}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        df = pd.DataFrame(results)
        
        fig = px.scatter(
            df,
            x="number_of_reviews",
            y="price",
            color="room_type",
            title="Relación entre Número de Reviews y Precio",
            labels={
                "number_of_reviews": "Número de Reviews",
                "price": "Precio (€/noche)",
                "room_type": "Tipo de Alojamiento"
            },
            opacity=0.6,
            trendline="lowess"
        )
        
        fig.update_layout(plot_bgcolor='white')
        
        return fig
    
    # ===== MAPA GEOESPACIAL =====
    
    def create_map(
        self,
        max_price: float = 500,
        sample_size: int = 2000
    ) -> go.Figure:
        """
        Crea mapa interactivo de listings
        
        Args:
            max_price: Precio máximo a mostrar
            sample_size: Número de puntos a mostrar
            
        Returns:
            go.Figure: Figura de Plotly
        """
        pipeline = [
            {
                "$match": {
                    "latitude": {"$exists": True},
                    "longitude": {"$exists": True},
                    "price": {"$lte": max_price}
                }
            },
            {"$sample": {"size": sample_size}},
            {
                "$project": {
                    "name": 1,
                    "latitude": 1,
                    "longitude": 1,
                    "price": 1,
                    "room_type": 1,
                    "neighbourhood": 1
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        df = pd.DataFrame(results)
        
        fig = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            color="price",
            size="price",
            hover_name="name",
            hover_data={"neighbourhood": True, "room_type": True, "price": True},
            color_continuous_scale="Viridis",
            size_max=15,
            zoom=11,
            title="Mapa de Listings de Airbnb en Madrid"
        )
        
        fig.update_layout(
            mapbox_style="open-street-map",
            height=700
        )
        
        return fig
    
    # ===== DASHBOARD COMPLETO =====
    
    def create_dashboard(self) -> go.Figure:
        """
        Crea dashboard con múltiples subplots
        
        Returns:
            go.Figure: Dashboard completo
        """
        from plotly.subplots import make_subplots
        
        # Obtener datos
        df = self._get_dataframe(
            query={"price": {"$lte": 500}},
            fields=["price", "room_type", "neighbourhood", "availability_365"]
        )
        
        # Crear figura con subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Distribución de Precios",
                "Tipos de Alojamiento",
                "Disponibilidad Anual",
                "Top 10 Barrios por Precio"
            ),
            specs=[
                [{"type": "histogram"}, {"type": "pie"}],
                [{"type": "histogram"}, {"type": "bar"}]
            ]
        )
        
        # 1. Histograma de precios
        fig.add_trace(
            go.Histogram(x=df['price'], nbinsx=50, name="Precio"),
            row=1, col=1
        )
        
        # 2. Pie chart de room types
        room_counts = df['room_type'].value_counts()
        fig.add_trace(
            go.Pie(labels=room_counts.index, values=room_counts.values, name="Tipo"),
            row=1, col=2
        )
        
        # 3. Histograma de disponibilidad
        fig.add_trace(
            go.Histogram(x=df['availability_365'], nbinsx=50, name="Disponibilidad"),
            row=2, col=1
        )
        
        # 4. Top barrios
        top_neighbourhoods = df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).head(10)
        fig.add_trace(
            go.Bar(x=top_neighbourhoods.values, y=top_neighbourhoods.index, orientation='h'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=False,
            title_text="Dashboard de Airbnb Madrid"
        )
        
        return fig
    
    # ===== VISUALIZACIONES CON MATPLOTLIB/SEABORN =====
    
    def create_correlation_heatmap(self) -> plt.Figure:
        """
        Crea heatmap de correlación usando Seaborn
        
        Returns:
            plt.Figure: Figura de Matplotlib
        """
        df = self._get_dataframe(
            fields=[
                "price",
                "minimum_nights",
                "number_of_reviews",
                "availability_365",
                "reviews_per_month"
            ]
        )
        
        # Eliminar valores nulos
        df = df.dropna()
        
        # Calcular correlación
        corr = df.corr()
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(
            corr,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            ax=ax
        )
        
        ax.set_title('Matriz de Correlación de Variables Numéricas', fontsize=14, pad=20)
        plt.tight_layout()
        
        return fig


if __name__ == "__main__":
    # Test de visualizaciones
    logging.basicConfig(level=logging.INFO)
    
    viz = AirbnbVisualizer()
    
    print("🎨 Generando visualizaciones de prueba...")
    
    # Generar gráfico de precios
    fig = viz.price_distribution()
    print("✅ Distribución de precios creada")
    
    # Generar pie chart
    fig = viz.room_type_pie_chart()
    print("✅ Pie chart de tipos de habitación creado")
