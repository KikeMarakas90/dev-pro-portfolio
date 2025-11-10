# -*- coding: utf-8 -*-
"""
Smoke test for Ops Stability Analytics
- Verifica pipeline Fabric-mock (Parquet)
- (Opcional) Verifica capa SQL si SMOKE_SQL=1
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

def fail(msg: str) -> None:
    print(f"❌ {msg}")
    sys.exit(1)

def ok(msg: str) -> None:
    print(f"✅ {msg}")

def check_columns(df: pd.DataFrame, required: list[str], name: str) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        fail(f"{name}: faltan columnas {missing}")

def smoke_fabric(py_bin: str) -> None:
    # 1) Raw
    rc = os.system(f"{py_bin} src/etl/generate_synthetic_data.py")
    if rc != 0:
        fail("Fallo al ejecutar generate_synthetic_data.py")
    # 2) KPIs -> stability + flags
    rc = os.system(f"{py_bin} src/analytics/kpi_calculations.py")
    if rc != 0:
        fail("Fallo al ejecutar kpi_calculations.py")

    lh = Path(os.getenv("LAKEHOUSE_PATH", "lakehouse_sim"))
    raw_parquet = lh / "Files" / "raw" / "ops_daily.parquet"
    stab_parquet = lh / "Tables" / "agent_stability.parquet"
    flags_parquet = lh / "Tables" / "weekly_flags.parquet"

    for p in [raw_parquet, stab_parquet, flags_parquet]:
        if not p.exists():
            fail(f"No se generó {p}")

    raw = pd.read_parquet(raw_parquet)
    stab = pd.read_parquet(stab_parquet)
    flags = pd.read_parquet(flags_parquet)

    if raw.empty:  fail("raw (ops_daily.parquet) está vacío")
    if stab.empty: fail("agent_stability.parquet vacío")
    if flags.empty:fail("weekly_flags.parquet vacío")

    check_columns(raw,  ["date","agent_id","team_id","productive_hours","cases_closed"], "raw")
    check_columns(stab, ["agent_id","team_id","cv_hours","cvm_hours","cv_cases","cvm_cases","quartile_efficiency"], "agent_stability")
    check_columns(flags, ["agent_id","team_id","iso_year","iso_week","hours_mean","cases_mean","out_hours_flag","out_cases_flag"], "weekly_flags")

    for col in ["out_hours_flag","out_cases_flag"]:
        s = set(pd.Series(flags[col]).dropna().unique().tolist())
        if not s.issubset({0,1}):
            fail(f"{col} contiene valores no binarios: {s}")

    ok(f"Fabric-mock OK: {len(raw)} raw, {len(stab)} stability, {len(flags)} weekly_flags")

def smoke_sql() -> None:
    try:
        from sqlalchemy import create_engine, text
    except Exception as e:
        fail(f"No se pudo importar SQLAlchemy: {e}")

    # Construye URL desde env (DATABASE_URL o vars POSTGRES_*)
    url = os.getenv("DATABASE_URL")
    if not url:
        host = os.getenv("POSTGRES_HOST","localhost")
        port = os.getenv("POSTGRES_PORT","5432")
        db   = os.getenv("POSTGRES_DB","ops_analytics")
        user = os.getenv("POSTGRES_USER","ops_user")
        pwd  = os.getenv("POSTGRES_PASSWORD","ops_pass")
        url = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"

    eng = create_engine(url, pool_pre_ping=True)
    with eng.connect() as cx:
        cx.execute(text("SELECT 1"))

        for tbl in [
            "ops.synthetic_agent",
            "ops.synthetic_weekly_perf",
            "ops.synthetic_budget_weekly",
            "ops.synthetic_capacity_weekly",
        ]:
            cnt = cx.execute(text(f"SELECT COUNT(*) FROM {tbl}")).scalar()
            if not cnt:
                fail(f"{tbl} sin datos (count=0)")
        ok("Tablas sintéticas OK")

        cols = cx.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_schema='ops' AND table_name='v_exec_finance'
        """)).fetchall()
        if not cols:
            fail("Vista ops.v_exec_finance no existe")

        cnt_view = cx.execute(text("SELECT COUNT(*) FROM ops.v_exec_finance")).scalar()
        if not cnt_view:
            fail("ops.v_exec_finance sin filas")

        sample = cx.execute(text("""
            SELECT team_id, iso_year, iso_week, revenue, hours, cost_real, margin
            FROM ops.v_exec_finance
            ORDER BY iso_year DESC, iso_week DESC
            LIMIT 5
        """)).fetchall()
        if not sample:
            fail("ops.v_exec_finance no devuelve resultados")
        ok(f"SQL OK: v_exec_finance rows={cnt_view}")

if __name__ == "__main__":
    load_dotenv()
    py = os.getenv("PYTHON_BIN", sys.executable)
    smoke_fabric(py)
    if os.getenv("SMOKE_SQL","0") == "1":
        smoke_sql()
    print("🎯 Smoke test COMPLETO: Fabric-mock + (opcional) SQL")