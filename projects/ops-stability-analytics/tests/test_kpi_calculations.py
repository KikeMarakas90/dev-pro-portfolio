import pandas as pd
from src.analytics.kpi_calculations import coef_variacion, coef_variacion_mediana

def test_cv_basic():
    s = pd.Series([1,2,3,4,5])
    cv = coef_variacion(s)
    assert 0.4 < cv < 0.7  # rango aproximado

def test_cvm_basic():
    s = pd.Series([1,2,100])  # outlier fuerte
    cv = coef_variacion(s)
    cvm = coef_variacion_mediana(s)
    assert cv > cvm  # CVM debe ser más robusto y por lo general menor con outliers