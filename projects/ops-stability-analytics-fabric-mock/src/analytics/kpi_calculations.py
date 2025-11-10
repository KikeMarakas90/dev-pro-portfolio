# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

__all__ = [
    "coef_variacion",
    "coef_variacion_mediana",
    "iqr_bounds",
    "build_daily",
    "build_agent_weekly",
    "compute_stability",
    "flag_outliers",
]

# -----------------------------
# Métricas estadísticas (APIs)
# -----------------------------
def coef_variacion(series: pd.Series) -> float:
    """Coeficiente de variación basado en media (std/mean)."""
    m = series.mean()
    s = series.std(ddof=1)
    return float(s / m) if m != 0 else np.nan

def coef_variacion_mediana(series: pd.Series) -> float:
    """Coeficiente de variación robusto basado en mediana y MAD."""
    med = series.median()
    mad = (series - med).abs().median()
    return float(1.4826 * mad / med) if med != 0 else np.nan

def iqr_bounds(series: pd.Series, k: float = 1.5) -> tuple[float, float]:
    """Límites inferior/superior por IQR para detección de outliers."""
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return (q1 - k * iqr, q3 + k * iqr)

# -----------------------------
# Transformaciones intermedias
# -----------------------------
def build_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza tipos base de la capa diaria (evita SettingWithCopy)."""
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"])
    return out

def build_agent_weekly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega métricas semanales por agente/equipo.
    Incluye iso_year + iso_week y deja alias 'week' para compatibilidad.
    """
    out = df.copy()
    iso = out["date"].dt.isocalendar()
    out["iso_year"] = iso.year.astype(int)
    out["iso_week"] = iso.week.astype(int)

    grp = out.groupby(
        ["agent_id", "team_id", "iso_year", "iso_week"], as_index=False
    ).agg(
        hours_mean=("productive_hours", "mean"),
        cases_mean=("cases_closed", "mean"),
    )

    # 👉 alias retro-compatible que tu test espera
    grp["week"] = grp["iso_week"]
    return grp

def compute_stability(df_week: pd.DataFrame) -> pd.DataFrame:
    """Calcula CV/CVM de horas y casos por agente; asigna cuartil de estabilidad."""
    by_agent = df_week.groupby(["agent_id", "team_id"]).agg(
        cv_hours=("hours_mean", coef_variacion),
        cvm_hours=("hours_mean", coef_variacion_mediana),
        cv_cases=("cases_mean", coef_variacion),
        cvm_cases=("cases_mean", coef_variacion_mediana),
    ).reset_index()

    # Cuartiles (1..4). Menor CV = más estable.
    base = by_agent["cv_hours"]
    # Si hay pocos valores únicos, qcut puede fallar; usamos duplicates='drop' y cast seguro.
    by_agent["quartile_efficiency"] = pd.qcut(
        base.fillna(base.median()),
        4,
        labels=[1, 2, 3, 4],
        duplicates="drop",
    )
    # Cast opcional a int cuando el binning conserva 4 bandas
    if by_agent["quartile_efficiency"].notna().any():
        try:
            by_agent["quartile_efficiency"] = by_agent["quartile_efficiency"].astype("int64")
        except Exception:
            # Si se reduce el número de bins, dejamos categoría/objeto como está
            pass

    return by_agent

def flag_outliers(df_week: pd.DataFrame) -> pd.DataFrame:
    """
    Marca outliers por equipo + año ISO + semana ISO (IQR).
    Conserva alias 'week' para compatibilidad.
    """
    out = df_week.copy()

    def flag_series(s: pd.Series) -> pd.Series:
        lo, hi = iqr_bounds(s)
        return (s.lt(lo) | s.gt(hi)).astype(int)

    keys = ["team_id", "iso_year", "iso_week"]
    out["out_hours_flag"] = out.groupby(keys)["hours_mean"].transform(flag_series)
    out["out_cases_flag"] = out.groupby(keys)["cases_mean"].transform(flag_series)

    # 👉 garantiza presencia de 'week'
    if "week" not in out.columns:
        out["week"] = out["iso_week"]

    return out

# -----------------------------
# Ejecución como script (E2E)
# -----------------------------
if __name__ == "__main__":
    lh_root = Path("lakehouse_sim")
    raw_parquet = lh_root / "Files" / "raw" / "ops_daily.parquet"

    if raw_parquet.exists():
        raw = pd.read_parquet(raw_parquet)
    else:
        raw_csv = Path("data/raw/ops_daily.csv")
        if not raw_csv.exists():
            raise FileNotFoundError(
                f"No se encontró {raw_parquet} ni {raw_csv}. "
                "Ejecuta primero la generación de datos."
            )
        raw = pd.read_csv(raw_csv)

    daily = build_daily(raw)
    weekly = build_agent_weekly(daily)
    stability = compute_stability(weekly)
    weekly_flagged = flag_outliers(weekly)

    tables_dir = lh_root / "Tables"
    tables_dir.mkdir(parents=True, exist_ok=True)

    out_agent = tables_dir / "agent_stability.parquet"
    out_weekly = tables_dir / "weekly_flags.parquet"

    stability.to_parquet(out_agent, index=False)
    weekly_flagged.to_parquet(out_weekly, index=False)

    print(f"✅ Wrote {len(stability)} rows → {out_agent}")
    print(f"✅ Wrote {len(weekly_flagged)} rows → {out_weekly}")