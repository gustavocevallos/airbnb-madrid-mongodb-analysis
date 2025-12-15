# Makefile para Airbnb Madrid MongoDB Analysis
# Simplifica comandos Docker comunes

.PHONY: help up down restart logs shell jupyter mongo clean data-sample data-full backup

# Colores para output
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[0;33m
NC=\033[0m # No Color

help: ## Mostrar esta ayuda
	@echo "$(BLUE)Airbnb Madrid MongoDB Analysis - Comandos Docker$(NC)"
	@echo ""
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Uso:$(NC) make [comando]"
	@echo "$(BLUE)Ejemplo:$(NC) make up"

up: ## Levantar todos los servicios
	@echo "$(GREEN)🚀 Levantando servicios...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Servicios iniciados$(NC)"
	@echo ""
	@echo "$(BLUE)📍 Jupyter Notebook:$(NC) http://localhost:8888"
	@echo "$(BLUE)📍 Mongo Express:$(NC)    http://localhost:8081"
	@echo ""
	@echo "💡 Ahora ejecuta: make data-sample"

down: ## Detener todos los servicios (mantiene datos)
	@echo "$(YELLOW)⏸️  Deteniendo servicios...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

stop: ## Detener servicios sin eliminar contenedores
	@echo "$(YELLOW)⏸️  Deteniendo servicios...$(NC)"
	docker-compose stop
	@echo "$(GREEN)✅ Servicios detenidos$(NC)"

restart: ## Reiniciar todos los servicios
	@echo "$(YELLOW)🔄 Reiniciando servicios...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✅ Servicios reiniciados$(NC)"

restart-app: ## Reiniciar solo la aplicación
	@echo "$(YELLOW)🔄 Reiniciando aplicación...$(NC)"
	docker-compose restart app
	@echo "$(GREEN)✅ Aplicación reiniciada$(NC)"

logs: ## Ver logs de todos los servicios
	docker-compose logs -f

logs-app: ## Ver logs de la aplicación
	docker-compose logs -f app

logs-mongo: ## Ver logs de MongoDB
	docker-compose logs -f mongodb

ps: ## Ver estado de los servicios
	@docker-compose ps

shell: ## Acceder a shell del contenedor
	@echo "$(BLUE)💻 Accediendo a shell...$(NC)"
	docker-compose exec app bash

mongo-shell: ## Acceder a MongoDB shell
	@echo "$(BLUE)🗄️  Accediendo a MongoDB...$(NC)"
	docker-compose exec mongodb mongosh -u admin -p admin123 airbnb_madrid

jupyter: ## Abrir Jupyter en el navegador
	@echo "$(BLUE)📓 Abriendo Jupyter...$(NC)"
	@(command -v xdg-open > /dev/null && xdg-open http://localhost:8888) || \
	 (command -v open > /dev/null && open http://localhost:8888) || \
	 echo "Abre manualmente: http://localhost:8888"

mongo-express: ## Abrir Mongo Express en el navegador
	@echo "$(BLUE)🗄️  Abriendo Mongo Express...$(NC)"
	@(command -v xdg-open > /dev/null && xdg-open http://localhost:8081) || \
	 (command -v open > /dev/null && open http://localhost:8081) || \
	 echo "Abre manualmente: http://localhost:8081 (user: admin, pass: admin123)"

data-sample: ## Importar datos de ejemplo (10 listings) - RÁPIDO
	@echo "$(GREEN)📥 Importando datos de ejemplo...$(NC)"
	docker-compose exec app python scripts/import_sample_data.py

data-full: ## Importar datos completos (~18,000 listings) - LENTO
	@echo "$(YELLOW)📥 Descargando datos de Inside Airbnb...$(NC)"
	docker-compose exec app python scripts/download_dataset.py
	@echo "$(YELLOW)📥 Importando datos...$(NC)"
	docker-compose exec app python scripts/import_data.py
	@echo "$(GREEN)✅ Datos completos importados$(NC)"

data-custom: ## Importar tus propios datos (CSV)
	@read -p "Ruta al archivo CSV: " filepath; \
	echo "$(YELLOW)📥 Copiando archivo al contenedor...$(NC)"; \
	docker cp $$filepath airbnb_app:/app/data/raw/custom.csv; \
	echo "$(YELLOW)📥 Importando datos...$(NC)"; \
	docker-compose exec app python scripts/import_custom_data.py data/raw/custom.csv --keep-all

data-clean: ## Limpiar base de datos
	@echo "$(YELLOW)⚠️  ¿Estás seguro? Esto eliminará todos los datos. [y/N]$(NC)" && read ans && [ $${ans:-N} = y ]
	@echo "$(YELLOW)🗑️  Limpiando base de datos...$(NC)"
	@docker-compose exec app python -c "from src.crud_operations import AirbnbCRUD; AirbnbCRUD().collection.delete_many({}); print('✅ Base de datos limpiada')"

stats: ## Ver estadísticas de la base de datos
	@echo "$(BLUE)📊 Estadísticas de MongoDB:$(NC)"
	@docker-compose exec app python -c "\
		from src.crud_operations import AirbnbCRUD; \
		from src.database import MongoDBConnection; \
		crud = AirbnbCRUD(); \
		conn = MongoDBConnection(); \
		stats = conn.get_collection_stats(); \
		print(f'\n📈 Total de listings: {crud.get_total_listings():,}'); \
		print(f'📁 Tamaño: {stats[\"size\"] / 1024 / 1024:.2f} MB'); \
		print(f'📑 Índices: {stats[\"indexes\"]}'); \
		print(f'🏘️  Barrios: {len(crud.get_distinct_values(\"neighbourhood\"))}'); \
		print(f'🏠 Tipos de habitación: {len(crud.get_distinct_values(\"room_type\"))}\n'); \
	"

build: ## Construir imágenes Docker
	@echo "$(YELLOW)🔨 Construyendo imágenes...$(NC)"
	docker-compose build
	@echo "$(GREEN)✅ Imágenes construidas$(NC)"

rebuild: ## Reconstruir imágenes desde cero
	@echo "$(YELLOW)🔨 Reconstruyendo imágenes...$(NC)"
	docker-compose build --no-cache
	@echo "$(GREEN)✅ Imágenes reconstruidas$(NC)"

clean: ## Limpiar contenedores, imágenes y volúmenes
	@echo "$(YELLOW)⚠️  Esto eliminará TODO incluyendo datos. ¿Continuar? [y/N]$(NC)" && read ans && [ $${ans:-N} = y ]
	@echo "$(YELLOW)🗑️  Limpiando...$(NC)"
	docker-compose down -v
	docker system prune -f
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

backup: ## Backup de MongoDB
	@echo "$(BLUE)💾 Creando backup...$(NC)"
	@mkdir -p backups
	docker-compose exec mongodb mongodump \
		--username admin \
		--password admin123 \
		--authenticationDatabase admin \
		--db airbnb_madrid \
		--out /data/backup
	docker cp airbnb_mongodb:/data/backup ./backups/backup_$$(date +%Y%m%d_%H%M%S)
	@echo "$(GREEN)✅ Backup creado en ./backups/$(NC)"

restore: ## Restaurar backup de MongoDB
	@read -p "Ruta del backup a restaurar: " backup_path; \
	echo "$(YELLOW)📥 Restaurando backup...$(NC)"; \
	docker cp $$backup_path airbnb_mongodb:/data/restore; \
	docker-compose exec mongodb mongorestore \
		--username admin \
		--password admin123 \
		--authenticationDatabase admin \
		--db airbnb_madrid \
		/data/restore; \
	echo "$(GREEN)✅ Backup restaurado$(NC)"

test-connection: ## Probar conexión a MongoDB
	@echo "$(BLUE)🔍 Probando conexión...$(NC)"
	@docker-compose exec app python -c "\
		from src.database import MongoDBConnection; \
		conn = MongoDBConnection(); \
		print('✅ Conexión exitosa' if conn.ping() else '❌ Error de conexión'); \
	"

install-local: ## Instalar dependencias localmente (sin Docker)
	@echo "$(YELLOW)📦 Instalando dependencias...$(NC)"
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencias instaladas$(NC)"
	@echo "💡 Activa el entorno: source venv/bin/activate"

update: ## Actualizar imágenes Docker
	@echo "$(YELLOW)🔄 Actualizando imágenes...$(NC)"
	docker-compose pull
	@echo "$(GREEN)✅ Imágenes actualizadas$(NC)"

# Shortcuts
start: up ## Alias para 'up'
sample: data-sample ## Alias para 'data-sample'
full: data-full ## Alias para 'data-full'

# Default target
.DEFAULT_GOAL := help
