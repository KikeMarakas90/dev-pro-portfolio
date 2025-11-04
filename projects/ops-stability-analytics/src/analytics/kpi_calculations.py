import pandas as pd
import numpy as np
from pathlib import Path

def coef_variacion(series: pd.Series) -> float:
    m = series.mean()
    s = series.std(ddof=1)
    return float(s / m) if m != 0 else np.nan

def coef_variacion_mediana(series: pd.Series) -> float:
    # CV basado en mediana: 1.4826 * MAD / mediana
    med = series.median()
    mad = (series - med).abs().median()
    return float(1.4826 * mad / med) if med != 0 else np.nan

def iqr_bounds(series: pd.Series, k: float = 1.5):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k*iqr, q3 + k*iqr

def build_daily(df: pd.DataFrame) -> pd.DataFrame:
    return df.copy()

def build_agent_weekly(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.isocalendar().week.astype(int)
    grp = df.groupby(['agent_id','team_id','week'], as_index=False).agg(
        hours_mean=('productive_hours','mean'),
        cases_mean=('cases_closed','mean')
    )
    return grp

def compute_stability(df_week: pd.DataFrame) -> pd.DataFrame:
    # estabilidad por agente en el periodo completo
    by_agent = df_week.groupby(['agent_id','team_id']).agg(
        cv_hours=('hours_mean', coef_variacion),
        cvm_hours=('hours_mean', coef_variacion_mediana),
        cv_cases=('cases_mean', coef_variacion),
        cvm_cases=('cases_mean', coef_variacion_mediana)
    ).reset_index()

    # cuartiles por equipo
    def quartile(s: pd.Series):
        return pd.qcut(s, 4, labels=[1,2,3,4], duplicates='drop')

    by_agent['quartile_efficiency'] = quartile(by_agent['cv_hours'].fillna(by_agent['cv_hours'].median()))
    return by_agent

def flag_outliers(df_week: pd.DataFrame) -> pd.DataFrame:
    # outliers por agente/semana en horas y casos
    bounds_h = df_week.groupby('team_id')['hours_mean'].apply(iqr_bounds).to_dict()
    bounds_c = df_week.groupby('team_id')['cases_mean'].apply(iqr_bounds).to_dict()

    def is_out_h(row):
        lo, hi = bounds_h[row['team_id']]
        return int(row['hours_mean'] < lo or row['hours_mean'] > hi)

    def is_out_c(row):
        lo, hi = bounds_c[row['team_id']]
        return int(row['cases_mean'] < lo or row['cases_mean'] > hi)

    df_week['out_hours_flag'] = df_week.apply(is_out_h, axis=1)
    df_week['out_cases_flag'] = df_week.apply(is_out_c, axis=1)
    return df_week

if __name__ == "__main__":
    raw = pd.read_csv("data/raw/ops_daily.csv")
    daily = build_daily(raw)
    weekly = build_agent_weekly(daily)
    stability = compute_stability(weekly)
    weekly_flagged = flag_outliers(weekly)

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    stability.to_csv("data/processed/agent_stability.csv", index=False)
    weekly_flagged.to_csv("data/processed/weekly_flags.csv", index=False)

    print("Wrote data/processed/agent_stability.csv and weekly_flags.csv")