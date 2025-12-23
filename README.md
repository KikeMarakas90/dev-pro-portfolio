<p align="center">
  <img src="https://img.shields.io/badge/Data_&_Cloud_Intelligence-262626?style=for-the-badge&logo=databricks&logoColor=white" alt="AEDRON Banner"/>
</p>

# 🧠 Dev Pro Portfolio – Jorge Enrique Rodríguez Aguilera

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/PowerBI-DAX%20%7C%20Modeling-yellow?logo=powerbi)](https://powerbi.microsoft.com/)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/KikeMarakas90/dev-pro-portfolio/ci.yml?label=CI%2FCD&logo=githubactions)](https://github.com/KikeMarakas90/dev-pro-portfolio/actions)
[![License](https://img.shields.io/github/license/KikeMarakas90/dev-pro-portfolio?color=green)](LICENSE)

---

## Overview / Descripción General

The **Dev Pro Portfolio** consolidates modular analytical and integration projects focused on  
**Business Intelligence, Process Optimization, and Cloud Architecture**.

Each subproject is independently executable yet shares a unified set of technical governance standards  
to ensure scalability, resilience, and production readiness.

El **Portafolio Dev Pro** consolida proyectos modulares orientados a la **Inteligencia de Negocios,  
Optimización de Procesos y Arquitectura Cloud**, manteniendo consistencia técnica y trazabilidad entre entornos.

---

## Modules / Módulos

| Module | Purpose / Propósito | Stack Tecnológico |
|--------|----------------------|-------------------|
| **Fabric Mock Module** (`ops-stability-analytics-fabric-mock`) | Synthetic datasets and stability analytics for Power BI / Fabric integration | Python, Pandas, Parquet |
| **SQL Module** (`ops-stability-analytics-sql`) | PostgreSQL pipelines, data seeding, and schema management with SQLAlchemy | Python, Docker, PostgreSQL |

---

## Repository Layout / Estructura del Repositorio

```
dev-pro-portfolio/
├─ projects/
│ ├─ ops-stability-analytics-fabric-mock/
│ └─ ops-stability-analytics-sql/
├─ docs/
│ └─ ARCHITECTURE.md
├─ scripts/
└─ .github/workflows/
```

---

## Test Matrix / Matriz de Pruebas

| Test Type | Module | Status |
|------------|---------|--------|
| Unit tests (Pytest) | Fabric Mock | ✅ Passed |
| E2E smoke (Make + Docker + SQLAlchemy) | SQL | ✅ Passed |
| CI-ready (future) | Root pipeline | ⚙️ Planned |

---

## Technical Standards / Estándares Técnicos

- Environment control: `.env`, `.env.local`
- Versioning: Semantic (`v1.0.0`)
- CI/CD: GitHub Actions
- Tests: `pytest` / `make`
- Documentation: Markdown bilingual

---

## Author / Autor

**Jorge Enrique Rodríguez Aguilera**  
Consultor en Business Intelligence, Cloud Integrations & Data Governance  
📍 México  
🔗 [LinkedIn](https://www.linkedin.com/in/enrique-rodr%C3%ADguez-007236243)

---

## License / Licencia
Distributed under the MIT License. 
Consulta el archivo LICENSE para más detalles.