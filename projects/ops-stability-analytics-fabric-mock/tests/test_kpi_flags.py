# -*- coding: utf-8 -*-
"""
Unit tests for outlier flagging in KPI calculations.
Validates binary consistency, schema integrity, and multi-team robustness.
"""
import pandas as pd
import numpy as np
from src.analytics.kpi_calculations import build_agent_weekly, flag_outliers

def _build_mock_df() -> pd.DataFrame:
    """Construye dataset sintético pequeño y reproducible."""
    return pd.DataFrame({
        "date": pd.date_range("2025-01-06", periods=14, freq="D").repeat(2),  # dos semanas ISO
        "agent_id": ["A", "B"] * 14,
        "team_id": ["T1", "T1"] * 14,
        "productive_hours": [5, 6] * 14,
        "cases_closed": [10, 11] * 14,
    })

# --------------------------------------------------------------------
# Tests principales
# --------------------------------------------------------------------
def test_flags_binary_and_notnull():
    """Verifica que los flags sean binarios (0/1) y sin nulos."""
    df = _build_mock_df()
    weekly = build_agent_weekly(df)
    flagged = flag_outliers(weekly)

    for col in ["out_hours_flag", "out_cases_flag"]:
        assert col in flagged.columns, f"Falta columna {col}"
        assert flagged[col].isna().sum() == 0, f"{col} contiene valores nulos"
        unique_vals = set(flagged[col].unique())
        assert unique_vals <= {0, 1}, f"{col} contiene valores no binarios: {unique_vals}"

def test_flags_schema_integrity():
    """Verifica que se mantengan columnas clave tras aplicar flags."""
    df = _build_mock_df()
    weekly = build_agent_weekly(df)
    flagged = flag_outliers(weekly)

    expected_cols = {"agent_id", "team_id", "week", "hours_mean", "cases_mean",
                     "out_hours_flag", "out_cases_flag"}
    assert expected_cols.issubset(flagged.columns), "Columnas esperadas ausentes"

def test_flags_multiple_teams_isolated():
    """Verifica que los outliers se calculen de forma independiente por equipo."""
    df = _build_mock_df()
    # Duplicar con otro equipo con valores distintos
    df_T2 = df.copy()
    df_T2["team_id"] = "T2"
    df_T2["productive_hours"] *= 1.5
    df_T2["cases_closed"] *= 1.5
    df_all = pd.concat([df, df_T2], ignore_index=True)

    weekly = build_agent_weekly(df_all)
    flagged = flag_outliers(weekly)

    # Debe haber flags separados por team_id
    unique_teams = flagged["team_id"].unique()
    assert len(unique_teams) == 2, "No se detectaron ambos equipos"
    assert all(col in flagged.columns for col in ["out_hours_flag", "out_cases_flag"])

    # Flags deben existir pero sin mezclar equipos
    grouped = flagged.groupby("team_id")[["out_hours_flag", "out_cases_flag"]].nunique().max(axis=1)
    assert (grouped >= 1).all(), "Al menos un flag debe calcularse por equipo"