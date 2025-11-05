import pandas as pd
from src.analytics.kpi_calculations import build_agent_weekly, flag_outliers

def test_flags_binary_and_notnull():
    # Dataset sintético mínimo con dos agentes en el mismo equipo/semana
    df = pd.DataFrame({
        "date": pd.date_range("2025-01-06", periods=14, freq="D").repeat(2),  # incluye dos semanas ISO
        "agent_id": ["A", "B"] * 14,
        "team_id": ["T1", "T1"] * 14,
        "productive_hours": [5, 6] * 14,
        "cases_closed": [10, 11] * 14,
    })

    weekly = build_agent_weekly(df)
    flagged = flag_outliers(weekly)

    for col in ["out_hours_flag", "out_cases_flag"]:
        assert set(flagged[col].unique()) <= {0, 1}
        assert flagged[col].isna().sum() == 0