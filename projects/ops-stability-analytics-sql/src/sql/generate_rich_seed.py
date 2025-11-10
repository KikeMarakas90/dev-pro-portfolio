# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
import os
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError

# ----------------------------
# Configuración y constantes
# ----------------------------
RNG = np.random.default_rng(123)

N_AGENTS = 60
TEAMS = [f"T{i}" for i in range(1, 7)]
ROLES = ["Analyst", "Senior Analyst", "Lead"]
SALARY_BANDS = {
    "Analyst": (18000, 26000),
    "Senior Analyst": (26000, 36000),
    "Lead": (36000, 48000),
}
HOURS_CAPACITY_WEEK = {"Analyst": 40, "Senior Analyst": 42, "Lead": 45}

CASE_TYPES = ["Standard", "Priority", "Escalation"]
CASE_PRICE = {"Standard": 110.0, "Priority": 150.0, "Escalation": 220.0}

WEEKS = 26

# Lakehouse sim outputs (parquet)
LH = Path("lakehouse_sim")
FILES = LH / "Files" / "enriched"
TABLES = LH / "Tables"
for p in [FILES, TABLES]:
    p.mkdir(parents=True, exist_ok=True)

# ----------------------------
# Utilidades
# ----------------------------
def _random_salary(role: str) -> float:
    lo, hi = SALARY_BANDS[role]
    return float(RNG.normal((lo + hi) / 2, (hi - lo) / 6))

def _hourly_cost(monthly_salary: float) -> float:
    # Costo/hora aprox: salario mensual / (4.33 semanas * 40h) + 25% overhead
    base = monthly_salary / (4.33 * 40.0)
    return float(base * 1.25)

# ----------------------------
# Constructores de dataframes
# ----------------------------
def build_dimensions():
    # Teams
    df_team = pd.DataFrame(
        {"team_id": TEAMS, "team_name": [f"Team {t[1:]}" for t in TEAMS]}
    )

    # Agents
    agents = []
    for i in range(1, N_AGENTS + 1):
        role = RNG.choice(ROLES, p=[0.55, 0.35, 0.10])
        team = TEAMS[(i % len(TEAMS))]
        salary = max(10000.0, _random_salary(role))
        hourly = _hourly_cost(salary)
        hire_date = pd.Timestamp.today().normalize() - pd.Timedelta(
            days=int(RNG.integers(120, 1200))
        )
        agents.append(
            (
                f"AG{str(i).zfill(3)}",
                team,
                role,
                round(salary, 2),
                round(hourly, 2),
                hire_date.date(),
            )
        )
    df_agent = pd.DataFrame(
        agents,
        columns=[
            "agent_id",
            "team_id",
            "role",
            "monthly_salary",
            "hourly_cost",
            "hire_date",
        ],
    )

    # Pricing por tipo de caso
    df_case_price = pd.DataFrame(
        [(ct, CASE_PRICE[ct]) for ct in CASE_TYPES],
        columns=["case_type", "price_per_case"],
    )

    return df_team, df_agent, df_case_price

def build_calendar_weeks():
    # Últimas WEEKS semanas ISO
    end = pd.Timestamp.today().normalize()
    start = end - pd.Timedelta(weeks=WEEKS)
    days = pd.date_range(start=start, end=end, freq="D")
    cal = pd.DataFrame({"date": days})
    iso = cal["date"].dt.isocalendar()
    cal["iso_year"] = iso.year.astype(int)
    cal["iso_week"] = iso.week.astype(int)
    cal = cal.drop_duplicates(["iso_year", "iso_week"]).sort_values(
        ["iso_year", "iso_week"]
    )
    return cal[["iso_year", "iso_week"]].reset_index(drop=True)

def build_capacity_budget(df_agent: pd.DataFrame, cal_weeks: pd.DataFrame):
    # Capacidad por agente/semana y presupuesto por equipo/semana
    rows_cap, rows_budget = [], []

    for _, a in df_agent.iterrows():
        role = a["role"]
        cap = HOURS_CAPACITY_WEEK[role]
        for _, w in cal_weeks.iterrows():
            rows_cap.append(
                (a["agent_id"], a["team_id"], int(w["iso_year"]), int(w["iso_week"]), cap)
            )
    df_capacity = pd.DataFrame(
        rows_cap, columns=["agent_id", "team_id", "iso_year", "iso_week", "capacity_hours"]
    )

    team_hourly_mean = df_agent.groupby("team_id")["hourly_cost"].mean().to_dict()
    for team in TEAMS:
        for _, w in cal_weeks.iterrows():
            cap_team = df_capacity.loc[
                (df_capacity["team_id"] == team)
                & (df_capacity["iso_year"] == w["iso_year"])
                & (df_capacity["iso_week"] == w["iso_week"]),
                "capacity_hours",
            ].sum()
            planned_hours = float(cap_team * 0.85 * RNG.uniform(0.95, 1.05))
            planned_cost = planned_hours * float(team_hourly_mean[team])
            rows_budget.append(
                (team, int(w["iso_year"]), int(w["iso_week"]), round(planned_hours, 2), round(planned_cost, 2))
            )
    df_budget = pd.DataFrame(
        rows_budget, columns=["team_id", "iso_year", "iso_week", "planned_hours", "planned_cost"]
    )
    return df_capacity, df_budget

