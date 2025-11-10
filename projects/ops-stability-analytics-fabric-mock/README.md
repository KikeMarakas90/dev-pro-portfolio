# Fabric Mock Module (`ops-stability-analytics-fabric-mock`)

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/PowerBI-Fabric%20Compatible-yellow?logo=powerbi)](https://powerbi.microsoft.com/)
[![Parquet](https://img.shields.io/badge/Format-Parquet-orange?logo=apacheparquet)](https://parquet.apache.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](../LICENSE)

---

## Overview / Descripción General

Simulated environment for **operational stability analytics** using **synthetic data**  
to validate Power BI and Microsoft Fabric pipelines.

Entorno simulado para análisis de **estabilidad operativa** mediante **datos sintéticos**,  
diseñado para validar transformaciones y modelos DAX en Power BI / Fabric.

---

## Execution / Ejecución

### Activate root environment

```bash
source ../../.venv/bin/activate
```

### Run local tests

```bash
pytest -q --tb=short --disable-warnings
```

### Generate stability outputs

```bash
python src/analytics/kpi_calculations.py
```

## Outputs are stored in:

```
lakehouse_sim/Files/enriched/
lakehouse_sim/Tables/
```

## Structure / Estructura

```
ops-stability-analytics-fabric-mock/
├─ src/
│  ├─ analytics/
│  │  ├─ kpi_calculations.py
│  │  └─ __init__.py
│  └─ __main__.py
├─ tests/
│  ├─ test_kpi_flags.py
│  └─ test_stability.py
├─ Makefile
├─ requirements.txt
└─ README.md
```

## Key Features / Características Clave

- CV / CVM computation for operational stability

- Outlier detection via IQR

- Compatibility with Fabric Lakehouse structure

- Unit-tested DAX-aligned logic

---

**Status: ✅ Stable**

**Version: 1.0.0** 