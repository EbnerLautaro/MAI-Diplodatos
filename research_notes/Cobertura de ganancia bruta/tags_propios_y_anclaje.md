# Tags propios (extensiones XBRL) y anclaje: ¿se pueden usar para recuperar el costo de ventas y la ganancia bruta?

Glosario mínimo: **XBRL** = formato de etiquetado de datos financieros que exige la SEC. **Tag estándar** = elemento de la taxonomía `us-gaap` (publicada por el FASB, el emisor de normas contables de EE. UU.). **Tag propio / extensión / custom** = elemento que define la empresa en su propia taxonomía. **Linkbase** = archivo de relaciones entre tags: de presentación (orden de renglones), de cálculo (qué suma a qué), de definición (dimensiones y otras relaciones). **Anclaje (anchoring)** = vincular un tag propio con el tag estándar más cercano, de significado más amplio (*wider*) o más estrecho (*narrower*). **FSDS** = Financial Statement Data Sets (los zips trimestrales que usa el proyecto). **FSNDS** = Financial Statement and Notes Data Sets (versión ampliada, con notas). **E&P** = empresas petroleras de exploración y producción. **LOE** = *lease operating expense*, el costo de operar los pozos.

Nota de método: la evidencia empírica de este documento sale de correr scripts sobre los zips locales del proyecto (`src/zips/`, filtrados por los `adsh` de `src/data/sub.csv`, sectores `energia` y `salud`). Los scripts quedaron en el scratchpad de la sesión (`/tmp/claude-1000/-home-ebner-FAMAF-Diplodatos-MAI/034c581f-a269-4335-9bfb-6c28960cb565/scratchpad/scripts/ext.py`, `stab.py`, `chk.py`) y no forman parte del repo. Esos números se marcan como "verificado en datos locales".

## 1. Qué contienen pre.txt y tag.txt y cómo identificar renglones de costo entre los tags propios

### Takeaway
Con solo FSDS ya se puede identificar un renglón de costo propio: `version == adsh` lo marca como propio, `stmt='IS'` e `inpth=0` lo ubican en el estado de resultados, `line` da el orden, `plabel` y `tlabel`/`doc` dan el texto y `crdr` el signo natural. El valor sale de `num.txt`, uniendo por `adsh`+`tag`+`version`. Pero en FSDS no hay relaciones de cálculo, así que la pertenencia a un subtotal se infiere por el texto o el orden, no por estructura.

