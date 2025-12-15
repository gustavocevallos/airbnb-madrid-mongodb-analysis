#!/bin/bash
set -e

echo "🚀 Iniciando Airbnb Madrid MongoDB Analysis..."

# Esperar a que MongoDB esté listo
echo "⏳ Esperando a MongoDB..."
until mongosh --host mongodb --eval "print('MongoDB está listo')" > /dev/null 2>&1; do
    sleep 2
done
echo "✅ MongoDB conectado"

# Verificar si hay datos en la base de datos
echo "🔍 Verificando datos..."
DOCS_COUNT=$(python -c "
from src.database import MongoDBConnection
try:
    conn = MongoDBConnection()
    collection = conn.get_collection()
    count = collection.count_documents({})
    print(count)
except Exception as e:
    print('0')
" 2>/dev/null || echo "0")

echo "📊 Documentos en la base de datos: $DOCS_COUNT"

# Si no hay datos, ofrecer importar datos de ejemplo
if [ "$DOCS_COUNT" = "0" ]; then
    echo ""
    echo "⚠️  No hay datos en la base de datos"
    echo "💡 Puedes importar datos de ejemplo con:"
    echo "   docker-compose exec app python scripts/import_sample_data.py"
    echo ""
fi

# Ejecutar comando
case "$1" in
    jupyter)
        echo "📓 Iniciando Jupyter Notebook..."
        exec jupyter notebook \
            --ip=0.0.0.0 \
            --port=8888 \
            --no-browser \
            --allow-root \
            --NotebookApp.token='' \
            --NotebookApp.password=''
        ;;
    bash)
        echo "💻 Iniciando bash..."
        exec /bin/bash
        ;;
    python)
        shift
        echo "🐍 Ejecutando Python..."
        exec python "$@"
        ;;
    *)
        exec "$@"
        ;;
esac
