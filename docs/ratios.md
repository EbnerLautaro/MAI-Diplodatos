# Ratios del proyecto

El panel de salud y energía usa 7 ratios: margen operativo, margen neto, ROA, ROE, endeudamiento, liquidez corriente y FCO / ingresos. (DECISIÓN TOMADA)

Este documento explica qué calcula cada ratio y qué explica. También dice con qué tags se obtiene cada concepto y cómo se construye un concepto cuando la empresa no reporta su tag principal.

Las coberturas se calculan con `data/num.csv`, números con `ddate` entre 2018 y 2023 (`num.csv` solo trae valores en USD). Hay 307 empresas de energía y 176 de salud. El sector de cada empresa sale de su documento más reciente. La lista de tags de cada concepto está en `src/shared/concepts.py`.

## Antes de empezar: flujos y saldos

Un **flujo** mide lo que pasó durante un período: ingresos, ganancia, flujo de caja. Un flujo trimestral tiene `qtrs=1`.

Un **saldo** mide lo que hay en una fecha: activo, pasivo, patrimonio. Un saldo tiene `qtrs=0`.

Hay ratios que dividen un flujo por un saldo, como el ROA y el ROE. En esos ratios hay que decidir dos cosas:
- **El período del flujo.** Una ganancia trimestral da un ROA unas 4 veces menor que una ganancia anual. Hay dos opciones: anualizar (multiplicar por 4) o usar los últimos 12 meses (la suma de los últimos 4 trimestres, en inglés TTM, trailing twelve months). Los últimos 12 meses eliminan la estacionalidad.
- **La fecha del saldo.** Lo más simple es el saldo al cierre del trimestre. Lo más usado es el promedio entre el saldo inicial y el saldo final.

El período del flujo es trimestral, sin anualizar (`decisions.md`, sección 10). (DECISIÓN TOMADA)

La fecha del saldo está pendiente.

## Los ratios

