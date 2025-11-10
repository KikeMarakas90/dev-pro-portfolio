#!/usr/bin/env bash
set -e
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/etl/generate_synthetic_data.py
python src/analytics/kpi_calculations.py
pytest -q || true
echo "Done."