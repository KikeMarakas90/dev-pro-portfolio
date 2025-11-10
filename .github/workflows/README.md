# ⚙️ DevPro Workflows  

### Continuous Integration & Governance Layer  
*(Bilingual Executive-Tech Overview)*  

---

## 🧩 Overview | Visión general

This directory defines the **automation backbone** for the `dev-pro-portfolio` repository.  
Each workflow enforces *reliability, reproducibility and governance* across both modules:  
**Fabric Mock** (data simulation layer) and **SQL Analytics** (pipeline orchestration layer).

> Designed under the principle of **“Operational Elegance”** — minimal, traceable, auditable.

---

## 🧱 Architecture | Arquitectura

```mermaid
graph TD
  A[Push / Pull Request] --> B(CI Validation)
  B --> C{Fabric Tests ✓}
  C -->|OK| D{SQL E2E ✓}
  D -->|OK| E(Conventional Commits ✓)
  E --> F[Merge Ready]

  subgraph Nightly
    N1[3 AM UTC] --> N2[Smoke Fabric + SQL]
  end

  subgraph Release
    R1[Manual Dispatch] --> R2[Version + Changelog + Tag]
  end

  subgraph Audit
    S1[Weekly] --> S2[Lint + Security + Structure]
  end
  ```

## 🧪 01-CI.yml — Continuous Integration

  **Purpose / Propósito:**

Ensures that every commit maintains functional integrity.
Validates Fabric unit tests, SQL end-to-end pipelines, and commit naming compliance.

**Highlights:**

- pytest for Fabric mock validations

- Full Dockerized SQL E2E workflow

- Conventional Commits enforcement (feat|fix|chore|...)

- Trigger:
`on: push, pull_request`

## 🏷️ 02-Release.yml — Semantic Versioning & Changelog Automation

**Purpose / Propósito:**

Manages version evolution and traceability through automated changelog generation and tagging.

**Highlights:**

- Manual workflow_dispatch trigger (patch/minor/major)

- Updates CHANGELOG.md + VERSION variable

- Auto-tags release (vX.Y.Z) and pushes to remote

- Trigger:
`on: workflow_dispatch`

## 🌙 03-Nightly-Smoke.yml — Integrity Validation

**Purpose / Propósito:**

Daily validation that both environments (Fabric & SQL) remain healthy and deterministic.
Runs synthetic data generation and database seeding in isolation.

**Highlights:**

- Scheduled nightly execution

- Ensures consistent deterministic outputs

- Detects regressions early in the lifecycle

Trigger:
`on: schedule (daily) + manual dispatch`

## 🛡️ 04-Audit-Lite.yml — Governance & Security

**Purpose / Propósito:**

Baseline protection for code quality, repository structure, and dependency security.

**Highlights:**

- safety + bandit scans

- Repository layout validation

- Weekly cadence for preventive compliance

Trigger:
`on: push, pull_request, schedule (weekly)`

## 🌐 Governance Narrative | Narrativa de Gobernanza

Each workflow contributes to a CI/CD maturity model:

| Layer	| Function | Control Objective |
|--------------------|------------------|---------------------------------|
| CI Validation | Automated Testing | Ensure operational consistency
| Release Automation |	Version Traceability | Guarantee change provenance
| Nightly Smoke | Predictive Monitoring	| Detect early degradation
| Audit Lite | Structural Security | Maintain compliance baseline

---

**Maintainer:**

Jorge Enrique Rodríguez Aguilera (Enrique Rodríguez)

[LinkedIn](https://www.linkedin.com/in/enrique-rodr%C3%ADguez-007236243)