### Cited Findings
- TAG: tiene "todos los tags estándar … y también todos los tags propios definidos en las presentaciones". Campos: `tag`; `version` ("para un tag estándar, identificador de la taxonomía; si no, el número de acceso [adsh] donde se definió el tag"); `custom` ("1 si el tag es propio (version=adsh)"; la SEC aclara que es redundante con `version`/`adsh`); `abstract`; `datatype` (p. ej. *monetary*); `iord` ("I" = saldo a una fecha, "D" = flujo de un período); `crdr` ("saldo contable natural … (débito o crédito)" si es monetario, si no NULL); `tlabel` (en un tag estándar, la etiqueta de la taxonomía; si no, "el texto que puso la empresa"); `doc` (definición truncada a 2048 caracteres: la de la taxonomía o la de la empresa; puede ser NULL). — [SEC, Financial Statement and Notes Data Sets, technical description (aqfsn_1.pdf), §5.2](https://www.sec.gov/files/aqfsn_1.pdf)
- PRE: "una fila por cada renglón de los estados financieros etiquetado por la empresa". Campos: `adsh`; `report` (número de la página "R" del visor); `line` ("orden de presentación del tag dentro del report"); `stmt` (CP = portada, BS = balance, IS = estado de resultados, CF = flujo de caja, EQ = patrimonio, CI = resultado integral, UN = no clasificable); `inpth` (1 = valor presentado "entre paréntesis"); `tag`; `version` ("identificador de la taxonomía si el tag es estándar; si no, adsh"); `prole` (rol de la etiqueta preferida); `plabel` ("el texto que aparece en el renglón", la etiqueta preferida); `negating` ("si el renderer trata el prole como de signo invertido"). Un mismo tag puede aparecer en más de un estado. — [SEC aqfsn_1.pdf, §5.7](https://www.sec.gov/files/aqfsn_1.pdf)
- La descripción de campos de PRE y TAG citada viene del PDF de FSNDS. Los zips FSDS del proyecto traen solo `sub.txt`, `num.txt`, `pre.txt`, `tag.txt` y `readme.htm` (verificado en datos locales: `unzip -l src/zips/2023q1.zip`). No hay `cal.txt`.
- Verificado en datos locales (2023q1): de los tags propios de **todas** las empresas en `tag.txt`, el 0% tiene `tlabel` nulo y el 12,5% tiene `doc` nulo. `crdr` vale C en 46.443, D en 37.391 y NULL en 11.135 (los NULL incluyen los no monetarios). Las extensiones de LOE tienen `crdr = D`, por ejemplo `LeaseOperatingExpenses` ("Lease operating expenses."), `OilAndGasProducingActivitiesLeaseOperatingExpense`, `OilLeaseOperatingExpense` y `DirectCostsOfLeaseOperatingExpenses`. — datos locales, `src/zips/2023q1.zip`
- Verificado en datos locales: ejemplos de nombres de tags propios en el estado de resultados (IS) de energía 2023q1: `ProductionAndSeveranceTaxesOperatingExpense`, `GasGatheringAndTransportationCost`, `LeaseOperatingExpenses`, `OilLeaseOperatingExpense`, `GatheringProcessingAndTransportationExpense`, `TransportationGatheringandProcessingCosts`, `ContractDrilling`, `OperatingExpensesExcludingDepreciationAndAmortization`, `OccupancyCost`. Cerca de la mitad no son costos: son ganancias o pérdidas, otros ingresos o subtotales (`IncomeIncludingEquityAffiliateEarningsBeforeIncomeTaxes`, `NetInterestAndOther`). — datos locales
- Verificado en datos locales: entre los renglones propios "con pinta de costo" del IS (filtro por expresión regular sobre `plabel`), `negating = 1` aparece en ~4% en energía y 0% en salud (2019q1 y 2023q1).
- Guía de la SEC: la etiqueta propia debe ser "lo más parecida posible al texto del documento original", lo que hace que `plabel` sea una buena fuente de texto para clasificar. — [SEC, EDGAR XBRL Guide (oct. 2026), §5.10.1 (antes EFM 6.11.1)](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf)

### Inferences
- Receta mínima con FSDS: `pre[(stmt=='IS') & (inpth=='0') & (version==adsh)]` → unir con `tag` por (`tag`, `version`) para obtener `crdr`, `datatype='monetary'`, `iord='D'` y `tlabel`/`doc` → clasificar por texto (`plabel` + `tlabel` + nombre del tag) → traer el valor de `num` con `adsh`+`tag`+`version`, sin dimensiones (en FSDS, `segments` vacío) y con `qtrs` según el período.
- `crdr='D'` + `iord='D'` + monetario filtra a "gastos/costos" (débito, flujo), pero no separa costo directo de gasto general, ni renglón de subtotal.
- Como en `num` el valor se guarda con el signo natural del elemento y `negating` solo cambia cómo se muestra, en principio no hace falta invertir signos por `negating`. Excepción: tags propios definidos con `crdr` contrario a su uso (p. ej. un "costo" definido como crédito). Esto es inferido, no verificado en la documentación.
- Probable trampa del pipeline actual: si `02_build_dataset` filtra `num` a versiones `us-gaap/...`, los tags propios no están en `src/data/num.csv`. Habría que releer los zips. Esto es inferido; no se revisó el código de `02_build_dataset`.

### Gaps
- No se leyó el `readme.htm` de FSDS para confirmar que la definición de campos de PRE/TAG es idéntica a la de FSNDS (en los datos se ven los mismos nombres de campo).
- No se midió cuántos renglones propios son subtotales y no partidas.

## 2. ¿FSNDS trae relaciones de cálculo (cal.txt) o de definición? ¿Sirve el linkbase de cálculo?

### Takeaway
FSNDS sí trae un `cal.txt` (relaciones de cálculo padre→hijo con signo) y no trae relaciones de definición. FSDS (los zips del proyecto) no trae ninguno de los dos. Con `cal.txt` se puede ver qué tags propios suman a `CostsAndExpenses`, `OperatingExpenses` o `CostOfRevenue`. No dice en qué estado está cada relación, pero eso se recupera cruzando con `pre`.

### Cited Findings
- FSNDS tiene ocho tablas: SUB, TAG, DIM, NUM, TXT, REN, PRE y CAL. CAL "provee información para relacionar aritméticamente los tags de una presentación". No hay tabla de definición (DEF). — [SEC aqfsn_1.pdf, §1 y §3](https://www.sec.gov/files/aqfsn_1.pdf)
- CAL: "una fila por cada relación de cálculo (arco)". Campos: `adsh`, `grp` (grupo de arcos), `arc`, `negative` ("indica un peso de −1 … típicamente +1"), `ptag`/`pversion` (padre) y `ctag`/`cversion` (hijo). No hay campo de rol ni de estado financiero. Fuente: "las presentaciones XBRL tal como se presentaron". — [SEC aqfsn_1.pdf, §5.8, Figura 9](https://www.sec.gov/files/aqfsn_1.pdf)
- REN (en FSNDS) da por cada `report` el `roleuri`, el nombre y la categoría de menú (S = estados, N = notas, etc.). — [SEC aqfsn_1.pdf, §5.6](https://www.sec.gov/files/aqfsn_1.pdf)
- Obligación de cálculo de la SEC: "si un estado financiero muestra dos o más partidas junto con su neto o total … la taxonomía propia debe tener una relación de cálculo del concepto total a cada una de las partidas" (5 condiciones). La SEC justifica estas relaciones porque dan "contexto vital para interpretar las extensiones de elementos propios". — [EDGAR XBRL Guide, §5.9.1 (antes EFM 6.15.2)](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf)
- Un mismo padre puede tener cálculos alternativos (dos sumas distintas en dos grupos). — [EDGAR XBRL Guide, §5.9.3 y ejemplo previo a §5.10](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf); [aqfsn_1.pdf §5.8 ("más de un conjunto de arcos para un mismo padre")](https://www.sec.gov/files/aqfsn_1.pdf)

### Inferences
- Algoritmo posible: en FSNDS, tomar los arcos con `ptag` ∈ {`CostsAndExpenses`, `OperatingCostsAndExpenses`, `OperatingExpenses`, `CostOfRevenue`, `CostOfGoodsAndServicesSold`} y `cversion == adsh` (hijo propio). Cruzarlos con `pre` (`stmt='IS'`) para quedarse con los del estado de resultados. Ventajas: confirma que el tag propio es un componente del total de costos y no un subtotal ni un "otro ingreso", y da el signo (`negative`).
- Límite clave para el objetivo: en E&P y hospitales, el padre suele ser `CostsAndExpenses` u `OperatingExpenses`, o sea todos los gastos operativos, no un "costo de ventas". La estructura de cálculo no dice cuáles de los hijos son "costo directo". Esa decisión sigue siendo por texto o por regla.
- Costo práctico: FSNDS es otro producto, con archivos mucho más grandes que FSDS (incluye notas y texto). Habría que descargarlo para 2018–2024. No se midió el tamaño.

### Gaps
- No se verificó qué período cubren los FSNDS ni con qué frecuencia se publican (la página de la SEC no se abrió en esta sesión).
- No se midió qué porcentaje de presentaciones de los dos sectores tiene arcos de cálculo con hijos propios bajo `CostsAndExpenses`/`OperatingExpenses`.
- Desde 2023 la SEC acepta XBRL Calculations 1.1 (el XBRL Guide lo menciona entre las especificaciones). No se verificó si eso cambia algo en `cal.txt`.

## 3. El "anclaje" de extensiones: ¿existe en EDGAR? ¿desde cuándo? ¿está en algún dataset de la SEC?

### Takeaway
No. El anclaje (*wider/narrower*) es un requisito del ESEF europeo, no de la SEC. No se encontró ninguna regla de EDGAR que lo exija para empresas que reportan en US GAAP 2018–2024. La premisa de un "requisito de anclaje de la SEC de 2019–2022" no se sostiene. Ningún dataset masivo de la SEC trae anclajes (FSNDS no tiene relaciones de definición). Lo más parecido que exige la SEC es la relación de cálculo.

### Cited Findings
- Verificado en documentos: el EDGAR XBRL Guide vigente (oct. 2026, que reemplaza al capítulo 6 del EDGAR Filer Manual Vol. II) no contiene "anchor", "wider" ni "narrower" en el sentido de anclaje. La única frase parecida es la de §5.10: "renglones … más amplios o más estrechos que los conceptos estándar disponibles", para justificar cuándo crear un concepto propio. — [EDGAR XBRL Guide](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf); el cap. 6 del Filer Manual ahora remite a esa guía: [EFM Vol. II cap. 6](https://www.sec.gov/files/edgar/filermanual/efmvol2-c6.pdf)
- Verificado en documentos: el EDGAR Filer Manual Vol. II v60 (diciembre de 2021, en plena adopción de Inline XBRL) tampoco menciona el anclaje. Las apariciones de "anchor" son anclas HTML `<a>`. — [EFM Vol. II v60](https://www.sec.gov/info/edgar/specifications/edgarfm-vol2-v60.pdf)
- Lo que sí exige la SEC: no duplicar conceptos estándar ("en vez de declarar un concepto nuevo … asignar una etiqueta a un concepto estándar"; ejemplo: "gross margin" debe ir en `GrossProfit` con etiqueta propia, no en un `GrossMargin` propio); crear un monetario propio solo si los estándar "son demasiado amplios"; y dar al propio las mismas propiedades (tipo, período, saldo) que el concepto general cercano. — [EDGAR XBRL Guide, §5.6.1 (EFM 6.8.4), §5.10.1, §5.10.2 (EFM 6.8.9)](https://www.sec.gov/files/edgar/filer-information/specifications/xbrl-guide.pdf)
- ESEF (Unión Europea, informes anuales desde 2020/2021): las extensiones deben anclarse "al concepto de la taxonomía ESEF de significado contable y/o alcance más amplio más cercano", con la relación *wider-narrower* en el linkbase de definición. — [XBRL International, "Wider, Narrower: Anchoring in ESEF"](https://www.xbrl.org/news/wider-narrower-anchoring-in-esef/); [ESMA, ESEF Reporting Manual (2019)](https://www.mfsa.mt/wp-content/uploads/2019/07/20190712_ESEF_esma32-60-254_ESEFReportingManual.pdf); [XBRL International, guía de anclaje](https://www.xbrl.org/guidance/esef-rules-anchoring-extensions/). Según fuentes de la industria, ESMA fue el primer regulador en exigir el anclaje (fuente secundaria, solo snippet de búsqueda: [IRIS CARBON](https://iriscarbon.com/anchoring)).
- La adopción de Inline XBRL por la SEC (Release 33-10514, 2018) se escalonó por tipo de empresa entre 2019 y 2021. No se encontró en ella ninguna regla de anclaje; la búsqueda dirigida tampoco devolvió una. — [SEC Release 33-10514](https://www.sec.gov/files/rules/final/2018/33-10514.pdf) (el PDF no se releyó en esta sesión; el calendario sale del conocimiento previo, no está verificado aquí)

### Inferences
- Para empresas de EE. UU., el anclaje no sirve para mapear los tags propios de LOE a `us-gaap`. Los sustitutos son la relación de cálculo (FSNDS `cal.txt`), las propiedades del elemento (`crdr`, `iord`, `datatype`) y el texto (`plabel`, `tlabel`, `doc`).
- Quizá la consigna confunde el anclaje con algo de ESEF o con las reglas DQC de XBRL US (sección 4). Conviene corregir la premisa en el informe.

### Gaps
- No se revisaron todas las versiones del EFM entre 2018 y 2024 (solo v60 y la guía vigente), ni las propuestas de la SEC posteriores a 2024. No se encontró evidencia de que la SEC haya propuesto el anclaje para US GAAP, pero tampoco se hizo una búsqueda exhaustiva de comment letters.

## 4. Investigación y herramientas existentes para mapear extensiones a conceptos estándar; precisión y trampas

### Takeaway
La literatura mide **cuántas** extensiones hay y si son innecesarias (~40% lo eran en 2009–2010), no reporta tasas de acierto de un mapeo automático extensión→estándar. No se encontró ningún benchmark público de precisión. Las herramientas reales (XBRL US DQC, el control de la SEC) se enfocan en detectar extensiones que no hacían falta. En la práctica, el mapeo es por reglas sobre el texto y la estructura, y las trampas más grandes en estos sectores son de **significado** más que de técnica.

### Cited Findings
- Debreceny, Farewell y Piechocki, "Flex or Break? Extensions in XBRL Disclosures to the SEC" (*Accounting Horizons*, 2011, DOI 10.2308/acch-50068): en presentaciones de abril 2009 a junio 2010, ~40% de las extensiones eran innecesarias porque ya existía un elemento equivalente en US GAAP. — [ResearchGate (resumen)](https://www.researchgate.net/publication/274579039_Flex_or_break_Extensions_in_XBRL_disclosures_to_the_SEC) (solo se leyó el resumen o snippet)
- Hoitash y Hoitash, "Measuring Accounting Reporting Complexity with XBRL", *The Accounting Review* 93(1), 2018: proponen medir la complejidad contando los tags de un 10-K (estándar y extensiones). La complejidad se asocia con más reexpresiones, problemas de control interno, atrasos y honorarios de auditoría. El paper no trata el mapeo. — [Bentley University](https://experts.bentley.edu/en/publications/measuring-accounting-reporting-complexity-with-xbrl-7/)
- Huang, No y Vasarhelyi (2018, *Journal of Information Systems*): las empresas con peor desempeño tienen presentaciones XBRL más complejas, lo que los autores leen como un uso estratégico de las extensiones. — snippet de búsqueda, no verificado en la fuente
- Tasa de tags propios según la SEC (renglones, sin miembros ni dominios; todos los formularios 10-K): promedio de todas las empresas 19% (2016) → 18% (2017–2018) → 17% (2019). En 2020 vuelve a subir (19–21% según el tipo de empresa). En 2021–2024 la SEC informa solo la tendencia (en general baja). No hay desagregación por industria ni por estado financiero. — [SEC, U.S. GAAP XBRL Custom Tags Trend](https://www.sec.gov/structureddata/trends)
- DERA (2014): las empresas chicas tenían una tasa de tags propios casi el doble que las grandes y eran el 96% de las que superaban el 50%. — [SEC DERA, Assessment of Custom Tag Rates (2014)](https://www.sec.gov/dera/reportspubs/assessment-custom-tag-rates-xbrl.html) (snippet)
- XBRL US DQC (Data Quality Committee, comité de calidad de datos): sus reglas detectan errores y extensiones que duplican elementos estándar (p. ej. DQC_0156, extensiones que combinan básico y diluido). Son validaciones, no un mapeo. — [XBRL US, reglas aprobadas](https://xbrl.us/home/priorities/data-quality/rules-guidance/); [DQC_0156](https://xbrl.us/data-rule/dqc_0156pr/)
- Práctica de usuarios: el linkbase de etiquetas de la extensión es "la mejor fuente" para emparejar nombres de la empresa con tags XBRL, y los nombres de tags cambian entre versiones de la taxonomía. — [Foro de XBRL US](https://xbrl.us/forums/topic/how-to-find-a-complete-list-of-similar-concept/) (fuente informal)
- Verificado en datos locales: **mal uso de tags estándar para LOE**. `us-gaap:LeaseOperatingExpense` y `OilAndGasProductionExpense` quedaron en desuso el 2018-01-31 (`tlabel` de las versiones us-gaap/2016 y 2017: "(Deprecated 2018-01-31)"). En los 10-K del primer trimestre de 2018 a 2024 de energía, los renglones del IS con etiqueta parecida a LOE/producción usan sobre todo `OperatingLeaseExpense` (179 renglones), que en la taxonomía es el gasto de arrendamiento operativo (norma ASC 842) y no el costo de operar pozos. Le siguen `LeaseOperatingExpense` (61, ya en desuso), `ResultsOfOperationsProductionOrLiftingCosts` (38) y `CostOfGoodsAndServicesSold` (26). Los tags propios son minoría: entre 2% (2018) y 14% (2024) de esos renglones. — datos locales, `src/zips/20{18..24}q1.zip`
- Verificado en datos locales: **inestabilidad entre años**. De 57 CIK de energía con renglón tipo LOE en ≥3 años de 10-K (2018–2024), 45 cambiaron de nombre de tag al menos una vez (incluye el cambio forzado por el desuso de 2018) y 9 alternaron entre tag propio y estándar. — datos locales

### Inferences
- Trampas para un mapeo por texto, ordenadas por impacto:
  1. **Significado, no técnica.** En E&P, "costo de ventas" = LOE + impuestos a la producción + gathering/transporte (± DD&A, la depreciación, agotamiento y amortización). Cada empresa arma esa suma distinto. En hospitales, el estado de resultados lista salarios, insumos, alquileres y "otros gastos operativos". Sumarlos da casi todos los gastos operativos, y la "ganancia bruta" se acerca a un EBITDA (resultado antes de intereses, impuestos, depreciación y amortización). `decisions.md` ya registra que en E&P el `CostOfGoodsAndServicesSold` da un margen mediano de 0,65 contra 0,13 en servicios petroleros.
  2. **Mal uso de tags estándar** (`OperatingLeaseExpense` como LOE). La regla "solo `us-gaap`" no protege de esto.
  3. **Subtotales y renglones duplicados**: un tag propio puede ser un subtotal ("total costos de producción") o repetir partidas. Sin `cal.txt`, si se suma todo lo que tiene pinta de costo, se cuenta dos veces.
  4. **"Excluyendo D&A"**: muchos costos propios y estándar vienen sin depreciación, lo que rompe la comparación con las empresas que la incluyen.
  5. **Falsos positivos de la expresión regular**: en datos locales aparecieron "gain from disposal of oil and gas operations", "severance and related costs" (indemnizaciones por despido, no impuestos de *severance*) y "unissued directors' deferred compensation shares".
  6. **Dimensiones**: los segmentos/miembros (en `num.segments`) pueden repetir el mismo tag por segmento. Hay que quedarse con el total sin dimensiones.
  7. **Signo**: confiar en el signo de `num` y en `crdr`; `negating` solo afecta la presentación (inferido).
  8. **Cambio de tags entre trimestres**: el nombre del tag propio o el `adsh` de origen (`version`) cambia en cada presentación. Hay que mapear por texto en cada presentación, no por nombre de tag.

### Gaps
- No se encontraron tasas de precisión publicadas para el mapeo automático de extensiones (ni por similitud de etiquetas ni por aprendizaje automático). No hay una cifra de "precisión típica" que reportar.
- No se revisaron las tablas de estandarización de proveedores comerciales (Calcbench, XBRL US API, S&P) ni paquetes como `secfsdstools`, que tiene un estandarizador propio.

## 5. ¿Cuánto pesan las extensiones en el estado de resultados de E&P y hospitales, y qué parte sería recuperable?

### Takeaway
Las extensiones son frecuentes (64–70% de las presentaciones tienen ≥1 renglón propio en el IS) pero pocas por presentación (5–9% de los renglones). Entre las presentaciones **sin** tag estándar de costo o de ganancia bruta, solo ~15–24% tiene un renglón propio con pinta de costo. El margen de mejora por extensiones es chico, y más chico todavía después de filtrar los falsos positivos. Hay más para recuperar en tags **estándar** que hoy no están en `concepts.py`, aunque con los problemas de significado de la sección 4.

### Cited Findings
Todo lo siguiente está verificado en datos locales (sectores del proyecto; IS con `inpth=0`; "con tag de costo" = alguno de los 8 tags de `costo_ventas` de `src/shared/concepts.py`, o `GrossProfit`):

| Trimestre de presentación | Sector | Presentaciones con IS | % renglones IS propios | % presentaciones con ≥1 propio | % con tag estándar de costo o ganancia bruta | Sin ese tag: % con renglón propio tipo costo |
|---|---|---|---|---|---|---|
| 2019q1 | energía | 199 | 6,8% | 63,8% | 52,3% | 21,1% (20 de 95) |
| 2019q1 | salud | 73 | 4,9% | 49,3% | 64,4% | 15,4% (4 de 26) |
| 2023q1 | energía | 156 | 8,9% | 67,9% | 43,6% | 19,3% (17 de 88) |
| 2023q1 | salud | 104 | 7,4% | 70,2% | 48,1% | 24,1% (13 de 54) |

- Etiquetas propias típicas en esas presentaciones sin tag de costo. Energía: "lease operating (expenses)", "production expenses", "production taxes", "gathering and transportation", "gathering, processing and transportation", "severance and ad valorem taxes". Salud: "patient care costs", "practice salaries and benefits", "practice supplies and other operating expenses", "cost of revenue(s) (exclusive of D&A)", "direct patient expense", "cost of operations, excluding D&A". — datos locales
- En esas mismas presentaciones sin tag de costo, los renglones tipo costo usan con más frecuencia tags **estándar** que no están en `concepts.py`. Energía 2023q1: `OperatingExpenses` 32, `OperatingLeaseExpense` 20, `CostsAndExpenses` 18, `OperatingCostsAndExpenses` 16, `ProductionTaxExpense` 12, `CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization` 10, `ResultsOfOperationsTransportationCosts` 6, `ResultsOfOperationsProductionOrLiftingCosts` 4. Salud 2023q1: `OperatingExpenses` 27, `LaborAndRelatedExpense` 9, `OtherCostAndExpenseOperating` 7, `CostsAndExpenses` 7, `CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization` 7, `SuppliesExpense` 6, `HealthCareOrganizationExpensesNet` 6. — datos locales
- Referencia general: la tasa de tags propios de todas las empresas que publica la SEC (~17–20% en 2017–2020) no está desagregada por industria. — [SEC trends](https://www.sec.gov/structureddata/trends)

### Inferences
- Techo de recuperación por extensiones: ~20% de las presentaciones hoy sin costo. En el panel, eso sumaría a lo sumo unos pocos puntos porcentuales de cobertura de la ganancia bruta en cada sector. Además, buena parte de esos casos (E&P con LOE, clínicas con salarios + insumos) no produce un "costo de ventas" comparable con el de las empresas que sí lo reportan. Estimación gruesa a partir de 2 trimestres con 10-K; no se calculó sobre el panel.
- Si se relaja la regla, lo más defendible es una regla acotada y documentada: (a) aceptar un tag propio solo si su `plabel`/`tlabel` coincide con una lista cerrada de patrones de "cost of revenue/sales/services/operations" (no LOE, no salarios); (b) exigir `crdr='D'`, `iord='D'`, monetario y `segments` vacío; (c) si es posible, confirmar con `cal.txt` de FSNDS que es hijo directo de un total de costos y no un subtotal. Para E&P y hospitales, quizá conviene aceptar que la ganancia bruta no existe en esos negocios y usar otro margen, por ejemplo el operativo.
- El mal uso de `OperatingLeaseExpense` como LOE muestra que relajar a "tags estándar extra" tiene el mismo problema de significado que relajar a extensiones.

### Gaps
- Solo se midieron 2 trimestres de alta concentración de 10-K (2019q1 y 2023q1). Faltan los 10-Q y el resto de los años.
- No se separaron E&P de servicios petroleros ni hospitales de otras actividades de salud (por código SIC, el código de actividad de la SEC). El pedido habla de "E&P" y "hospitales", y los números son de los sectores `energia` y `salud` completos.
- No se validó a mano qué parte del ~20% son verdaderos "costo de ventas" y no falsos positivos.
- No se midió la cobertura en celdas empresa × trimestre del panel (la métrica de `decisions.md` §14).
