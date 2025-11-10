# ===== Fabric-mock Makefile =====
PYTHON ?= ../../.venv/bin/python
PIP    ?= ../../.venv/bin/pip

SRC_DIR := src
ETL     := $(SRC_DIR)/etl/generate_synthetic_data.py
KPI     := $(SRC_DIR)/analytics/kpi_calculations.py

.PHONY: deps run generate kpi test smoke e2e clean

deps:
	$(PIP) install -r requirements.txt

generate:
	$(PYTHON) $(ETL) --format parquet --outdir lakehouse_sim/Files/raw

kpi:
	$(PYTHON) $(KPI)

run: generate kpi

test:
	pytest -q --tb=short --disable-warnings

smoke: run test
	@echo "✅ Fabric-mock smoke OK"

e2e: deps run test
	@echo "🏁 Fabric-mock E2E OK"

clean:
	rm -rf lakehouse_sim/Files/raw/*.parquet lakehouse_sim/Tables/*.parquet