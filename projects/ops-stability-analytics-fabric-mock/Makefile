# ===== Fabric-mock Makefile =====
PYTHON ?= ../../.venv/bin/python
PIP    ?= ../../.venv/bin/pip

SRC_DIR := src
ETL     := $(SRC_DIR)/etl/generate_synthetic_data.py
KPI     := $(SRC_DIR)/analytics/kpi_calculations.py

# Notebooks opcionales
NOTEBOOKS := $(wildcard notebooks/*.ipynb)

.PHONY: deps deps-nb run generate kpi nb-run test smoke e2e clean

deps:
	$(PIP) install -r requirements.txt

# (Opcional) deps para ejecutar notebooks localmente
deps-nb:
	$(PIP) install jupyter nbconvert nbclient ipykernel

generate:
	$(PYTHON) $(ETL) --format parquet --outdir lakehouse_sim/Files/raw

kpi:
	$(PYTHON) $(KPI)

# Ejecuta todos los notebooks en notebooks/ si existen
nb-run:
	@if [ -z "$(NOTEBOOKS)" ]; then \
		echo "ℹ️  No se encontraron notebooks en notebooks/ (omitiendo)"; \
	else \
		for nb in $(NOTEBOOKS); do \
			echo "▶ Ejecutando $$nb"; \
			jupyter nbconvert --to notebook --execute "$$nb" --inplace; \
		done; \
		echo "✅ Notebooks ejecutados"; \
	fi

run: generate kpi

test:
	pytest -q --tb=short --disable-warnings

smoke: run test
	@echo "✅ Fabric-mock smoke OK"

# E2E local: instala deps, (opcional) deps de notebooks, ejecuta notebooks, corre pipeline y tests
e2e: deps deps-nb nb-run run test
	@echo "🏁 Fabric-mock E2E OK"

clean:
	rm -rf lakehouse_sim/Files/raw/*.parquet lakehouse_sim/Tables/*.parquet