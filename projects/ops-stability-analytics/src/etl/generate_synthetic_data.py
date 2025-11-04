import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)

N_AGENTS = 60
DAYS = 90

agents = [f"AG{str(i).zfill(3)}" for i in range(1, N_AGENTS+1)]
teams = [f"T{(i%6)+1}" for i in range(1, N_AGENTS+1)]

dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=DAYS, freq='D')

rows = []
for a, t in zip(agents, teams):
    base_prod = rng.normal(6.0, 1.0)  # horas productivas promedio/día
    base_cases = rng.normal(18, 4)    # casos cerrados promedio/día
    stability = rng.uniform(0.05, 0.25)  # desviación relativa

    for d in dates:
        hrs = max(0.0, rng.normal(base_prod, base_prod*stability))
        cases = max(0.0, rng.normal(base_cases, base_cases*stability))
        rows.append((d.date().isoformat(), a, t, round(hrs,2), int(cases)))

df = pd.DataFrame(rows, columns=["date","agent_id","team_id","productive_hours","cases_closed"])

out_dir = Path("data/raw")
out_dir.mkdir(parents=True, exist_ok=True)
df.to_csv(out_dir / "ops_daily.csv", index=False)
print(f"Generated {len(df):,} rows -> {out_dir/'ops_daily.csv'}")