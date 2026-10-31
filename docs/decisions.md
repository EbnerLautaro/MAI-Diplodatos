# Decisiones metodológicas del dataset

Este documento registra cada decisión de `src/02_build_dataset.ipynb` y `src/04_build_panel.ipynb` y su justificación. Sirve de base para la sección de metodología del informe. El rumbo del grupo (`docs/rumbo-mai.pdf`) manda sobre este documento: si chocan, gana el rumbo. Algunas cifras de abajo son de la versión anterior del dataset (zips 2018q1–2024q4, sin enmiendas) y hay que recalcularlas.

## 1. Período 2018Q1–2024Q4 y zips 2018q1 a 2025q4

**Decisión.** El período de análisis es 2018Q1–2024Q4 (`docs/rumbo-mai.pdf`). Se descargan 32 zips, hasta 2025q4. (DECISIÓN TOMADA)

**Por qué.** Cada zip agrupa los documentos por fecha de **presentación**, no por período. El 10-K (informe anual) del año 2024 se presenta entre febrero y marzo de 2025, así que está en el zip 2025q1. Sin los zips de 2025, falta el cuarto trimestre de 2024.

**Historial.** Hasta el 2026-10-30 el período era 2018–2023, con zips hasta 2024q4.

## 2. Sectores por código SIC

**Decisión.** Salud es SIC 8000–8099 y energía es SIC 1300–1399. En `sub.csv` la columna `sector` vale `salud` o `energia`. El SIC (Standard Industrial Classification) sale de la columna `sic` de `sub.txt`. (DECISIÓN TOMADA)

**Por qué.** Son los rangos de la consigna de la Opción 3.

**Empresa que cambia de sector.** Cada empresa tiene un solo sector: el de su documento más reciente por `filed`. Decisión del usuario, 2026-10-26. (DECISIÓN TOMADA)
- Por qué: sin esta regla, una empresa que cambia de SIC cuenta en los dos sectores. Hoy pasa en 1 empresa: American International Holdings Corp. (SIC 1389, energía, hasta 2019Q2; SIC 8000, salud, desde 2019Q4). Cuenta como salud.
- Alternativa descartada: eliminar las empresas con más de un sector. No cambia los sobrevivientes, porque esa empresa no tiene los 24 trimestres.
- Código: `src/04_build_panel.ipynb`, paso 1.

## 3. Tipos de documento: 10-K, 10-Q y sus enmiendas

**Decisión.** Se conservan `10-K`, `10-Q`, `10-K/A` y `10-Q/A`. No se usan los 8-K de los zips. (DECISIÓN TOMADA)

**Por qué.**
- El 10-Q es el informe trimestral y el 10-K es el anual. El 10-K hace falta para calcular el cuarto trimestre (ver sección 9).
- Los `/A` son enmiendas. El rumbo acepta las presentadas hasta el 31/12/2023 (sección 8).
- Los 8-K de los zips (unos 2 por trimestre en estos sectores) son comunicados con cifras, no estados contables. Si entraran, una cifra de un comunicado podría reemplazar a la del 10-Q. La quiebra sale de los 8-K con el ítem 1.03, pero de la API de la SEC, no de los zips (`src/03_bankruptcy.ipynb`).
- Los otros formularios (S-1, 20-F, etc.) no son estados contables trimestrales o anuales de empresas de EE. UU.

## 4. Columnas de `sub.txt` que no se leen

**Decisión.** No se leen (`usecols`) `ein`, `former`, `changed`, las 13 columnas de dirección, `countryinc`, `stprinc`, `afs`, `wksi`, `accepted`, `instance`, `detail`, `nciks` y `aciks`. (DECISIÓN TOMADA)

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

## 8. Versión de cada número: foto de la base al 31/12/2023

**Decisión.** Se aceptan las correcciones presentadas hasta el 31/12/2023 y no las posteriores (`docs/rumbo-mai.pdf`). Para cada número (sección 7): (DECISIÓN TOMADA)
- Si tiene versiones presentadas hasta el 31/12/2023, gana la **última** de ellas. Puede ser una enmienda (`/A`) o el comparativo de un documento posterior.
- Si no, gana la **primera** presentada después del 31/12/2023. Así los números de 2024 quedan como se publicaron por primera vez.

El código ordena por `["filed", "form"]`, aplica `keep="last"` a las filas con `filed` hasta `CUTOFF` y `keep="first"` a las posteriores, y da prioridad a las primeras (`src/02_build_dataset.ipynb`, paso 3).

