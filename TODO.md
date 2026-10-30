# TODO

El rumbo del grupo está en `docs/rumbo-mai.pdf` y manda sobre todo lo demás. Cada decisión tomada se documenta, con su porqué, en `docs/decisions.md`. Las tareas terminadas antes del 2026-10-30 están en el historial de git.

## Pipeline (rumbo, 2026-10-30)

- [x] Borrar los notebooks de análisis, `docs/ratios.md` y `docs/ACLARACIONES.md`. Se rehacen en una etapa posterior. (DECISIÓN TOMADA)
- [x] `download.ipynb`: zips hasta 2025q4, para el período 2018Q1–2024Q4. `decisions.md`, sección 1. (DECISIÓN TOMADA)
- [x] `build_dataset.ipynb`: 10-K, 10-Q y sus `/A`, sin 8-K. `decisions.md`, sección 3. (DECISIÓN TOMADA)
- [x] `build_dataset.ipynb`: versión de cada número = foto de la base al 31/12/2023 (la última hasta el corte; si no hay, la primera después). `decisions.md`, sección 8. (DECISIÓN TOMADA)
- [x] `concepts.py`: `ProfitLoss` como alternativo del resultado neto, caja y costo de ventas (para construir la ganancia bruta). `decisions.md`, sección 12. (DECISIÓN TOMADA)
- [x] `bankruptcy.ipynb`: quiebras hasta el 31/12/2025 (un año de horizonte después del panel); guarda `data/bankruptcy.csv`.
- [x] `build_panel.ipynb`: panel no balanceado con las empresas con datos en 2018Q1, columnas en español, 8 ratios en fracción y corte desde el trimestre de la quiebra. `decisions.md`, secciones 12 y 13. (DECISIÓN TOMADA)

## Pendientes

- [ ] **Outliers.** Hay ratios extremos (endeudamiento de hasta 100.000, márgenes de −100.000) en empresas con activos o ingresos casi nulos. Decidir si se recortan (winsorizar) o se marcan.
- [ ] **ROA y ROE:** decidir la fecha del saldo (cierre o promedio) y qué hacer con el patrimonio negativo (ejemplo: HCA).
- [ ] **Sesgo de anticipación** de la regla de enmiendas (`decisions.md`, sección 8): medir con `fecha_presentacion` cuántas filas de 2018–2023 se conocieron después del trimestre siguiente.
- [ ] **Salidas que no son quiebra.** Una empresa sin `fecha_quiebra` que deja de tener filas salió por compra o dejó de presentar. Decidir si se identifican (8-K ítem 2.01, Form 15 o Form 25).
- [ ] Revisar Riley Exploration Permian (antes Tengasco Inc, probable fusión inversa en 2021) y decidir si queda en el panel.
- [ ] Rehacer los análisis borrados que hagan falta (sesgo de supervivencia, atraso de presentación, cobertura de tags).
- [ ] Borrar `src/zips/2018q1/` (un zip descomprimido) si ya no se usa.
- [ ] Preguntar a la mentora: si "deuda total" es `Liabilities` o deuda financiera, el formato de la entrega y si se alinea por trimestre calendario.