| Ratio | Fórmula | Qué mide | Cómo se lee | En el panel y cuidados |
|---|---|---|---|---|
| **Margen operativo** | Resultado operativo / ingresos × 100. | El resultado operativo es lo que gana el negocio principal antes de intereses e impuestos. En inglés se llama operating income, y es parecido al EBIT (earnings before interest and taxes). El margen operativo mide la eficiencia del negocio sin el efecto de cómo se financia la empresa. | Un margen de 10% significa 10 centavos de resultado operativo por cada dólar de ventas. Un margen negativo significa que los costos del negocio superan a las ventas. | En energía, el margen operativo sigue al precio del petróleo y del gas, y cae mucho en 2020. En salud es más estable, pero en el segundo trimestre de 2020 se suspendieron las cirugías programadas. El margen operativo de las dos industrias muestra el efecto del COVID sobre el negocio, separado del efecto financiero. |
| **Margen neto** | Ganancia neta / ingresos × 100. | La ganancia neta es lo que queda después de todos los costos, intereses, impuestos y resultados extraordinarios. El margen neto mide la rentabilidad final sobre las ventas. | La diferencia con el margen operativo muestra el peso de los intereses, los impuestos y los resultados extraordinarios. | En energía, 2020 tiene pérdidas muy grandes por deterioro de activos (impairment): la empresa reduce el valor contable de sus reservas porque el precio del petróleo bajó. Ese efecto no es caja, pero baja mucho el margen neto. Es un caso típico de valores extremos. |
| **ROA** (return on assets, retorno sobre activos) | Ganancia neta / activo × 100. | Cuánto gana la empresa con todos sus recursos, sin importar si los financió con deuda o con capital propio. | Sirve para comparar empresas de tamaño distinto. Una empresa intensiva en capital, como una petrolera con pozos y oleoductos, tiende a tener un ROA más bajo que una empresa de servicios. | **Cuidado.** Divide un flujo por un saldo (ver "Antes de empezar"). |
| **ROE** (return on equity, retorno sobre patrimonio) | Ganancia neta / patrimonio × 100. | El rendimiento para los accionistas: cuánto gana la empresa por cada dólar de capital propio. | Con más deuda, el ROE sube cuando hay ganancias y baja más cuando hay pérdidas (apalancamiento). | ADVERTENCIA: si el patrimonio es negativo o cercano a cero, el ROE no tiene sentido. Ganancia positiva sobre patrimonio negativo da un ROE negativo, y un patrimonio cercano a cero da valores enormes. Ejemplo real: HCA Healthcare, la mayor empresa de hospitales del panel, tiene patrimonio negativo al cierre de casi todos los años de 2016 a 2023 (−4.950 millones de USD en 2018), aunque gana dinero. La causa son las recompras de acciones. Hay que decidir qué hacer con estos casos y documentarlo.<br><br>**Cuidado.** Divide un flujo por un saldo (ver "Antes de empezar"). |
| **Endeudamiento** | Pasivo / activo. | La proporción de los activos que se financia con deuda de terceros. El resto se financia con patrimonio. | Un valor de 0,6 significa que el 60% de los activos se financia con pasivo. Un valor mayor a 1 significa patrimonio negativo, como en el caso de HCA. | En 2020, muchas petroleras con endeudamiento alto quebraron. Este ratio sirve para mostrar el riesgo financiero antes y después del COVID.<br><br>PRECAUCIÓN: el pasivo total incluye deudas que no son financieras: cuentas a pagar, impuestos diferidos, obligaciones de abandono de pozos. No es lo mismo que "deuda". Esta diferencia está entre las preguntas para la mentora en `TODO.md`. |
| **Liquidez corriente** | Activo corriente / pasivo corriente. | El activo corriente es lo que se convierte en caja dentro de un año: caja, cuentas a cobrar, inventario. El pasivo corriente es lo que se paga dentro de un año. El ratio mide si la empresa puede pagar sus deudas de corto plazo. | Un valor menor a 1 es una señal de alerta: la empresa debe en el año más de lo que cobra en el año. | En 2020, muchas empresas tomaron deuda para tener caja. La liquidez puede subir aunque la empresa esté en peor situación. |
| **FCO / ingresos** | Flujo de caja operativo / ingresos × 100. El FCO (flujo de caja operativo) es la caja que genera el negocio en el período. | Cuánto de las ventas se convierte en caja. La ganancia contable incluye partidas que no son caja, como amortizaciones y deterioros; el FCO no las incluye. | Si el margen neto es muy distinto del FCO / ingresos, la ganancia contable tiene mucha partida que no es caja. En energía, un deterioro baja el margen neto pero no el FCO. | **Cuidado.** En los 10-Q (informes trimestrales), el flujo de caja viene acumulado desde el inicio del año. El valor trimestral se calcula por diferencia (ver `decisions.md`, sección 9). |

### Ratios descartados

| Ratio | Motivo |
|---|---|
| Margen bruto | `GrossProfit` lo reportan 12,1% de las empresas de energía (37 de 307). Las petroleras no presentan ganancia bruta. (DECISIÓN TOMADA) |
| I+D / ingresos | `ResearchAndDevelopmentExpense` lo reportan 4,6% de las empresas de energía (14 de 307). Es un ratio para tecnología o farmacéuticas. La norma contable de EE. UU. ASC 730 (Research and Development) obliga a informar el gasto en I+D (investigación y desarrollo) cuando existe. Si la empresa no lo informa, el gasto es probablemente cero o no significativo, así que se puede completar con 0. Pero con ceros el ratio casi no tiene información: queda en 0 en el 95,4% de las empresas de energía. En salud, el I+D se concentra en los laboratorios médicos (SIC 8071, 27 de 44 empresas), y esa información ya está en el SIC. (DECISIÓN TOMADA) |

## Conceptos y tags

La tabla muestra cuántas empresas tienen cada concepto con los tags de la lista, sobre el total del sector.

