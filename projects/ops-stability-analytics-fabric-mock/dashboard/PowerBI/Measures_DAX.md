# Medidas DAX (plantilla)

> Copia/pega y ajusta a tus tablas/columnas.

```DAX
m_Hours Mean =
AVERAGEX (
    VALUES ( 'Fact'[Date] ),
    CALCULATE ( AVERAGE ( 'Fact'[ProductiveHours] ) )
)

m_Cases Mean =
AVERAGEX (
    VALUES ( 'Fact'[Date] ),
    CALCULATE ( AVERAGE ( 'Fact'[CasesClosed] ) )
)

m_CV Hours =
VAR _mean = [m_Hours Mean]
VAR _stdev = STDEVX.P ( VALUES('Fact'[Date]), CALCULATE ( AVERAGE ( 'Fact'[ProductiveHours] ) ) )
RETURN DIVIDE ( _stdev, _mean )

m_CVM Hours =
VAR _med = MEDIANX ( VALUES('Fact'[Date]), CALCULATE ( AVERAGE ( 'Fact'[ProductiveHours] ) ) )
VAR _mad =
    MEDIANX (
        VALUES('Fact'[Date]),
        ABS ( CALCULATE ( AVERAGE ( 'Fact'[ProductiveHours] ) ) - _med )
    )
RETURN DIVIDE ( 1.4826 * _mad, _med )
```

## Top N dinámico por defectos/categorías (ejemplo)
```DAX
m_TopN Flag =
VAR N = SELECTEDVALUE ( 'Parametros'[TopN], 5 )
VAR _tbl =
    ADDCOLUMNS (
        VALUES ( 'Dim'[Categoria] ),
        "__val", [m_Cases Mean]
    )
VAR _rank = RANKX ( _tbl, [__val], , DESC, DENSE )
RETURN IF ( _rank <= N, 1, 0 )
```