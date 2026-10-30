# CLAUDE.md

Proyecto del MAI (Módulo de Aplicaciones Integradoras) de la diplomatura. Base: SEC EDGAR Financial Statement Data Sets. Mentora: Delfina Pons Guisiano. Repo git público: github.com/EbnerLautaro/MAI-Diplodatos (sin `src/zips/`, `src/data/` ni `docs/professor-materials/`, ver `.gitignore`). No hay build ni tests.

**Al empezar una sesión nueva, leer `TODO.md`.** Tiene las tareas pendientes y las decisiones ya tomadas sobre cómo armar el dataset. Cuando el usuario pida anotar algo "en la lista de TODO", agregarlo ahí; marcar `[x]` lo que se termine.

## Estructura

Los nombres de archivos y carpetas van en inglés (el contenido de los documentos, en español).

- `TODO.md`: tareas pendientes del proyecto.
- `src/`: notebooks.
  - Orden de ejecución: `download` → `build_dataset` → `bankruptcy` → `build_panel`.
  - `download.ipynb`: descarga un zip por trimestre en `src/zips/` (2018q1 a 2025q4).
  - `build_dataset.ipynb`: arma el dataset. Genera `src/data/sub.csv` (documentos 10-K, 10-Q y sus enmiendas de salud y energía, con columnas `sector` y `zip`) y `src/data/num.csv` (una versión de cada número, la foto de la base al 31/12/2023; solo en USD).
  - `bankruptcy.ipynb`: fecha de quiebra de cada empresa (8-K con ítem 1.03) con la API `data.sec.gov/submissions`. Guarda todos los 8-K con ítem 1.03 en `src/data/bankruptcy_filings.csv` (caché: si existe, no consulta a la SEC) y la quiebra que empieza dentro de `START`–`END` en `src/data/bankruptcy.csv`.
  - `build_panel.ipynb`: arma `src/data/panel.csv`: una fila por empresa y trimestre calendario 2018Q1–2024Q4, panel no balanceado, columnas en español (conceptos, ratios y `fecha_quiebra`). Una empresa que quiebra deja de tener filas desde el trimestre de la quiebra.
  - `shared/`: código que usan varios notebooks; se importa con `from shared.<módulo> import ...`. `concepts.py` tiene `CONCEPTS` (concepto → tags en orden de prioridad, los de la guía de la mentora).
  - Los notebooks de análisis (sesgo de supervivencia, atraso de presentación, cobertura de tags) se borraron el 2026-10-30 y se rehacen en una etapa posterior. Están en el historial de git.
- `src/zips/<AAAA>q<N>.zip`: un zip por trimestre de **presentación**, no por trimestre del período. Cada zip trae `sub.txt`, `num.txt`, `pre.txt`, `tag.txt` y `readme.htm`.
- `docs/`: `rumbo-mai.pdf` (el rumbo que definió el grupo: objetivos, variables, ratios y requerimientos de la base; **manda sobre cualquier otro documento**), `decisions.md` (decisiones metodológicas del dataset y su porqué; al tomar una decisión nueva, agregarla ahí), `conceptos.md` (notas del usuario) y `sec-edgar-overview.md`.
- Toda decisión que toma el usuario lleva el sufijo `(DECISIÓN TOMADA)` al final de su renglón, en `docs/` y en `TODO.md`. El equipo tiene más personas y el sufijo marca qué decidió el usuario. Una propuesta o un pendiente no lleva el sufijo.
- `docs/professor-materials/`: material de la mentora: `dataset-description.pdf` (consigna), `sec-edgar-guide.docx` (guía de la base, tags y ratios sugeridos) y `sec-edgar-notebook.ipynb` (ejemplo de la Opción B, Colab).
- Las propuestas de los mentores, con las consignas por checkpoint, están en `~/FAMAF/Diplodatos-etc/propuestas-MAI.zip`.

## Entorno

- Entorno pyenv `Diplodatos` (Python 3.14), fijado con `.python-version`. Es el mismo entorno de toda la diplomatura; ver `../CLAUDE.md`.
- Para ejecutar Python sobre los zips desde la terminal: `~/.pyenv/versions/Diplodatos/bin/python -I`.
- Para ejecutar un notebook desde la terminal (desde `src/`): `~/.pyenv/versions/Diplodatos/bin/jupyter nbconvert --to notebook --execute --inplace <notebook>`.

## Datos

- Leer los zips sin descomprimir: `zipfile.ZipFile(z).open("num.txt")` y pasarlo a `pd.read_csv(..., sep="\t", dtype=str)`. `pd.read_csv("x.zip")` falla porque el zip tiene más de un archivo.
- `num.txt` de un trimestre ocupa unos 400 MB descomprimido. En un loop sobre varios zips, filtrar `num` por los `adsh` del sector antes de pasar al zip siguiente.
- La descarga por script necesita `User-Agent` con un email (no se verifica). Sin email la SEC responde 403.

## Guía de estudio

`docs/financial-statements-guide.md` es una guía viva: el usuario pide agregar conceptos a medida que avanza. Solo existe el `.md` (el `.html` y el artefacto se dejaron de usar el 2026-10-20).
## Notebooks

- Los `id` de las celdas siguen el patrón `cell-00`, `cell-01`, `cell-02`, ... (empieza en 0) en el orden en que aparecen (el usuario los ve con la extensión "Notebook Cell Id"). Al agregar o borrar una celda, renumerar todas para que sigan el orden.
