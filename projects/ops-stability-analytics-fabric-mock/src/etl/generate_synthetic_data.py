# -*- coding: utf-8 -*-
"""
Synthetic Daily Data Generator
Fabric-ready compatible. Supports .env configuration and CLI overrides.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv

# --------------------------------------------------------------------
# Configuración global
# --------------------------------------------------------------------
load_dotenv()

DEFAULT_AGENTS = int(os.getenv("N_AGENTS", 60))
DEFAULT_DAYS = int(os.getenv("N_DAYS", 90))
DEFAULT_SEED = int(os.getenv("SEED", 42))
DEFAULT_FORMAT = os.getenv("OUT_FORMAT", "parquet").lower()
DEFAULT_OUTDIR = Path(os.getenv("RAW_PATH", "lakehouse_sim/Files/raw"))

# --------------------------------------------------------------------
# Generador base
# --------------------------------------------------------------------
def generate(n_agents: int, days: int, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    agents = [f"AG{str(i).zfill(3)}" for i in range(1, n_agents + 1)]
    teams  = [f"T{(i % 6) + 1}" for i in range(1, n_agents + 1)]
    dates  = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days, freq="D")

    rows = []
    for a, t in zip(agents, teams):
        base_prod  = rng.normal(6.0, 1.0)   # horas promedio por día
        base_cases = rng.normal(18, 4)      # casos promedio por día
        stability  = rng.uniform(0.05, 0.25)
        for d in dates:
            hrs   = max(0.0, rng.normal(base_prod,  base_prod  * stability))
            cases = max(0.0, rng.normal(base_cases, base_cases * stability))
            rows.append((d.date().isoformat(), a, t, round(float(hrs), 2), int(cases)))

    return pd.DataFrame(
        rows,
        columns=["date", "agent_id", "team_id", "productive_hours", "cases_closed"]
    )

# --------------------------------------------------------------------
# Main CLI handler
# --------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic ops data for Athera/Fabric pipeline")
    parser.add_argument("--agents", type=int, default=DEFAULT_AGENTS, help="Number of agents")
    parser.add_argument("--days",   type=int, default=DEFAULT_DAYS,   help="Number of days to simulate")
    parser.add_argument("--seed",   type=int, default=DEFAULT_SEED,   help="Random seed")
    parser.add_argument("--format", choices=["parquet", "csv"], default=DEFAULT_FORMAT, help="Output format")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR, help="Output directory path")
    args = parser.parse_args()

    df = generate(args.agents, args.days, args.seed)
    args.outdir.mkdir(parents=True, exist_ok=True)

    if args.format == "csv":
        out = args.outdir / "ops_daily.csv"
        df.to_csv(out, index=False)
    else:
        out = args.outdir / "ops_daily.parquet"
        df.to_parquet(out, index=False)

    print(f"✅ Generated {len(df):,} rows → {out}")

# --------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------
if __name__ == "__main__":
    main()
