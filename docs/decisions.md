# Decisiones metodológicas del dataset

Este documento registra cada decisión de `src/build_dataset.ipynb` y su justificación. Sirve de base para la sección de metodología del informe. Las cifras salen de los zips 2018q1–2024q4, sectores salud y energía.

## 1. Zips descargados: 2018q1 a 2024q4

**Decisión.** Se descargan 28 zips, aunque el período de análisis es 2018–2023. (DECISIÓN TOMADA)

**Por qué.** Cada zip agrupa los documentos por fecha de **presentación**, no por período. El 10-K (informe anual) del año 2023 se presenta entre febrero y marzo de 2024, así que está en el zip 2024q1. Sin los zips de 2024, falta el cuarto trimestre de 2023.

## 2. Sectores por código SIC

**Decisión.** Salud es SIC 8000–8099 y energía es SIC 1300–1399. El SIC (Standard Industrial Classification) sale de la columna `sic` de `sub.txt`. (DECISIÓN TOMADA)

**Por qué.** Son los rangos de la consigna de la Opción 3.

**Empresa que cambia de sector.** Cada empresa tiene un solo sector: el de su documento más reciente por `filed`. Decisión del usuario, 2026-10-26. (DECISIÓN TOMADA)
- Por qué: sin esta regla, una empresa que cambia de SIC cuenta en los dos sectores. Hoy pasa en 1 empresa: American International Holdings Corp. (SIC 1389, energía, hasta 2019Q2; SIC 8000, salud, desde 2019Q4). Cuenta como salud.
- Alternativa descartada: eliminar las empresas con más de un sector. No cambia los sobrevivientes, porque esa empresa no tiene los 24 trimestres.
- Código: `src/survivorship_bias.ipynb`, cell-02.

## 3. Tipos de documento: 10-K, 10-Q y sus enmiendas

**Decisión.** Se conservan `10-K`, `10-Q`, `10-K/A` y `10-Q/A`. Quedan 5.838 10-Q, 1.955 10-K, 143 10-Q/A y 82 10-K/A. (DECISIÓN TOMADA)

**Por qué.**
- El 10-Q es el informe trimestral y el 10-K es el anual. El 10-K hace falta para calcular el cuarto trimestre (ver sección 9).
- Los `/A` son enmiendas. Con la regla de la sección 8 casi nunca reemplazan un valor, pero aportan los números que el original no tenía.
- Los otros formularios (8-K, S-1, 20-F, etc.) no son estados contables trimestrales o anuales de empresas de EE. UU.

## 4. Columnas de `sub.txt` que se eliminan

**Decisión.** Se eliminan `ein`, `former`, `changed`, las 13 columnas de dirección, `countryinc`, `stprinc`, `afs`, `wksi`, `accepted`, `instance`, `detail`, `nciks` y `aciks`. (DECISIÓN TOMADA)

**Por qué.** No aportan al análisis: son datos de contacto, nombres anteriores, la categoría de presentador ante la SEC (`afs`) y detalles técnicos del archivo XBRL (el formato de etiquetas de los estados contables). `filed` **no** se elimina, porque la sección 8 la necesita.

## 5. La empresa se identifica por `cik`

**Decisión.** Toda unión o agrupación por empresa usa `cik` (el identificador de la empresa en la SEC), nunca `name`. (DECISIÓN TOMADA)

**Por qué.** En el período, 88 de 496 empresas cambiaron de nombre, 20 cambiaron el cierre del año fiscal (`fye`) y 1 cambió de SIC. El `cik` no cambia.

## 6. Filtros de `num.txt`

| Filtro | Qué elimina | Por qué |
|---|---|---|
| `segments` vacío | Valores por línea de negocio, región o producto | Solo interesa el total de la empresa. Sin este filtro, el total se mezcla con sus partes. (DECISIÓN TOMADA) |
| `coreg` vacío | Valores de una subsidiaria que presenta en el mismo documento | Solo interesa la empresa consolidada. 28 documentos tienen dos empresas registrantes. (DECISIÓN TOMADA) |
| `version` en `us-gaap/2000` … `us-gaap/2027` | Tags propios de cada empresa | Un tag propio no se puede comparar entre empresas. Es una decisión: la guía de la profesora sugiere buscarlos cuando falta el tag estándar. (DECISIÓN TOMADA) |
| `uom` igual a USD | Cantidades de acciones (`shares`), valores por acción (`USD/shares`) y otras unidades | Los ratios dividen montos en dólares. En el `num.csv` anterior, sin este filtro, eran 57.095 filas. (DECISIÓN TOMADA) |
| `qtrs` de 0 a 4 | Períodos de más de un año (`qtrs` 5, 8 y 12) | Son 36 filas y no sirven para un panel trimestral. (DECISIÓN TOMADA) |
| `value` no vacío | Líneas etiquetadas sin monto | Son 25.683 filas, 5.398 de `CommitmentsAndContingencies` (una línea del balance que por norma no lleva monto). Un vacío no es un cero. (DECISIÓN TOMADA) |

