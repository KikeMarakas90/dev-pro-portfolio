# SQL Module (`ops-stability-analytics-sql`)

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.12-green?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](../LICENSE)

---

## Overview / Descripción General

Implements **data pipelines and schema orchestration** using PostgreSQL, SQLAlchemy,  
and Docker Compose — including full E2E validation with seed data and health checks.

Implementa canalizaciones de datos y orquestación de esquemas con PostgreSQL, SQLAlchemy  
y Docker Compose — incluye validación E2E con datos sintéticos y pruebas de salud.

---

## Execution / Ejecución

### Run full end-to-end process

```bash
make e2e-sql
```

### Or run independently:

```bash
make up
make seed
make views
make smoke
```

## Access Adminer:

```
http://localhost:8080
```

## Structure / Estructura

```
ops-stability-analytics-sql/
├─ src/
│  └─ sql/
│     ├─ generate_rich_seed.py
│     └─ __init__.py
├─ docker/
│  ├─ Dockerfile
│  ├─ docker-compose.yml
│  ├─ pg_hba.conf
│  └─ postgres.conf
├─ sql/
│  └─ views_enriched.sql
├─ .env.local
├─ Makefile
└─ README.md
```

## Key Features / Características Clave

- Postgres containerized pipeline

- Secure .env configuration

- Schema creation + upsert logic

- Healthcheck and smoke validation

- Parquet–SQL hybrid compatibility

---

**Status: ✅ Stable**

**Version: 1.0.0**

