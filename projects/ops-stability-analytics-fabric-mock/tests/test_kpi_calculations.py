# -*- coding: utf-8 -*-
"""
Unit tests for KPI calculations module
Validates robustness of statistical coefficients (CV and CVM).
"""
import pandas as pd
import numpy as np
from src.analytics.kpi_calculations import (
    coef_variacion,
    coef_variacion_mediana,
)

# --------------------------------------------------------------------
# Tests for coeficiente de variación (CV)
# --------------------------------------------------------------------
def test_coef_variacion_linear_series():
    """Debe devolver un valor razonable para una secuencia lineal."""
    s = pd.Series([1, 2, 3, 4, 5])
    cv = coef_variacion(s)
    # Valor teórico aproximado 0.527 → rango seguro
    assert 0.4 < cv < 0.7, f"CV fuera de rango esperado: {cv}"

def test_coef_variacion_with_zero_mean():
    """Debe manejar correctamente series con media cero (retornar NaN)."""
    s = pd.Series([-1, 0, 1])
    cv = coef_variacion(s)
    assert np.isnan(cv), "CV debería ser NaN cuando la media es 0."

# --------------------------------------------------------------------
# Tests for coeficiente de variación basado en mediana (CVM)
# --------------------------------------------------------------------
def test_coef_variacion_mediana_with_outlier():
    """CVM debe ser más robusto que el CV tradicional ante outliers."""
    s = pd.Series([1, 2, 100])  # outlier fuerte
    cv = coef_variacion(s)
    cvm = coef_variacion_mediana(s)
    assert cv > cvm, f"CVM no es menor ante outlier (cv={cv:.3f}, cvm={cvm:.3f})"

def test_coef_variacion_mediana_with_constant_series():
    """CVM de una serie constante debe ser 0."""
    s = pd.Series([5, 5, 5, 5])
    cvm = coef_variacion_mediana(s)
    assert cvm == 0, f"CVM incorrecto para serie constante: {cvm}"