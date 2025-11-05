# ===========================================================
# AEDRON | Ops Stability Analytics - Makefile
# ===========================================================
# Descripción:
# Automatiza la ejecución local del pipeline Fabric-ready:
# 1. Configura entorno virtual
# 2. Ejecuta scripts de ETL y KPI
# 3. Corre pruebas unitarias
# 4. Permite limpiar o desactivar entorno
# ===========================================================

PYTHON := python
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate

# ----------------------------------------
#  Inicialización del entorno virtual
# ----------------------------------------
init:
	@echo "🧱 Creando entorno virtual..."
	$(PYTHON) -m venv $(VENV)
	@$(ACTIVATE) && pip install --upgrade pip && pip install -r requirements.txt
	@echo "✅ Entorno listo."

# ----------------------------------------
#  Ejecución del pipeline (ETL + KPIs)
# ----------------------------------------
run:
	@echo "🚀 Ejecutando pipeline completo..."
	@$(ACTIVATE) && \
	$(PYTHON) src/etl/generate_synthetic_data.py && \
	$(PYTHON) src/analytics/kpi_calculations.py && \
	pytest -q --tb=short --disable-warnings
	@echo "✅ Pipeline completado con éxito."

# ----------------------------------------
#  Pruebas unitarias
# ----------------------------------------
test:
	@echo "🧪 Ejecutando pruebas unitarias..."
	@$(ACTIVATE) && pytest -q --tb=short --disable-warnings

# ----------------------------------------
#  Limpieza (archivos temporales y datos)
# ----------------------------------------
clean:
	@echo "🧹 Limpiando artefactos..."
	rm -rf __pycache__ .pytest_cache
	rm -rf lakehouse_sim/Files/raw/*.parquet
	rm -rf lakehouse_sim/Tables/*.parquet
	@echo "✅ Limpieza completada."

# ----------------------------------------
#  Desactivar entorno virtual
# ----------------------------------------
deactivate:
	@echo "🔒 Desactivando entorno virtual..."
	deactivate || true
	@echo "✅ Entorno desactivado."

# ----------------------------------------
#  Ayuda
# ----------------------------------------
help:
	@echo ""
	@echo "Comandos disponibles:"
	@echo "  make init         → Crear e inicializar entorno virtual"
	@echo "  make run          → Ejecutar pipeline completo"
	@echo "  make test         → Ejecutar pruebas unitarias"
	@echo "  make clean        → Limpiar artefactos temporales"
	@echo "  make deactivate   → Desactivar entorno virtual"
	@echo ""
	