PRECAUCIÓN: los vacíos se eliminan **antes** de elegir la versión (sección 8). Si no, la regla puede elegir una versión vacía y perder una versión con monto. Con la regla anterior (`keep="last"`), este orden recuperó 713 valores. (DECISIÓN TOMADA)

## 7. Clave de un número

**Decisión.** Un número queda definido por `cik`, `tag`, `ddate`, `qtrs` y `uom`. (DECISIÓN TOMADA)

**Por qué.**
- `ddate` es la fecha de fin del período y `qtrs` es su duración en trimestres. Dos filas con el mismo tag pero distinto `ddate` o `qtrs` miden períodos distintos: no son duplicados.
- `uom` es la unidad. Con el filtro de la sección 6 siempre vale USD, así que en la clave no tiene efecto.
- Se usa `cik` y no `adsh` (el identificador del documento), porque el mismo número aparece en varios documentos de la empresa.

## 8. Versión de cada número: la primera publicada

**Decisión.** Cuando un número aparece en varios documentos, se conserva la **primera versión publicada**. El código ordena por `["filed", "form"]` y aplica `drop_duplicates(KEY, keep="first")`. (DECISIÓN TOMADA)

**Por qué.**
- El objetivo final es un modelo que predice. Al predecir el próximo trimestre solo se conoce lo que ya se publicó, no las correcciones futuras.
- Entrenar con valores corregidos introduce sesgo de anticipación (look-ahead bias): el modelo usa información que en esa fecha no existía y parece mejor de lo que es.
- Escala del problema: en una prueba, el 6,4% de los números difiere entre la primera y la última versión. Las enmiendas llegan con una mediana de 105 días de atraso. En 57 de 133 pares original-enmienda, `NetIncomeLoss` cambia.

**Desempate.** Si dos documentos tienen el mismo `filed`, `form` desempata: `"10-Q"` va antes que `"10-Q/A"` en orden alfabético, así que gana el original. (DECISIÓN TOMADA)

**`filed` es la fecha en que se conoció el número.** Esta columna queda en `num.csv`. Al armar features para predecir en la fecha t, solo se usan filas con `filed` anterior a t. El `ddate` no alcanza. Por ejemplo, el 10-K de 2020 se presenta entre 60 y 90 días después del 31 de diciembre. Además, una empresa nueva presenta comparativos de años anteriores con `ddate` viejo y `filed` nuevo. (DECISIÓN TOMADA)

**Limitaciones.**
- Es una aproximación. Lo exacto es "el último valor conocido en la fecha t", que puede ser una enmienda si llegó antes de t. Para un horizonte de un trimestre, casi siempre coincide con la primera versión.
- Cuando una empresa reclasifica cuentas (operaciones discontinuadas, norma de arrendamientos ASC 842 en 2019), la primera versión no se corrige. La serie muestra un salto que no es económico. Ese salto también existió para el mercado, así que es correcto para el modelo. En el EDA (análisis exploratorio) hay que explicarlo cuando aparezca.

**Historial.** Primero se eligió la última versión (`keep="last"`), para tener los valores corregidos. El 2026-10-20 se cambió a la primera versión por el objetivo predictivo. Se usa un solo dataset en todo el proyecto, también en el M1, para que el EDA describa los mismos datos que usa el modelo.

## 9. Los acumulados se conservan hasta calcular los trimestres

**Decisión.** `num.csv` conserva `qtrs` 0, 1, 2, 3 y 4. Los acumulados se eliminan recién en el paso que calcula los valores trimestrales (pendiente). (DECISIÓN TOMADA)

**Por qué.**
- El 10-K trae el año (`qtrs=4`), no el cuarto trimestre. Solo el 26% de los `NetIncomeLoss` anuales tiene un `qtrs=1` del cuarto trimestre. El cuarto trimestre se calcula como año menos 9 meses.
- En los 10-Q, el flujo de efectivo viene solo acumulado. De 2.500 flujos operativos anuales, solo 3 tienen el cuarto trimestre. Los trimestres se calculan por diferencia entre acumulados.
- No se suman trimestres para obtener el año: el valor anual del 10-K está auditado y los trimestres no.

## 10. ROA y ROE: flujo trimestral, sin anualizar

**Decisión.** El ROA y el ROE usan la ganancia del trimestre (`qtrs=1`). No se anualiza (× 4) ni se usan los últimos 12 meses (TTM, trailing twelve months). Decisión del usuario, 2026-10-20. (DECISIÓN TOMADA)

**Por qué.**
- Todo el panel usa la misma regla, así que las comparaciones entre empresas y entre trimestres son válidas.
- Es la regla de la guía de la profesora: `qtrs=1` para resultados y `qtrs=0` para balance.
- No pierde trimestres. El TTM necesita los 4 trimestres anteriores, y los zips empiezan en 2018q1.
- Es reversible. El TTM es la suma móvil de 4 valores trimestrales, así que se calcula después si hace falta.

**Limitaciones.**
- El ROA trimestral es unas 4 veces menor que el anual. No se compara directamente con la literatura, que usa valores anuales.
- La estacionalidad queda en el ratio. El EDA y el modelo la tienen que tener en cuenta, por ejemplo con una variable del trimestre del año.
- El cuarto trimestre no viene con `qtrs=1`. Sale de la resta año menos 9 meses (sección 9).

