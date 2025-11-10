python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src\etl\generate_synthetic_data.py
python src\analytics\kpi_calculations.py
pytest -q
Write-Host "Done."