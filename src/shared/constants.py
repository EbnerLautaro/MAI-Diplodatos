"""Constantes que comparten los notebooks."""

import pandas as pd

# Trimestres calendario del panel, 2018Q1-2024Q4 (docs/decisions.md, sección 1)
TRIMESTRES = pd.period_range("2018Q1", "2024Q4", freq="Q")
N_TRIMESTRES = len(TRIMESTRES)  # 28

# Trimestres que los gráficos sombrean como COVID (primero y último, inclusive)
COVID = ("2020Q1", "2021Q4")