| Concepto | Energía | Salud |
|---|---|---|
| Ingresos | 282/307 (91,9%) | 161/176 (91,5%) |
| Resultado operativo | 266/307 (86,6%) | 162/176 (92,0%) |
| Ganancia neta | 299/307 (97,4%) | 173/176 (98,3%) |
| Activo | 306/307 (99,7%) | 175/176 (99,4%) |
| Pasivo | 236/307 (76,9%) | 157/176 (89,2%) |
| Patrimonio | 299/307 (97,4%) | 174/176 (98,9%) |
| Activo corriente | 298/307 (97,1%) | 173/176 (98,3%) |
| Pasivo corriente | 300/307 (97,7%) | 175/176 (99,4%) |
| Flujo de caja operativo | 307/307 (100,0%) | 176/176 (100,0%) |

PRECAUCIÓN: una empresa tiene el concepto si reporta alguno de sus tags al menos una vez en 2018–2023. Para el panel, la empresa necesita el concepto en todos los trimestres.

Las secciones siguientes dicen, para cada concepto, qué tags se usan y cómo construirlo cuando falta. "Coincide" es el porcentaje de períodos con diferencia de 1% o menos, medido en los períodos que tienen las dos cosas: el tag y la construcción. Todos los números de esta sección salen de `src/concepts_justification.ipynb`; su sección "Resultado" dice qué celda calcula cada uno.

### Cómo se eligió el orden de los tags

El orden de cada lista es una propuesta armada con criterios contables generales, no con una fuente externa. Solo se controló contra los datos de dos formas:
- **Cobertura:** cuántas empresas reportan cada tag. Dice si un tag sirve, pero no si el orden elige el valor correcto.
- **Estado de resultados:** para los ingresos, se comparó el orden con la línea que la empresa presenta como total (`src/concepts_justification.ipynb`, prueba 3, ver Ingresos).
- **Justificación completa:** `src/concepts_justification.ipynb` controla todas las listas con cuatro pruebas. Resultados:
  - **Los tags son los correctos.** En 8 de los 9 conceptos, un tag de la lista está en el estado contable en más del 95% de los documentos. La excepción es la ganancia neta (91,6%): en el resto, la línea "net income" usa `ProfitLoss` o `NetIncomeLossAvailableToCommonStockholdersBasic`, que son conceptos distintos.
  - **Casi todos los tags aportan.** `SalesRevenueGoodsNet` no se elige en ningún período y sacarlo no cambia nada. Los tags 4 a 10 de ingresos se eligen en 0 a 15 períodos cada uno.
  - **El orden elige el total.** Ingresos 99,7%, flujo de caja operativo 98,1%. En patrimonio la prueba no aplica: sus 22 conflictos son empresas que cambiaron de forma legal.
  - **Los alternativos de la guía de la profesora no sirven.** `StockholdersEquityAttributableToParent` tiene 0 filas. En el 83% de los períodos en que `ProfitLoss` difiere de `NetIncomeLoss`, la diferencia es exactamente la parte de los minoritarios.

"Coincide" significa que la diferencia relativa entre dos valores, |a − b| / |a|, es menor a 1%. Para una construcción, a es el valor del tag reportado y b es el valor construido.

Los criterios:
- **El total antes que sus partes.** En la taxonomía US-GAAP, `Revenues` es el total de los ingresos y `RevenueFromContract...` es un componente.
- **Neto de impuestos antes que bruto.** `...ExcludingAssessedTax` (sin impuestos a las ventas) va antes que `...IncludingAssessedTax`, porque se compara mejor entre empresas.
- **Tags vigentes antes que tags viejos.** `SalesRevenueNet` y sus variantes son anteriores a la norma ASC 606.
- **Tags de industria al final.** `OilAndGasRevenue` o `HealthCareOrganizationRevenue` suelen ser una parte de los ingresos.
- **Forma legal.** `StockholdersEquity`, `PartnersCapital` y `MembersEquity` dependen de la forma legal de la empresa y casi nunca aparecen juntos.

**Cuándo importa el orden.** Solo importa cuando una empresa reporta dos tags del mismo concepto para el mismo período (`cik`, `ddate`, `qtrs`) y los valores difieren. Medido en `num.csv`, 2018–2023, USD:

| Concepto | Períodos con más de un tag | Valores que difieren más de 1% |
|---|---|---|
| Ingresos | 2.286 de 10.418 (22%) | 1.290 (12%) |
| Patrimonio | 60 de 7.013 (1%) | 41 (0,6%) |
| Flujo de caja operativo | 508 de 7.349 (7%) | 232 (3%) |

