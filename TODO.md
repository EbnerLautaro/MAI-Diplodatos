# TODO

## Dataset (`src/build_dataset.ipynb`)

Cada decisión tomada se documenta, con su porqué, en `docs/decisions.md`.

- [x] **Leer `num.txt` de cada zip** y quedarse con las filas de los `adsh` de `data/sub.csv`, con `segments` vacío, `coreg` vacío, `qtrs` de 0 a 4, `uom` igual a USD y `value` no vacío. Los vacíos se eliminan antes de elegir la versión: si no, la regla de versión puede quedarse con una versión vacía. (DECISIÓN TOMADA)
- [x] **Quedarse con la primera versión publicada de cada número.** `build_dataset.ipynb` ordena por `["filed", "form"]` y conserva la primera fila por `cik`, `tag`, `ddate`, `qtrs`, `uom` (`keep="first"`). Decisión del usuario (2026-10-20): el objetivo es predecir, y al predecir no se conocen las correcciones futuras. Reemplaza a `keep="last"`. Justificación en `docs/decisions.md`, sección 8. (DECISIÓN TOMADA)
  - [x] Ejecutar `build_dataset.ipynb` de nuevo para regenerar `data/num.csv` con `keep="first"`. Regenerado de nuevo con el filtro `uom == "USD"` (827.929 filas).
  - Al armar features: usar `filed` como fecha en que se conoció el número, no `ddate`.
- [x] **Filtrar `form`** a `10-K`, `10-Q`, `10-K/A` y `10-Q/A`. Los `/A` son enmiendas; con `keep="first"` aportan los números que el original no tiene. (DECISIÓN TOMADA)
- [ ] **Columnas de `sub` que se conservan:** `adsh`, `cik`, `name`, `sic`, `form`, `period`, `fy`, `fp`, `fye`, `filed`, `prevrpt`, `afs`, más `sector` y `zip`.
  - `filed` se conserva siempre: es la fecha en que se conoció cada número.
  - `afs` (tamaño de la empresa en bolsa) se conserva solo si se usa como feature o en el EDA.
- [x] **Elegir los ratios:** margen operativo, margen neto, ROA, ROE, endeudamiento, liquidez corriente y FCO / ingresos. Se descartan margen bruto e I+D / ingresos por baja cobertura en energía. Explicación en `docs/ratios.md`. (DECISIÓN TOMADA)
- [x] **Mapa de conceptos a tags.** `CONCEPTS` (`shared/concepts.py`), `mapa`.
  - [x] El orden de `concepts.py` se respeta, con `Revenues` primero en los ingresos y el flujo operativo total primero. La justificación está en `concepts_justification.ipynb`. (DECISIÓN TOMADA)
  - [x] Construcciones de `docs/ratios.md` implementadas en `build_panel.ipynb` (paso 4).
- [ ] **ROA y ROE:** decidir la fecha del saldo (cierre o promedio) y qué hacer con el patrimonio negativo (ejemplo: HCA).
  - [x] Período del flujo: trimestral (`qtrs=1`), sin anualizar. Decisión del usuario (2026-10-20), en `docs/decisions.md`, sección 10. (DECISIÓN TOMADA)
- [x] **Valores trimestrales** en `build_panel.ipynb` (paso 2): `qtrs=1` si existe; si no, el acumulado de k trimestres menos el de k − 1 que termina 3 meses antes (incluye el cuarto trimestre = año menos 9 meses).
- [x] **Alinear a trimestre calendario** con `ddate`, no con `fy`/`fp`: el trimestre con más meses del trimestre fiscal. Código en `shared/align.py`; `docs/decisions.md`, sección 11. (DECISIÓN TOMADA)
- [x] **Tag por trimestre (regla A):** el primer tag de `concepts.py` con valor en cada trimestre. Los valores trimestrales se calculan por tag y el tag se elige después. `docs/decisions.md`, sección 12. (DECISIÓN TOMADA)
  - [ ] Revisar Riley Exploration Permian (antes Tengasco Inc, probable fusión inversa en 2021) y decidir si queda en el panel.
- [ ] **Paso atrás (reunión de grupo, 2026-10-26).** Se borraron los notebooks del panel y de cobertura, `shared/align.py` y `data/panel.csv`. Los ítems que los nombran quedan como registro de lo hecho.
  - [ ] Investigar el sesgo de supervivencia.
  - [x] Comparar nuestro `concepts.py` con los conceptos de la mentora (`mentor_concepts.ipynb`).
  - [x] El panel usa solo los tags de la mentora. `concepts.py` y nuestras construcciones quedan obsoletos por ahora. Decisión del grupo, 2026-10-27. (DECISIÓN TOMADA)
  - [x] Panel armado de nuevo: `build_panel.ipynb` genera `data/panel.csv` con 23 empresas de energía y 21 de salud.
  - [ ] Revisar el filtro de fechas de `build_panel.ipynb` (paso 4): usa los cierres de los documentos en lugar del filtro módulo 3 de `docs/decisions.md`, sección 11.
- [ ] **Elegir las empresas:** 20 a 30 por sector (40 a 60 en total). Las elige el alumno, no la mentora. Documentar el sesgo de supervivencia.
  - [x] Criterio: entran las empresas con todos los conceptos de `concepts.py` (reportados o construidos) en los 24 trimestres 2018–2023. Se aplica como filtro sobre el panel ya armado. (DECISIÓN TOMADA)
  - [x] Panel armado: `build_panel.ipynb` genera `data/panel.csv` con 69 empresas de energía y 37 de salud.
  - Supera el máximo de 30 por sector de la consigna. Se supone que la mentora lo acepta; falta confirmarlo.

## Otros

- [ ] `src/exploration.ipynb` lee `tmp/*.txt`, que ya no existe. Cambiarlo para leer desde `zips/`.
- [ ] Borrar `src/zips/2018q1/` (un zip descomprimido) si ya no se usa.
- [ ] Preguntar a la mentora: si "deuda total" es `Liabilities` o deuda financiera, el formato de la entrega, si se alinea por trimestre calendario y si se aceptan más de 30 empresas por sector.
