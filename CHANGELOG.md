# Changelog  
_All notable changes to this project will be documented in this file._  

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-11-09  

### 🚀 Initial Stable Release

#### 🧠 Root Repository (`dev-pro-portfolio`)
- Added bilingual `README.md` and unified **technical scoreboard layout**.  
- Integrated centralized virtual environment (`.venv` in root).  
- Added root-level `Makefile` with orchestration targets:
  - `test-all` → executes Fabric & SQL validation.  
  - `e2e-sql` → launches full Docker + SQL end-to-end process.  
- Established common `.gitignore` and documentation templates.  
- Introduced `ARCHITECTURE.md` and `CHANGELOG.md`.  

#### 🧩 Fabric Mock Module (`ops-stability-analytics-fabric-mock`)
- Implemented synthetic dataset generator using **NumPy + Pandas**.  
- Added robust statistical metrics:
  - Coefficient of Variation (CV).  
  - Median-based CV (CVM).  
  - IQR-based outlier flagging.  
- Created `pytest`-based unit tests (7 passing).  
- Aligned lakehouse simulation paths to Fabric schema:
  - `lakehouse_sim/Files/enriched/`  
  - `lakehouse_sim/Tables/`  
- Documentation:
  - Added bilingual `README.md`.  
  - Integrated compatibility with root Makefile.  

#### 🗄 SQL Module (`ops-stability-analytics-sql`)
- Added PostgreSQL 16 + Adminer Docker Compose stack.  
- Hardened configuration:
  - `pg_hba.conf` (SCRAM-SHA-256).  
  - `postgresql.conf` with explicit `listen_addresses=*`.  
- Developed `generate_rich_seed.py` for enriched synthetic data:
  - Schema auto-creation (`ops`).  
  - Upsert logic (TRUNCATE + append).  
  - Healthcheck fallback between `db` and `localhost`.  
- Added E2E validation pipeline:
  - `make e2e-sql` for smoke + seed + view creation.  
  - Healthcheck and `psql` inline verification.  
- Documentation:
  - Added bilingual `README.md`.  
  - Included secure `.env` and `.env.local` templates.

#### 🧱 Docs & Standards
- Added `ARCHITECTURE.md` with bilingual layered system diagram:
  - Root orchestration layer.  
  - Fabric Mock layer.  
  - SQL persistence layer.  
  - Analytics (Power BI/Fabric) layer.  
- Included **Naming, Branching & Commit Conventions** section.  
- Version control alignment for CI/CD readiness.

---

### 🧩 Summary of Technical Baseline
| Layer | Stack | Validation |
|--------|--------|-------------|
| Fabric Mock | Python, Pandas, Pytest | ✅ 7/7 tests passed |
| SQL | Python, Docker, PostgreSQL | ✅ E2E pipeline healthy |
| Root | Make + GitHub Actions Ready | ⚙️ Next step: CI/CD integration |

---

## Planned for [1.1.0]  
### 🧭 Enhancements
- Add **integration tests** (container orchestration validation).  
- Introduce **GitHub Actions CI pipeline** with matrix jobs.  
- Add **Fabric Warehouse connector** integration.  
- Embed **CHANGELOG auto-version bump** task in Makefile.  
- Add **Power BI Gateway refresh hooks**.

---

**Maintained by:**  
**Jorge Enrique Rodríguez Aguilera**  
_Consultor en Business Intelligence, Cloud Integrations & Data Governance_  
📍 México  
🔗 [LinkedIn](https://www.linkedin.com/in/enrique-rodr%C3%ADguez-007236243)