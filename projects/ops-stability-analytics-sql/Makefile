# ==========================================================
# AEDRON | ops-stability-analytics-sql
# Makefile — Ejecuta entorno SQL (Docker + Seed + Views) (CI-safe)
# ==========================================================

ENV_FILE ?= .env.local

# Descubre un Python válido (local o CI) sin depender de .venv
PY ?= $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)

DB_CONTAINER := ops_db
ADMINER_CONTAINER := ops_adminer

# ----------------------------------------------------------
# 🔧 Base
# ----------------------------------------------------------
.PHONY: up down ps wait seed views smoke e2e-sql logs status clean test

up:
	@echo ">> Iniciando contenedores Docker"
	docker compose up -d

wait:
	@echo "⏳ Esperando healthcheck de Postgres..."
	@until [ "$$(docker inspect -f '{{.State.Health.Status}}' $(DB_CONTAINER))" = "healthy" ]; do \
		printf "."; sleep 2; \
	done; echo " OK"
	@docker compose ps --format "table {{.Name}}\t{{.State}}\t{{.Ports}}"

down:
	@echo ">> Deteniendo y limpiando contenedores"
	docker compose down -v

ps:
	@docker compose ps --format "table {{.Name}}\t{{.State}}\t{{.Ports}}"

# ----------------------------------------------------------
# 💾 Seed de base de datos (Postgres)
# ----------------------------------------------------------
seed:
	@echo ">> DB seed usando $(ENV_FILE)"
	@echo ">> PY = $(PY)"
	ENV_FILE=$(ENV_FILE) WRITE_DB=1 $(PY) src/sql/generate_rich_seed.py

# ----------------------------------------------------------
# 🧱 Creación / actualización de vistas SQL
# ----------------------------------------------------------
views:
	@echo ">> Creando/actualizando vistas ($(ENV_FILE))"
	@cat sql/views_enriched.sql | \
	  docker exec -e PGPASSWORD=$$(grep POSTGRES_PASSWORD $(ENV_FILE) | cut -d '=' -f2) -i $(DB_CONTAINER) \
	    psql -U $$(grep POSTGRES_USER $(ENV_FILE) | cut -d '=' -f2) \
	        -d $$(grep POSTGRES_DB   $(ENV_FILE) | cut -d '=' -f2) \
	        -v ON_ERROR_STOP=1 -f -

# ----------------------------------------------------------
# ✅ Smoke test SQL (opcional)
# ----------------------------------------------------------
smoke:
	@echo ">> Smoke SQL ($(ENV_FILE))"
	@docker exec -e PGPASSWORD=$$(grep POSTGRES_PASSWORD $(ENV_FILE) | cut -d '=' -f2) -i $(DB_CONTAINER) \
	  psql -U $$(grep POSTGRES_USER $(ENV_FILE) | cut -d '=' -f2) \
	      -d $$(grep POSTGRES_DB   $(ENV_FILE) | cut -d '=' -f2) \
	      -c "select current_database(), current_user, now();"

# ----------------------------------------------------------
# 🚀 E2E completo
# ----------------------------------------------------------
e2e-sql: up wait seed views smoke
	@echo "✅ E2E SQL completado correctamente"

# ----------------------------------------------------------
# 🧹 Utilidades
# ----------------------------------------------------------
logs:
	@docker logs $(DB_CONTAINER) --tail 50

status:
	@docker inspect -f '{{.State.Health.Status}}' $(DB_CONTAINER)

clean:
	@echo ">> Eliminando artefactos locales"
	rm -rf lakehouse_sim/Files/enriched/*.parquet
	rm -rf lakehouse_sim/Tables/*.parquet

# ----------------------------------------------------------
# 🧪 Test placeholder (para compatibilidad con test-all)
# ----------------------------------------------------------
test:
	@echo ">> Running SQL smoke test"
	@docker exec -e PGPASSWORD=$$(grep POSTGRES_PASSWORD $(ENV_FILE) | cut -d '=' -f2) -i $(DB_CONTAINER) \
	  psql -U $$(grep POSTGRES_USER $(ENV_FILE) | cut -d '=' -f2) \
	      -d $$(grep POSTGRES_DB   $(ENV_FILE) | cut -d '=' -f2) \
	      -c "select count(*) as tables_in_ops_schema from information_schema.tables where table_schema='ops';"