def build_weekly_perf(df_agent: pd.DataFrame, cal_weeks: pd.DataFrame, df_case_price: pd.DataFrame):
    # Rendimiento semanal por agente, con estacionalidad y mix de casos
    records = []
    for _, a in df_agent.iterrows():
        base_hours = RNG.normal(34, 4)
        for _, w in cal_weeks.iterrows():
            season = 1.0 + 0.10 * np.sin((w["iso_week"] % 10) / 10 * 2 * np.pi)
            hours = max(10.0, RNG.normal(base_hours * season, 3.0))

            mix = RNG.dirichlet([8, 3, 1])  # mayormente Standard
            cases_total = max(5.0, RNG.normal(hours * RNG.uniform(2.4, 3.4), 4.0))
            cases = (cases_total * mix).round(0).astype(int)
            case_counts = dict(zip(CASE_TYPES, cases))
            revenue = sum(case_counts[ct] * CASE_PRICE[ct] for ct in CASE_TYPES)

            # Flags simples (IQR-like aprox)
            cph = cases_total / max(hours, 1.0)
            out_hours = int(hours < 24 or hours > 50)
            out_cases = int(cph < 1.8 or cph > 4.2)

            records.append(
                (
                    a["agent_id"],
                    a["team_id"],
                    int(w["iso_year"]),
                    int(w["iso_week"]),
                    float(hours),
                    float(cases_total),
                    int(case_counts["Standard"]),
                    int(case_counts["Priority"]),
                    int(case_counts["Escalation"]),
                    float(revenue),
                    out_hours,
                    out_cases,
                )
            )

    cols = [
        "agent_id",
        "team_id",
        "iso_year",
        "iso_week",
        "hours",
        "cases_total",
        "cases_standard",
        "cases_priority",
        "cases_escalation",
        "revenue",
        "out_hours_flag",
        "out_cases_flag",
    ]
    df_wp = pd.DataFrame(records, columns=cols)

    # Medias “semanales” compatibles con modelo
    df_wp["hours_mean"] = df_wp["hours"]
    df_wp["cases_mean"] = df_wp["cases_total"]
    return df_wp

# ----------------------------
# Persistencia
# ----------------------------
def write_parquet(dfs: dict[str, pd.DataFrame]):
    for name, df in dfs.items:
        out = FILES / f"{name}.parquet"
        df.to_parquet(out, index=False)
        print(f"💾 Wrote {len(df):,} rows → {out}")

def make_engine_from_env():
    """Crea engine usando .env, con fallback host=db → localhost."""
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db   = os.getenv("POSTGRES_DB", "ops_analytics")
    user = os.getenv("POSTGRES_USER", "ops_user")
    pwd  = os.getenv("POSTGRES_PASSWORD", "ops_pass")

    def _make(h):
        url = f"postgresql+psycopg://{user}:{pwd}@{h}:{port}/{db}"
        eng = create_engine(url, pool_pre_ping=True, future=True)
        with eng.connect() as cx:
            cx.exec_driver_sql("SELECT 1")
        return eng

    try:
        return _make(host)
    except OperationalError:
        if host != "localhost":
            return _make("localhost")
        raise

def write_postgres(dfs: dict[str, pd.DataFrame]):
    """Carga idempotente: CREATE SCHEMA si no existe; TRUNCATE+append si existe, replace si no."""
    load_dotenv()
    if os.environ.get("WRITE_DB", "0") != "1":
        print("WRITE_DB=0 → skipping DB load")
        return

    eng = make_engine_from_env()

    # Asegura esquema
    with eng.begin() as cx:
        cx.execute(text("CREATE SCHEMA IF NOT EXISTS ops"))

    insp = inspect(eng)
    order = [
        "team", "agent", "case_pricing",
        "calendar_weeks", "capacity_weekly", "budget_weekly",
        "weekly_perf",
    ]

    for name in order:
        tbl = f"synthetic_{name}"
        full = f"ops.{tbl}"

        if insp.has_table(tbl, schema="ops"):
            # existe → vaciar y luego append
            with eng.begin() as cx:
                cx.execute(text(f"TRUNCATE TABLE {full} RESTART IDENTITY"))
            dfs[name].to_sql(tbl, eng, schema="ops", if_exists="append", index=False)
        else:
            # no existe → crear
            dfs[name].to_sql(tbl, eng, schema="ops", if_exists="replace", index=False)

        print(f"🗄 Upserted {full} ({len(dfs[name])} rows)")

# ----------------------------
# Main (E2E)
# ----------------------------
if __name__ == "__main__":
    # 1) Build dataframes
    df_team, df_agent, df_case_price = build_dimensions()
    cal_weeks = build_calendar_weeks()
    df_capacity, df_budget = build_capacity_budget(df_agent, cal_weeks)
    df_wp = build_weekly_perf(df_agent, cal_weeks, df_case_price)

    dfs = {
        "team": df_team,
        "agent": df_agent,
        "case_pricing": df_case_price,
        "calendar_weeks": cal_weeks,
        "capacity_weekly": df_capacity,
        "budget_weekly": df_budget,
        "weekly_perf": df_wp,
    }

    # 2) Parquet local
    for name, df in dfs.items():
        out = FILES / f"{name}.parquet"
        df.to_parquet(out, index=False)
        print(f"💾 Wrote {len(df):,} rows → {out}")

    # 3) Carga a Postgres (si WRITE_DB=1)
    write_postgres(dfs)