Los demás conceptos tienen un solo tag, así que no tienen orden.

### Ingresos

**Tags, en orden de prioridad:**
1. `Revenues`
2. `RevenueFromContractWithCustomerExcludingAssessedTax`
3. `RevenueFromContractWithCustomerIncludingAssessedTax`
4. `SalesRevenueNet`
5. `SalesRevenueServicesNet`
6. `SalesRevenueGoodsNet`
7. `HealthCareOrganizationRevenue`
8. `HealthCareOrganizationPatientServiceRevenue`
9. `OilAndGasRevenue`
10. `OilAndGasSalesRevenue`

**Por qué tantos.** En 2018 entró en vigencia la norma ASC 606 (ingresos por contratos con clientes). Desde entonces muchas empresas pasaron de `SalesRevenueNet` a `RevenueFromContractWithCustomer...`. Los tags 7 a 10 son específicos de cada industria.

**Control con el estado de resultados (`src/concepts_justification.ipynb`, prueba 3, detalle de ingresos).** `pre.txt` dice en qué línea del estado de resultados está cada tag y con qué texto (`plabel`). El total de los ingresos está después de sus componentes. Entonces el tag correcto es el de la última línea de ingresos: la que la propia empresa presenta como total.
- De los 1.290 conflictos, 1.102 tienen los dos valores en el mismo documento. Los otros 188 mezclan documentos (un original y un comparativo posterior) y sus líneas no se pueden comparar.
- En los 1.102, todos los tags en conflicto están en el estado de resultados. La empresa muestra los dos: uno es el total y el otro es una parte.
- La prioridad actual elige el tag de la última línea en 1.099 casos (99,7%). Los 3 casos restantes (Expand Energy y Denbury) tienen `Revenues` como total y una línea `RevenueFromContract...` debajo, como detalle.
- El texto de la línea de `Revenues` casi siempre dice "total": "total revenue", "total revenues", "total operating revenues".

Conclusión: los datos apoyan poner `Revenues` primero. Se usa el orden de `concepts.py`, con `Revenues` primero. (DECISIÓN TOMADA)

PRECAUCIÓN: en el 28% de los pares (297 de 1.072), `Revenues` es **menor** que `RevenueFromContract...`. El total incluye una partida negativa. Los 297 casos son de energía (28 empresas). La causa probable son pérdidas por derivados (contratos de cobertura del precio), pero no se verificó línea por línea. Con `Revenues`, el margen incluye el resultado de la cobertura y es más volátil. Es coherente con `OperatingIncomeLoss`, que se calcula después de esas partidas.

**Quiénes quedan afuera.** Casi todas son empresas sin ventas: SPAC (empresas vacías creadas para comprar otra empresa, como HH&L Acquisition Co. o MedTech Acquisition Corp), biotecnológicas en etapa de investigación y petroleras en exploración (Zion Oil & Gas). No sirven para ratios sobre ingresos y quedan afuera del panel.

### Resultado operativo

**Tag:** `OperatingIncomeLoss`.

**Construcción si falta:** ingresos − `CostsAndExpenses` (costos y gastos totales). Coincide en el 89,7% de 3.875 períodos. De las 55 empresas sin `OperatingIncomeLoss`, recupera 34 (30 de energía y 4 de salud).

PRECAUCIÓN: no usar ingresos − `OperatingExpenses`. Solo coincide en el 70,2%, porque muchas empresas no incluyen el costo de ventas en `OperatingExpenses`.

**Por qué falta.** Muchas petroleras presentan el estado de resultados sin una línea de resultado operativo: listan todos los costos y pasan directo al resultado antes de impuestos.

### Ganancia neta

**Tag:** `NetIncomeLoss` (ganancia atribuible a los accionistas de la empresa).

**Construcción si falta:** `ProfitLoss` − `NetIncomeLossAttributableToNoncontrollingInterest`. `ProfitLoss` incluye la parte de los socios minoritarios (las participaciones no controladoras), y la resta la saca. Coincide en el 91,2% de 4.825 períodos; `ProfitLoss` solo coincide en el 54,8%. De las 11 empresas sin `NetIncomeLoss`, recupera 10.

