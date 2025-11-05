# Ops Stability & Talent Performance Analytics

[![CI/CD](https://github.com/KikeMarakas90/dev-pro-portfolio/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/KikeMarakas90/dev-pro-portfolio/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Fabric Ready](https://img.shields.io/badge/Fabric%20Ready-lakehouse--sim-brightgreen?logo=microsoft)](https://learn.microsoft.com/en-us/fabric/)
[![License](https://img.shields.io/github/license/KikeMarakas90/dev-pro-portfolio?color=green)](../../LICENSE)

**Tagline:** KPIs de estabilidad operativa y desempeño con trazabilidad ética, listos para entrevista.

Este repositorio demuestra un caso end-to-end: generación de datos sintéticos, ETL, KPIs de estabilidad (CV / CVM), outliers, segmentación por cuartiles y una capa de medidas DAX para un dashboard (Power BI). Incluye CI con `pytest` para validar cálculos.

## Pitch de entrevista (30 segundos)
Construí un pipeline reproducible que simula operaciones y desempeño por agente, calcula estabilidad con enfoques robustos (mediana y IQR), clasifica por cuartiles y entrega medidas DAX listas para Power BI. La repo trae CI, pruebas unitarias, docker-compose con Postgres y una guía para levantar todo en 10 minutos.

## Arquitectura
```mermaid
flowchart LR
  A[Sintetizador de datos] --> B[ETL Python]
  B --> C[(Postgres)]
  C --> D[KPIs (Python)]
  D --> E[Medidas DAX / Power BI]
  E --> F[Dashboard / Entrevista]
```

## Quickstart
```bash
# 1) Crear venv
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Generar datos + KPIs
python src/etl/generate_synthetic_data.py
python src/analytics/kpi_calculations.py

# 4) Correr pruebas
pytest -q
```

## Contenido clave
- `src/etl/generate_synthetic_data.py`: genera dataset realista (agente, equipo, fecha, horas productivas, casos resueltos, etc.).
- `src/analytics/kpi_calculations.py`: calcula CV, CVM, flags de outlier e índices de eficiencia relativa.
- `dashboard/PowerBI/Measures_DAX.md`: medidas DAX listas para pegar en tu modelo.
- `docs/architecture.md`: decisiones de diseño y diagrama.
- CI con `pytest` en `.github/workflows/ci.yml`.

## Roadmap corto
- [ ] Cargar a Postgres con `load_to_postgres.py` (opcional)
- [ ] Publicar dashboard en Fabric/Service (si aplica)
- [ ] Añadir notebook con EDA