# System Architecture / Arquitectura del Sistema

---

## Overview / Descripción General

The **Dev Pro Portfolio Architecture** integrates modular analytics pipelines,  
synthetic data generation, and SQL-based persistence — designed for scalability, traceability,  
and test reproducibility across environments.

La **Arquitectura del Portafolio Dev Pro** integra canalizaciones analíticas modulares,  
generación de datos sintéticos y persistencia SQL, garantizando escalabilidad, trazabilidad  
y reproducibilidad de pruebas en distintos entornos.

---

## Layered Design / Diseño por Capas
```


            ┌────────────────────────────────────────┐
            │         Root Orchestration Layer        │
            │  (Makefile + CI/CD + .venv management)  │
            └────────────────────────────────────────┘
                             │
                             ▼
   ┌───────────────────────────────────────────────┐
   │       Fabric Mock Layer (Synthetic Data)      │
   │  • Data generation via NumPy / Pandas         │
   │  • Stability metrics (CV, CVM, IQR)           │
   │  • Parquet outputs for Fabric / Power BI      │
   └───────────────────────────────────────────────┘
                             │
                             ▼
   ┌───────────────────────────────────────────────┐
   │          SQL Layer (Persistent DB)            │
   │  • PostgreSQL + SQLAlchemy integration         │
   │  • Schema ops / Views orchestration            │
   │  • Dockerized with healthchecks & Adminer      │
   └───────────────────────────────────────────────┘
                             │
                             ▼
   ┌───────────────────────────────────────────────┐
   │                Analytics Layer                │
   │  • Power BI / DAX consumption                 │
   │  • Fabric-compatible tables                   │
   │  • KPI + Outlier tracking                     │
   └───────────────────────────────────────────────┘
```

---

## Data Flow / Flujo de Datos

```
[generate_rich_seed.py]
│
▼
[Parquet Files] → [PostgreSQL Tables (ops schema)]
│ │
├────────► [Views: v_exec_finance, etc.]
│
▼
[Power BI / Fabric Dashboards]
```

---

## Integration Logic / Lógica de Integración

| Layer | Input | Output | Integration Method |
|--------|--------|----------|-------------------|
| Fabric Mock | Synthetic NumPy data | Parquet tables | Pandas I/O |
| SQL | Parquet tables | Postgres schema `ops` | SQLAlchemy |
| Analytics | DB views | Power BI visuals | DirectQuery / Import |

---

## Deployment Flow / Flujo de Ejecución

### Root environment

```bash
make test-all      # Run all tests
make e2e-sql       # Launch Docker + SQL E2E test
make clean         # Reset local artifacts
```

- ✅ Local development: Python + virtualenv
- ✅ Containerized: PostgreSQL 16 + Adminer 4
- ✅ CI-ready: GitHub Actions (matrix by module)

---

# Naming & Branching Standards / Convenciones de Nombres y Ramas

## 🧩 Branching Model (Git)

| Branch Type	| Purpose |	Example |
|------------|--------------------------------------|--------------------------|
| `main` |	Stable, production-ready version | `main` |
| `develop` |	Active integration branch | `develop` |
| `feature/*` |	New features or module enhancements | `feature/sql-upsert-logic` |
| `fix/*`	| Minor fixes or patches |	`fix/docker-healthcheck` |
| `hotfix/*` | Urgent patch on main |	`hotfix/env-loader-bug` |
| `release/*` |	Version staging for delivery | `release/v1.0.0`

--- 

## 🧭 Policy:

- All commits must reference an issue or task ID if available.

- Use Squash & Merge for cleaner history.

- Tags follow semantic versioning: v1.0.0, v1.1.0, v2.0.0.

## 🧾 File & Folder Conventions

| Category |	Convention |	Example |
|-------------------|-------------------|------------------------------------|
| Python files |	`snake_case` |	`generate_rich_seed.py` |
| Tests |	`test_*` |	`test_kpi_flags.py` |
| Directories |	lowercase, dash-separated |	`ops-stability-analytics-sql/` |
| Environment files | `.env`, `.env.local` |	`.env.local` |
| Make targets |	lowercase with dashes |	`e2e-sql, test-all` |
| Docs |	UPPERCASE kebab-case |	`ARCHITECTURE.md`, `README.md` |

---

## 📌 Commit Convention

Use concise, action-based messages in imperative mood (English preferred).
Recommended format (aligns with Conventional Commits):

```
<type>(scope): <short description>

[optional body]
```

### Examples:

```
feat(sql): add upsert logic to seed generator
fix(fabric): correct CVM quartile boundaries
docs(root): add bilingual README and architecture diagram
```

Allowed types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `build`, `ci`.

## Future Enhancements / Futuras Extensiones

- ✅ CI/CD integration via GitHub Actions

- 🚀 Add integration tests with container orchestration

- ☁️ Migrate SQL pipeline to Fabric Warehouse connector

- 🔒 Hardened .env & secret management (Vault / AWS SSM)

- 📈 Power BI gateway + automatic refresh hooks

---

**Maintained by: Jorge Enrique Rodríguez Aguilera**

**Version: 1.0.0**

**Status: ✅ Stable**

---