PRECAUCIÓN: no usar `ProfitLoss` solo. Para el ROE, el numerador y el denominador tienen que ser de los mismos dueños: `NetIncomeLoss` va con `StockholdersEquity`.

### Activo

**Tag:** `Assets`. Lo reportan todas las empresas salvo una por sector.

**Construcción si falta:** `LiabilitiesAndStockholdersEquity`. Por la ecuación contable, el total del pasivo más el patrimonio es igual al activo. Coincide en el 100% de 6.856 períodos. Las 2 empresas sin `Assets` tampoco tienen `LiabilitiesAndStockholdersEquity`, así que la construcción no recupera ninguna.

### Pasivo

**Tag:** `Liabilities`.

**Construcción si falta:** `LiabilitiesAndStockholdersEquity` − patrimonio total − capital temporario.
- El patrimonio total incluye a los minoritarios: `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest`, o `StockholdersEquity` si la empresa no tiene minoritarios.
- El capital temporario (temporary equity) son acciones que la empresa puede tener que recomprar. No es pasivo ni patrimonio. Tags: `TemporaryEquityCarryingAmountAttributableToParent` y `RedeemableNoncontrollingInterestEquityCarryingAmount`.

Coincide en el 94,7% de 5.330 períodos. Sin restar el capital temporario, coincide en el 86,2%. De las 90 empresas sin `Liabilities`, recupera 89 (70 de energía y 19 de salud).

**Por qué falta.** Muchas empresas no presentan una línea de "total pasivo": listan cada pasivo y pasan al patrimonio. Es el concepto que más se beneficia de la construcción: sin ella, el endeudamiento deja afuera a 71 empresas de energía.

### Patrimonio

**Tags, en orden de prioridad:**
1. `StockholdersEquity`: patrimonio de una sociedad anónima, atribuible a los accionistas de la empresa.
2. `PartnersCapital`: patrimonio de una sociedad de socios (partnership, por ejemplo las MLP, master limited partnerships, comunes en oleoductos). 38 empresas de energía.
3. `MembersEquity`: patrimonio de una LLC (limited liability company, sociedad de responsabilidad limitada).

Los tres miden lo mismo con el nombre de cada forma legal.

**Construcción si falta:** `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest` − `MinorityInterest`. Coincide en el 93,1% de 2.263 períodos. De las 45 empresas sin `StockholdersEquity`, recupera 11; la mayoría de las otras son sociedades de socios o LLC y usan `PartnersCapital` o `MembersEquity`.

PRECAUCIÓN: la misma resta para una sociedad de socios (`PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest` − `MinorityInterest`) coincide con `PartnersCapital` solo en el 23,0% de 74 períodos. No se usa.

### Activo corriente y pasivo corriente

**Tags:** `AssetsCurrent` y `LiabilitiesCurrent`.

**Construcción si falta:** no hay una construcción confiable. Probablemente, las empresas que no reportan estos tags presentan un balance sin separar corriente y no corriente (no verificado con datos). Para ellas, la liquidez corriente no se puede calcular. Son 9 empresas de energía y 3 de salud.

### Flujo de caja operativo

**Tags, en orden de prioridad:**
1. `NetCashProvidedByUsedInOperatingActivities`
2. `NetCashProvidedByUsedInOperatingActivitiesContinuingOperations`

El segundo tag excluye las operaciones discontinuadas (negocios que la empresa vendió o cerró). Se usa solo si falta el primero. Con los dos tags, todas las empresas tienen el concepto.

**Por qué el total primero.** Es coherente con `NetIncomeLoss`, que también incluye las operaciones discontinuadas. El orden cambia el valor en 232 períodos.

Se usa el orden de `concepts.py`: el total primero. (DECISIÓN TOMADA)

PRECAUCIÓN: para predecir, `...ContinuingOperations` puede ser mejor, porque deja afuera los negocios que ya no existen.

## Pendientes

- Fecha del saldo (cierre o promedio) en el ROA y el ROE.
- Tratamiento del patrimonio negativo en el ROE.
