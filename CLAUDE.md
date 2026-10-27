# CLAUDE.md

Proyecto del MAI (Módulo de Aplicaciones Integradoras) de la diplomatura. Base: SEC EDGAR Financial Statement Data Sets. Mentora: Delfina Pons Guisiano. Repo git público: github.com/EbnerLautaro/MAI-Diplodatos (sin `src/zips/`, `src/data/` ni `docs/professor-materials/`, ver `.gitignore`). No hay build ni tests.

**Al empezar una sesión nueva, leer `TODO.md`.** Tiene las tareas pendientes y las decisiones ya tomadas sobre cómo armar el dataset. Cuando el usuario pida anotar algo "en la lista de TODO", agregarlo ahí; marcar `[x]` lo que se termine.

## Estructura

Los nombres de archivos y carpetas van en inglés (el contenido de los documentos, en español).

- `TODO.md`: tareas pendientes del proyecto.
- `src/`: notebooks.
  - `download.ipynb`: descarga un zip por trimestre en `src/zips/` (2018q1 en adelante).
  - `build_dataset.ipynb`: arma el dataset. Genera `src/data/sub.csv` (documentos 10-K, 10-Q y sus enmiendas de salud y energía, con columnas `sector` y `zip`) y `src/data/num.csv` (primera versión publicada de cada número, solo en USD).
  - `survivorship_bias.ipynb`: sesgo de supervivencia. Cuenta las empresas con presentación en cada trimestre 2018–2023, cuántas tienen los 24 trimestres y por qué quedan afuera las demás. Lee `data/sub.csv`.
  - `filing_delay.ipynb`: atraso entre `period` y `filed`. Justifica que los zips 2018q1–2024q4 alcanzan para los períodos 2018–2023. Lee `data/sub.csv`.
  - `mentor_concepts.ipynb`: cuántos sobrevivientes tienen los 9 conceptos en los 24 trimestres con tres opciones acumulativas: tags de la mentora, + `concepts.py`, + nuestras construcciones. Lee `data/*.csv`.
  - `build_panel.ipynb`: arma `src/data/panel.csv` (una fila por empresa y trimestre calendario, 9 conceptos) con los sobrevivientes y los tags de la mentora. Calcula los flujos trimestrales. Lee `data/*.csv`.
  - `concepts_justification.ipynb`: justifica con datos cada lista de `CONCEPTS` y cada número de `docs/ratios.md` (tag de la línea del estado, aporte de cada tag, orden con el detalle de ingresos, alternativos de la profesora, construcciones). Lee `pre.txt` de los zips.
  - `shared/`: código que usan varios notebooks; se importa con `from shared.<módulo> import ...`. `concepts.py` tiene `CONCEPTS` (concepto → tags en orden de prioridad). Quedó obsoleto el 2026-10-27: el panel usa los tags de la mentora.
  - `exploration.ipynb`: exploración del usuario. Todavía lee `tmp/*.txt`, una carpeta que ya no existe.
- `src/zips/<AAAA>q<N>.zip`: un zip por trimestre de **presentación**, no por trimestre del período. Cada zip trae `sub.txt`, `num.txt`, `pre.txt`, `tag.txt` y `readme.htm`.
- `docs/`: `financial-statements-guide.md` (guía de estudio), `decisions.md` (decisiones metodológicas del dataset y su porqué; al tomar una decisión nueva, agregarla ahí) `ratios.md` (qué mide cada ratio, tags de cada concepto y cómo construir un concepto que falta) y `ACLARACIONES.md` (explicaciones puntuales que pide el usuario, por ejemplo `inpth`).
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
