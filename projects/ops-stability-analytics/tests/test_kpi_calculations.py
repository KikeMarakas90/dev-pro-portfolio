import pandas as pd
from src.analytics.kpi_calculations import (
    coef_variacion,
    coef_variacion_mediana,
)

def test_coef_variacion_with_linear_data():
    """CV básico: debe ser positivo y razonable para una secuencia lineal."""
    s = pd.Series([1, 2, 3, 4, 5])
    cv = coef_variacion(s)
    # Valor teórico ~0.527. Dejamos margen por diferencias numéricas.
    assert 0.4 < cv < 0.7, f"CV fuera de rango esperado: {cv}"

def test_coef_variacion_mediana_with_outlier():
    """CVM debe ser más robusto ante outliers que el CV estándar."""
    s = pd.Series([1, 2, 100])  # outlier fuerte
    cv = coef_variacion(s)
    cvm = coef_variacion_mediana(s)
    assert cv > cvm, f"CVM no es menor (cv={cv:.3f}, cvm={cvm:.3f})"