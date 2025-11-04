# Fabric Quickstart – Ops Stability & Talent Performance

## 1. Activar Fabric (trial) y crear Workspace
- Inicia sesión en app.fabric.microsoft.com y habilita el trial.
- Crea **Workspace**: `AEDRON – Ops Stability (Dev)`

## 2. Lakehouse + Notebooks
- En el Workspace, crea **Lakehouse**: `ops_lakehouse_dev`
- Sube estos notebooks:
  - `01_Generate_Synthetic_Data.ipynb`
  - `02_Calculate_KPIs.ipynb`

## 3. Ejecutar
1. Abre `01_Generate_Synthetic_Data.ipynb` y corre todas las celdas.
   - Crea `/lakehouse/default/Files/raw/ops_daily.parquet`
2. Abre `02_Calculate_KPIs.ipynb` y corre todas las celdas.
   - Crea:
     - `/lakehouse/default/Tables/agent_stability`
     - `/lakehouse/default/Tables/weekly_flags`

## 4. Modelo y Reporte
- Crea un **Semantic Model** desde el Lakehouse (usa las tablas anteriores).
- Pega tus medidas DAX desde `dashboard/PowerBI/Measures_DAX.md` del repo local.
- Publica un **Report** y prueba filtros por equipo/agente/semana.

## 5. Deployment Pipelines (opcional)
- Crea pipeline Dev → Prod y vincula workspaces.
- Define reglas de parámetros si cambias rutas entre ambientes.

## 6. Git Integration (opcional)
- Vincula el Workspace Dev a tu repositorio (GitHub o Azure DevOps).
- Versiona notebooks y artefactos para ALM/CI/CD.