**Desempate.** Si dos documentos tienen el mismo `filed`, `form` desempata: `"10-Q"` va antes que `"10-Q/A"` en orden alfabético. Antes del corte gana la enmienda (la última); después, el original (el primero). (DECISIÓN TOMADA)

**`filed` es la fecha en que se conoció la versión elegida.** Esta columna queda en `num.csv`, y `04_build_panel.ipynb` la lleva al panel como `fecha_presentacion`. Al armar features para predecir en la fecha t, solo se usan filas con `filed` anterior a t. El `ddate` no alcanza: el 10-K de 2020 se presenta entre 60 y 90 días después del 31 de diciembre. (DECISIÓN TOMADA)

**PRECAUCIÓN: sesgo de anticipación.** En 2018–2023 un número puede ser una corrección presentada años después: el modelo usa en 2019 un valor que en 2019 todavía no se conocía (look-ahead bias). En una prueba con la base anterior, el 6,4% de los números difería entre la primera y la última versión, y las enmiendas llegaban con una mediana de 105 días de atraso. El efecto en la evaluación del modelo es leve si se entrena con 2018–2023 y se evalúa con 2024, porque esa foto es la que se conocía al 31/12/2023. Con `filed` se puede medir: cuando la versión elegida es posterior al trimestre siguiente, el número no se conocía al predecir.

**Historial.**
- Primero se eligió la última versión (`keep="last"`), para tener los valores corregidos.
- El 2026-10-20 se cambió a la primera versión (`keep="first"`), para evitar el sesgo de anticipación.
- El 2026-10-30 el rumbo del grupo fijó la regla actual.

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

**Sigue pendiente.** La fecha del saldo (cierre o promedio) y el tratamiento del patrimonio negativo (por ejemplo HCA, con patrimonio negativo por recompras de acciones).

## 11. Alineación a trimestre calendario

**Decisión.** Cada número va al trimestre calendario que contiene más meses de su trimestre fiscal. En código: restar un mes al `ddate` y tomar su trimestre. Un trimestre fiscal que cierra el 31 de enero (noviembre, diciembre y enero) va al cuarto trimestre del año anterior. Decisión del usuario, 2026-10-22. (DECISIÓN TOMADA)

**Paso previo.** Se conservan solo las fechas de cierre de los documentos de la empresa (`sub.period`). Así se eliminan subperíodos, por ejemplo los de una empresa que sale de una quiebra (Gulfport Energy, 2021), y los comparativos con otro calendario (Sustainable Projects cambió su cierre de mayo a diciembre). Reemplaza al filtro anterior (meses de cierre módulo 3), que no resolvía a Sustainable Projects. (DECISIÓN TOMADA)

El trimestre de cada número se calcula en `src/02_build_dataset.ipynb` (paso 4, columna `quarter` de `num.csv`). El filtro de las fechas de cierre está en `src/04_build_panel.ipynb`, paso 4.

**Por qué.**
- El panel compara empresas en la misma fila. La regla elige el trimestre calendario que más se superpone con el trimestre fiscal: 2 de 3 meses.
- La alternativa era el trimestre que contiene el `ddate` (enero va al primer trimestre). Se superpone en 1 solo mes.
- Para el año fiscal, Compustat (la base contable más usada en finanzas) usa una regla equivalente: un año que termina entre enero y mayo se asigna al año calendario anterior.

**Alcance (panel anterior, solo sobrevivientes).** En el panel, 3 de 62 empresas cierran fuera de calendario. Las que cierran en febrero, mayo, agosto y noviembre (Norris Industries y Cryo-Cell) tienen el mismo trimestre con las dos reglas. La regla solo cambia a Enzo Biochem, que cierra en enero, abril, julio y octubre. Ninguna empresa del panel tiene choques (dos fechas en el mismo trimestre).

**Limitación.** La fila de un trimestre puede incluir un mes posterior: la fila 2018Q4 de Enzo Biochem incluye enero de 2019. Para el modelo, `filed` sigue siendo la fecha en que se conoció el número (sección 8).

## 12. Conceptos, tags y construcciones

**Decisión.** El mapa de conceptos a tags es `src/shared/concepts.py`: los 10 conceptos del rumbo más caja, con los tags de la guía de la mentora (`professor-materials/sec-edgar-guide.docx`, sección 4) y los del rumbo. El orden de cada lista es la prioridad. (DECISIÓN TOMADA)
- Resultado neto: `NetIncomeLoss` y, si falta, `ProfitLoss`, el alternativo de la mentora. `ProfitLoss` incluye la parte de los accionistas minoritarios, así que no es exactamente lo mismo. (DECISIÓN TOMADA)
- Caja: `CashAndCashEquivalentsAtCarryingValue` y `CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents`, los tags del rumbo. (DECISIÓN TOMADA)
- `StockholdersEquityAttributableToParent` (alternativo de la mentora para el patrimonio) no aparece en ningún documento de los dos sectores. Queda en la lista, pero no aporta.