**Sigue pendiente.** La fecha del saldo (cierre o promedio) y el tratamiento del patrimonio negativo (ver `ratios.md`, ROE).

## 11. Alineación a trimestre calendario

**Decisión.** Cada número va al trimestre calendario que contiene más meses de su trimestre fiscal. En código: restar un mes al `ddate` y tomar su trimestre. Un trimestre fiscal que cierra el 31 de enero (noviembre, diciembre y enero) va al cuarto trimestre del año anterior. Decisión del usuario, 2026-10-22. (DECISIÓN TOMADA)

**Paso previo.** Se eliminan las fechas fuera del calendario fiscal de la empresa: los meses de cierre de sus documentos (`sub.period`), módulo 3. Así se eliminan subperíodos, por ejemplo los de una empresa que sale de una quiebra (Gulfport Energy, 2021). Son 3.052 filas.

El código está en `src/shared/align.py` y la explicación paso a paso en `src/panel_coverage.ipynb`.

**Por qué.**
- El panel compara empresas en la misma fila. La regla elige el trimestre calendario que más se superpone con el trimestre fiscal: 2 de 3 meses.
- La alternativa era el trimestre que contiene el `ddate` (enero va al primer trimestre). Se superpone en 1 solo mes.
- Para el año fiscal, Compustat (la base contable más usada en finanzas) usa una regla equivalente: un año que termina entre enero y mayo se asigna al año calendario anterior.

**Cambio propuesto (2026-10-27).** `src/build_panel.ipynb` (paso 4) reemplaza el paso previo: conserva solo las fechas de cierre de los documentos de la empresa (`sub.period`). El filtro módulo 3 no resuelve a Sustainable Projects, que cambió su cierre de mayo a diciembre y tiene dos calendarios.

**Alcance.** En el panel, 3 de 62 empresas cierran fuera de calendario. Las que cierran en febrero, mayo, agosto y noviembre (Norris Industries y Cryo-Cell) tienen el mismo trimestre con las dos reglas. La regla solo cambia a Enzo Biochem, que cierra en enero, abril, julio y octubre. Ninguna empresa del panel tiene choques (dos fechas en el mismo trimestre).

**Limitación.** La fila de un trimestre puede incluir un mes posterior: la fila 2018Q4 de Enzo Biochem incluye enero de 2019. Para el modelo, `filed` sigue siendo la fecha en que se conoció el número (sección 8).

## 12. Decisiones pendientes

Están en `TODO.md`:
- Cálculo del cuarto trimestre y de los flujos trimestrales.
- Si Riley Exploration Permian (antes Tengasco Inc) queda en el panel: probable fusión inversa en 2021.
- Cuántas empresas por sector, si el criterio deja más de 30.
- Tratamiento de outliers. En un panel balanceado no se eliminan filas; se recortan los extremos (winsorizar) o se marcan.

Ya decidido:
- El mapa de conceptos a tags es la tabla de la mentora (`professor-materials/sec-edgar-guide.docx`, sección 4), sin construcciones. Reemplaza a `shared/concepts.py`. Decisión del grupo, 2026-10-27. Código: `src/build_panel.ipynb`, cell-05. (DECISIÓN TOMADA)
- Reemplazado el 2026-10-27: el mapa de conceptos a tags es `shared/concepts.py`, con su orden de prioridad. La justificación está en `src/concepts_justification.ipynb` y en `ratios.md`. (DECISIÓN TOMADA)
- Entran al panel las empresas con todos los conceptos (reportados o construidos) en los 24 trimestres 2018–2023. Es un panel balanceado, y eso implica sesgo de supervivencia. (DECISIÓN TOMADA)
- El orden de `concepts.py` se aplica en cada trimestre (regla A): en cada empresa, concepto y trimestre se usa el primer tag con valor. Una empresa puede cambiar de tag entre trimestres. Decisión del usuario, 2026-10-22. (DECISIÓN TOMADA)
  - Por qué: en 26 de los 35 cambios de tag del panel, los valores coinciden. Con un tag fijo por empresa (regla B), una empresa que cambió de tag necesita una excepción o queda afuera del panel. No se midió cuántas.
  - Condición: los valores trimestrales se calculan por tag (cuarto trimestre y flujos acumulados) y el tag se elige después. Así una resta nunca mezcla dos tags, como pasaría en Houston American Energy. (DECISIÓN TOMADA)

## Relación con el checklist de la profesora

La sección 9 de `professor-materials/sec-edgar-guide.docx` lista las decisiones a justificar.

| Pregunta del checklist | Sección |
|---|---|
| ¿Qué tipo de reporte usaron? | 3 |
| ¿Qué tag eligieron para cada variable? | 12 y `ratios.md` |
| ¿Filtraron por `coreg`? | 6 |
| ¿Usaron `qtrs=4` para resultados y `qtrs=0` para balance? | 9 y 10 |
| ¿Cómo manejaron el desfasaje entre cierre y presentación? | 8 |
| ¿Qué criterio usaron para los outliers? | 12 (pendiente) |
