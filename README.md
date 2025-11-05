<p align="center">
  <img src="https://img.shields.io/badge/AEDRON_Data_&_Cloud_Intelligence-262626?style=for-the-badge&logo=databricks&logoColor=white" alt="AEDRON Banner"/>
</p>


# 🧠 Dev Pro Portfolio – Jorge Enrique Rodríguez Aguilera

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/PowerBI-DAX%20%7C%20Modeling-yellow?logo=powerbi)](https://powerbi.microsoft.com/)
[![CI/CD](https://img.shields.io/github/actions/workflow/status/KikeMarakas90/dev-pro-portfolio/ci.yml?label=CI%2FCD&logo=githubactions)](https://github.com/KikeMarakas90/dev-pro-portfolio/actions)
[![License](https://img.shields.io/github/license/KikeMarakas90/dev-pro-portfolio?color=green)](LICENSE)

---

> **EN:** Professional portfolio focused on **Business Intelligence, Cloud Integration, and Ethical Automation**, built as a modular laboratory for applied data engineering, analytics, and CI/CD in hybrid environments.

> **ES:** Portafolio técnico orientado a **Business Intelligence, Integración Cloud y Automatización Ética**, diseñado como laboratorio modular para prácticas de ingeniería de datos, análisis avanzado y CI/CD en entornos híbridos.

---

## 🧩 Repository Structure | Estructura del Repositorio

```bash
dev-pro-portfolio/
│
├── .github/workflows/       # CI/CD (pytest / build / coverage)
├── cases/                   # Data analysis cases / Casos analíticos
├── dashboards/              # Power BI dashboards, DAX templates
├── docs/                    # Technical & executive documentation
├── projects/                # Core projects & frameworks
│   └── ops-stability-analytics/   # Fabric-ready validated project with CI/CD
│
├── scripts/                 # Utility & automation scripts
├── LICENSE
├── README.md
└── requirements.txt
```

## 🚀 Active Projects | Proyectos Activos

| Project | Description | Estado | Stack |
|----------|--------------|--------|--------|
| [**Ops Stability Analytics**](projects/ops-stability-analytics) | **EN:** End-to-end Fabric-ready pipeline for synthetic data generation, KPI computation (CV, CVM, IQR), and CI/CD validation.<br>**ES:** Pipeline local “Fabric-ready” para generación de datos sintéticos, cálculo de KPIs (CV, CVM, IQR) y validación CI/CD. | 🟢 Active / Activo | Python, PyArrow, Pandas, PyTest, Power BI |
| *(coming soon)* **AEDRON Integrator Framework (AIF)** | **EN:** Composable middleware for cloud-agnostic integrations with embedded governance.<br>**ES:** Middleware composable, Python-native y vendor-agnostic con gobernanza integrada. | 🟡 Design / En diseño | Python, FastAPI, Azure/AWS SDK |

---

## ⚙️ Development Environment | Entorno de Desarrollo

### Create virtual environment / Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies / Instalar dependencias

```bash
pip install -r requirements.txt
```

### Run pipeline (subproject) / Ejecutar pipeline

```bash
cd projects/ops-stability-analytics
make run
```

## 🧪 CI/CD Pipeline

- **Automation / Automatización:** GitHub Actions + PyTest  
- **Validation / Validación:** modular structure + unit tests in `src/tests`  
- **Results / Resultados:** pipeline verified (`2 passed in <1s>`)  
- **Objective / Objetivo:** reproducible BI / DataOps workflows with enterprise best practices  

## 🧭 Author | Autor

**Jorge Enrique Rodríguez Aguilera**

**Consultor en Business Intelligence, Cloud Integrations & Data Governance.**

**📍 México**

🔗 [LinkedIn](https://www.linkedin.com/in/enrique-rodr%C3%ADguez-007236243)

## 🪶 License | Licencia
Distributed under the MIT License.
Consulta el archivo LICENSE para más detalles.

---