**Construcción de la ganancia bruta.** Si falta `GrossProfit`, ganancia bruta = ingresos netos − costo de ventas (`CostOfRevenue` o `CostOfGoodsSold`), como indica la guía de la mentora. `GrossProfit` lo reporta solo una minoría de las empresas, sobre todo en energía. El costo de ventas no queda en el panel. (DECISIÓN TOMADA)

**Un tag por trimestre (regla A).** En cada empresa, concepto y trimestre se usa el primer tag con valor. Una empresa puede cambiar de tag entre trimestres. Decisión del usuario, 2026-10-22. (DECISIÓN TOMADA)
- Por qué: en el panel anterior, en 26 de los 35 cambios de tag los valores coincidían. Con un tag fijo por empresa (regla B), una empresa que cambió de tag necesita una excepción o queda afuera.
- Condición: los valores trimestrales se calculan por tag (cuarto trimestre y flujos acumulados) y el tag se elige después. Así una resta nunca mezcla dos tags, como pasaría en Houston American Energy. (DECISIÓN TOMADA)

**Ratios.** ROE, ROA, endeudamiento (`Liabilities / Assets`), liquidez corriente (`AssetsCurrent / LiabilitiesCurrent`), FCO / ingresos, margen bruto, margen operativo y margen neto. Van en fracción, no en porcentaje (`docs/rumbo-mai.pdf`). Una división por cero queda vacía (NaN), no infinita. (DECISIÓN TOMADA)

**Historial.** El 2026-10-27 el grupo decidió usar solo los tags de la mentora, sin construcciones. Antes se había descartado el margen bruto por baja cobertura en energía. El rumbo vuelve a incluir el margen bruto, y por eso se agrega la construcción.

## 13. Empresas del panel y quiebras

**Panel no balanceado.** Una empresa no necesita datos en todos los trimestres ni todos los conceptos (`docs/rumbo-mai.pdf`). Reemplaza al criterio anterior: 24 trimestres con todos los conceptos, que dejaba solo sobrevivientes. (DECISIÓN TOMADA)

**Empresas que existían al inicio.** Entra una empresa si tiene al menos un concepto con valor en 2018Q1. Quedan afuera las que se crearon (o empezaron a presentar) durante el período, como pide el rumbo. (DECISIÓN TOMADA)
- PRECAUCIÓN: las empresas jóvenes suelen ser las más riesgosas. Excluirlas puede bajar la cantidad de quiebras observadas.

**Quiebra.** La fecha de quiebra es la del 8-K con el ítem 1.03 ("Bankruptcy or Receivership"), de la API de la SEC (`src/03_bankruptcy.ipynb`). En el panel, una empresa que quiebra deja de tener filas desde el trimestre calendario de esa fecha. Por ejemplo, una quiebra del 2021-08-15 deja la última fila en 2021Q2. (DECISIÓN TOMADA)
- Se cortan también las empresas en Chapter 11 (reorganización) que siguen presentando, como Gulfport.
- `fecha_quiebra` cubre hasta el 31/12/2025, un año más que el panel, para poder etiquetar la quiebra en los próximos 2 trimestres o 1 año desde 2024.
- Una empresa que deja de tener filas sin `fecha_quiebra` salió por otra razón, por ejemplo una compra, o dejó de presentar.

**Pendientes** (`TODO.md`):
- Si Riley Exploration Permian (antes Tengasco Inc) queda en el panel: probable fusión inversa en 2021.
- Tratamiento de outliers: recortar los extremos (winsorizar) o marcarlos.
- ROA y ROE: fecha del saldo y patrimonio negativo (sección 10).

## Relación con el checklist de la profesora

La sección 9 de `professor-materials/sec-edgar-guide.docx` lista las decisiones a justificar.

| Pregunta del checklist | Sección |
|---|---|
| ¿Qué tipo de reporte usaron? | 3 |
| ¿Qué tag eligieron para cada variable? | 12 y `src/shared/concepts.py` |
| ¿Filtraron por `coreg`? | 6 |
| ¿Usaron `qtrs=4` para resultados y `qtrs=0` para balance? | 9 y 10 |
| ¿Cómo manejaron el desfasaje entre cierre y presentación? | 8 |
| ¿Qué criterio usaron para los outliers? | 13 (pendiente) |
