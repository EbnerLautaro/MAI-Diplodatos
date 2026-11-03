# Cómo presentan el costo de ventas y la ganancia bruta las petroleras (SIC 1300–1399) y los servicios de salud (SIC 8000–8099) en EE.UU., 2018–2024, y cómo lo etiquetan en XBRL (us-gaap)

(Notas del investigador; guardadas por el coordinador porque el subagente no pudo escribir el archivo.)

Siglas: **LOE** = lease operating expense (gasto operativo de pozos); **DD&A** = depreciación, agotamiento y amortización; **GP&T** = gathering, processing and transportation; **E&P** = exploración y producción; **G&A / SG&A** = gastos generales y de administración (y de ventas); **EBITDA** = resultado antes de intereses, impuestos, depreciaciones y amortizaciones; **S-X** = Regulation S-X de la SEC; **ASC** = FASB Accounting Standards Codification; **FSDS** = SEC Financial Statement Data Sets; **DQC** = Data Quality Committee de XBRL US.

**Evidencia propia.** Además de fuentes web, se analizaron en local: (1) las taxonomías FASB 2018–2024 (`https://xbrl.fasb.org/us-gaap/<año>/us-gaap-<año>[-01-31].zip`: etiqueta estándar con "(Deprecated AAAA-MM-DD)", documentación y linkbase `depcon-def` de reemplazos); (2) los FSDS del proyecto: `src/zips/2022q1.zip` y `2024q1.zip` `pre.txt` (renglón del estado de resultados → etiqueta visible → tag) y `src/data/num.csv` / `sub.csv` (solo tags us-gaap estándar de 10-K/10-Q de salud y energía). Scripts en el scratchpad de la sesión (tax2.py, tax3.py, tax4.py, usage.py, usage2.py, custom.py, pre.py).

## Hallazgos principales
1. Ni ASC 220 ni S-X 5-03 exigen un subtotal de ganancia bruta; S-X 5-03 solo pide los costos aplicables a cada clase de ingreso.
2. Casi ninguna E&P ni ningún operador de hospitales reporta ganancia bruta: 3 de 74 10-K de E&P y 0 de 15 de hospitales/geriátricos la tienen en el estado de resultados (2024q1).
3. La taxonomía 2018 deprecó CostOfGoodsSold, CostOfServices, OilAndGasProductionExpense, LeaseOperatingExpense, OilAndGas*Revenue y HealthCareOrganization*Revenue; su uso termina con los filings de 2018.
4. El reemplazo oficial de FASB para LeaseOperatingExpense es OperatingLeaseExpense (elemento de arrendamientos ASC 842), y la mayoría de las E&P lo adoptó (24–26 de 35). En hospitales el mismo tag es alquiler de inmuebles: el tag significa cosas distintas según el sector.
5. En Devon, Diamondback y Pioneer, CostOfGoodsAndServicesSold cubre solo marketing/midstream/producto comprado: ingresos − ese tag es una ganancia bruta engañosa para E&P.
6. Los tags deprecados de la lista `costo_ventas` de `concepts.py` casi no tienen datos después de 2018.

## 1. Qué exigen ASC 220 y S-X 5-03; ¿se permite presentar por naturaleza?

### Takeaway
Ninguna norma exige el subtotal "ganancia bruta". ASC 220 no fija renglones de gastos. S-X 5-03 (registrantes SEC) pide mostrar por separado el costo aplicable a cada tipo de ingreso, no un subtotal de margen. En la práctica: las E&P listan costos operativos por tipo (LOE, impuestos a la producción, GP&T, exploración, DD&A); los hospitales presentan gastos por naturaleza (salarios, insumos, otros, D&A, alquileres). Solo laboratorios y parte de los servicios petroleros muestran "cost of revenue/services", y a veces ganancia bruta.

### Cited Findings
- "Topic 220 ... does not contain any general requirements for specific expense captions on the face of the income statement"; no hay en US GAAP un análogo a IAS 1 ¶104 — [FASB/IASB staff paper 21C (DISE), 30-sep-2022, ¶3](https://www.ifrs.org/content/dam/ifrs/meetings/2022/september/fasb-iasb/ap-21c-fasb-standard-setting-disaggregation-income-statement-expenses-project-background-and-next-steps.pdf)
- "Commercial and industrial companies are generally required to present certain expense captions by function, such as cost of sales and ... SG&A" — mismo documento, ¶4.
- Nota 4 del mismo documento: "Notwithstanding ... Rule 5-03 to present functional expense captions, some entities, such as airlines, have a longstanding industry practice of presenting expenses by nature on the face of their income statements".
- S-X 210.5-03 — [LII Cornell](https://www.law.cornell.edu/cfr/text/17/210.5-03): ítem 2 "State separately the amount of (a) cost of tangible goods sold, (b) operating expenses of public utilities or others, (c) expenses applicable to rental income, (d) cost of services, and (e) expenses applicable to other revenues"; ítem 3 "State separately any material amounts not included under caption 2"; ítem 4 SG&A; se pueden combinar clases que no superen el 10 %; se admiten apartamientos "except as otherwise permitted by the Commission".
- KPMG: US GAAP no exige naturaleza ni función; los requisitos vienen de la SEC; la mayoría presenta por función — [KPMG 2023](https://kpmg.com/us/en/articles/2023/income-statement-presentation.html) (solo resumen del buscador).
- SAB Topic 11.B: si el costo de ventas excluye la depreciación, el renglón debe decirlo y no debe presentarse una ganancia bruta antes de depreciación; la SEC ha pedido quitar ese subtotal o rotularlo no-GAAP — [Deloitte Roadmap Non-GAAP 4.9](https://dart.deloitte.com/USDART/home/accounting/sec/sec-reporting-interpretations-manual/roadmap-non-gaap-financial-measures/chapter-4-non-gaap-measures-that/4-9-non-gaap-measures-that); [CORRESP 1463972](https://www.sec.gov/Archives/edgar/data/1463972/000110465922096491/filename1.htm)
- ASU 2024-03 (DISE) no cambia renglones; agrega desglose en nota; rige para ejercicios que empiezan después del 15-dic-2026 (fuera de 2018–2024) — [RSM](https://www.rsmus.com/insights/financial-reporting/fasb-issues-final-guidance-on-disaggregated-expense-disclosures); [Deloitte ASU 2025-01](https://dart.deloitte.com/USDART/home/news/all-news/2025/jan/fasb-effective-date-asu-disaggregation-income-statement)
- La taxonomía refiere `ProductionTaxExpense` a ASC 220-10-S99-2 "(SX 210.5-03(2))" — [taxonomía 2024](https://xbrl.fasb.org/us-gaap/2024/us-gaap-2024.zip)
- Definición FASB de `GrossProfit`: "Aggregate revenue less cost of goods and services sold or operating expenses directly attributable to the revenue generation activity" — [taxonomía 2024](https://xbrl.fasb.org/us-gaap/2024/us-gaap-2024.zip)
- Tags en el estado de resultados de los 10-K presentados en 2024q1 — [FSDS](https://www.sec.gov/dera/data/financial-statement-data-sets):

| Grupo SIC | 10-K con estado de resultados | GrossProfit | CostOfRevenue | CostOfGoodsAndServicesSold | OperatingLeaseExpense | LaborAndRelatedExpense | SuppliesExpense |
|---|---|---|---|---|---|---|---|
| 1311 E&P | 74 | 3 | 2 | 29 | 26 | 1 | 0 |
| 1381/1382/1389 perforación y servicios | 40 | 3 | 3 | 16 | 1 | 0 | 0 |
| 805x/806x geriátricos y hospitales | 15 | 0 | 0 | 4 | 3 | 8 | 5 |
| 8071 laboratorios | 20 | 5 | 9 | 4 | 0 | 0 | 0 |

- % de empresas que alguna vez reportaron el tag, 2018–2025 (`num.csv`, cualquier contexto), en el orden E&P (234) / perforación (29) / servicios petroleros (65) / hospitales (19) / geriátricos (16) / laboratorios (47) / atención domiciliaria (17) / consultorios (13):
  - GrossProfit: 11/10/20/11/6/45/59/62 %
  - CostOfRevenue: 9/10/20/16/6/51/41/46 %
  - CostOfGoodsAndServicesSold: 23/24/28/32/25/21/41/31 %
  - LeaseOperatingExpense: 36/10/0/0/0/0/0/0 %
  - ProductionTaxExpense: 31/10/0/… %
  - ExplorationExpense: 34/10/3/0… %
  - OtherCostAndExpenseOperating: 18/7/6/53/25/6/6/15 %
  - LaborAndRelatedExpense: 4/0/2/53/38/6/12/23 %
  - SuppliesExpense: solo hospitales, 42 %
  - OperatingIncomeLoss: 85/90/95/74/69/98/100/100 %
- 10-K con `GrossProfit`, 2018–2025: E&P 7 %, perforación 5 %, servicios petroleros 12 %, hospitales 5 %, geriátricos 1 %, laboratorios 31 %, atención domiciliaria 43 %, consultorios 29 %.

### Inferences
- La ganancia bruta falta porque las empresas no la presentan, no por un problema de etiquetado.
- La presentación por naturaleza de los hospitales es una práctica sectorial tolerada, como la de las aerolíneas (sin fuente primaria que lo diga para hospitales).
- El margen operativo se puede calcular para casi todas las empresas; el margen bruto no.

### Gaps
- No se pudo leer ASC 220-10-S99-2 (requiere login).
- Un resumen del buscador atribuía a PwC que la presentación por naturaleza "no está permitida" para registrantes SEC; no verificado y contradice la práctica de los hospitales.
- Solo se contaron 2022q1 y 2024q1, no la serie año por año.

## 2. Renglones típicos del estado de resultados por sector

### Takeaway
- **E&P:** LOE/production expenses, impuestos a la producción y ad valorem, GP&T, exploración/pozos secos, DD&A, deterioros, G&A. Sin ganancia bruta.
- **Hospitales:** salarios y beneficios, insumos, otros gastos operativos, D&A, alquileres. Sin ganancia bruta.
- **Servicios petroleros y laboratorios:** un renglón único de cost of services/revenue; LabCorp además muestra Gross profit.

### Cited Findings
Etiqueta visible → tag, 10-K presentados en 2024q1:
- **Devon** — [10-K](https://www.sec.gov/Archives/edgar/data/1090012/000095017024021781/): Production expenses → `ResultsOfOperationsProductionOrLiftingCosts`; Exploration → `ExplorationExpense`; Marketing and midstream expenses → `CostOfGoodsAndServicesSold`; DD&A → `DepreciationDepletionAndAmortization`; G&A → `GeneralAndAdministrativeExpense`; Total expenses → extensión `TotalExpenses`.
- **EOG** — [10-K](https://www.sec.gov/Archives/edgar/data/821189/000082118924000011/): Lease and Well → `OperatingLeaseExpense`; Transportation → `ResultsOfOperationsTransportationCosts`; Gathering and Processing → extensión; Exploration → `ExplorationExpense`; Dry Hole → `ResultsOfOperationsDryHoleCosts`; Impairments → `ImpairmentOfOilAndGasProperties`; Marketing Costs → extensión; Taxes Other Than Income → extensión; Total → `CostsAndExpenses`.
- **Diamondback** — [10-K](https://www.sec.gov/Archives/edgar/data/1539838/000153983824000019/): Lease operating expenses → `OperatingLeaseExpense`; Production and ad valorem taxes → `ProductionTaxExpense`; Cost of goods and services sold → `CostOfGoodsAndServicesSold`; DD&A; G&A → `SellingGeneralAndAdministrativeExpense`; Other operating → `OtherCostAndExpenseOperating`.
- **Pioneer** — [10-K](https://www.sec.gov/Archives/edgar/data/1038357/000103835724000020/): "Costs and expenses" → `CostOfGoodsAndServicesSold`; Production and ad valorem taxes → `ProductionTaxExpense`; Exploration and abandonments → `ExplorationAbandonmentAndImpairmentExpense`.
- **Halliburton** — [10-K](https://www.sec.gov/Archives/edgar/data/45012/000004501224000007/): Cost of services and sales → `CostOfGoodsAndServicesSold`.
- **Patterson-UTI** — [10-K](https://www.sec.gov/Archives/edgar/data/889900/000095017024020661/): Operating costs and expenses → `CostOfGoodsAndServicesSold`; DD&A e impairment aparte, en una extensión.
- **Tenet** — [10-K](https://www.sec.gov/Archives/edgar/data/70318/000007031824000016/): Salaries, wages and benefits → `LaborAndRelatedExpense`; Supplies → `SuppliesExpense`; Other operating → `OtherCostAndExpenseOperating`; D&A.
- **Community Health Systems** — [10-K](https://www.sec.gov/Archives/edgar/data/1108109/000095017024018021/): Salaries → `LaborAndRelatedExpense`; Supplies → **`CostOfGoodsAndServicesSold`**; Other operating → `OtherCostAndExpenseOperating`; Lease cost and rent → `OperatingLeaseExpense`.
- **Universal Health Services** — [10-K](https://www.sec.gov/Archives/edgar/data/352915/000095017024021175/): `LaborAndRelatedExpense`, `OtherCostAndExpenseOperating`, `SuppliesExpense`; Lease and rental expense → `OperatingLeaseExpense`.
- **HCA** — [10-K](https://www.sec.gov/Archives/edgar/data/860730/000095017024016524/): Salaries and benefits → `LaborAndRelatedExpense`; Supplies → `SuppliesExpense`; Other operating → `OtherCostAndExpenseOperating` (la extracción mezcló renglones de más de un reporte; solo se informan los seguros).
- **Brookdale** — [10-K](https://www.sec.gov/Archives/edgar/data/1332349/000133234924000041/): "Costs incurred" (facility operating expense) → `CostOfGoodsAndServicesSold`; Facility operating lease expense → extensión.
- **Quest** — [10-K](https://www.sec.gov/Archives/edgar/data/1022079/000102207924000041/): Cost of services → `CostOfRevenue`, sin ganancia bruta.
- **LabCorp** — [10-K](https://www.sec.gov/Archives/edgar/data/920148/000092014824000014/): Cost of Revenue → `CostOfRevenue`; Gross profit → `GrossProfit`.

Conteos de renglones del estado de resultados ([FSDS](https://www.sec.gov/dera/data/financial-statement-data-sets)):
- E&P, renglón "lease operating": 2022q1 (n=35) `OperatingLeaseExpense` 26, extensión 4, `ResultsOfOperationsProductionOrLiftingCosts` 3, `LeaseCost` 1, `LeaseAndRentalExpense` 1; 2024q1 (n=35) 24 / 5 / 3 / otros 3.
- E&P 2024q1, impuestos a la producción (n=35): `ProductionTaxExpense` 23, extensión 8, `TaxesExcludingIncomeAndExciseTaxes` 3.
- E&P 2024q1, gathering/transportation (n=27): extensión 14, `ResultsOfOperationsTransportationCosts` 8, `CostOfGoodsAndServicesSold` 4.
- Hospitales y geriátricos 2024q1: salarios (n=9) `LaborAndRelatedExpense` 8; insumos (n=8) `SuppliesExpense` 5, extensión 2, `CostOfGoodsAndServicesSold` 1; otros gastos operativos (n=8) `OtherCostAndExpenseOperating` 7.
- Salarios y beneficios ≈45,4 % de los ingresos en HCA y ≈45 % en Tenet (1T-2023, Moody's) — [Becker's](https://www.beckershospitalreview.com/finance/hca-tenet-ebitda-rises-as-labor-costs-cool); [MedCity News](https://medcitynews.com/2023/07/hca-tenet-healthcare-hospital-expense-labor/)

### Inferences
- En E&P el costo de producción se reparte en 3–6 renglones con tags distintos; no hay un tag único de costo de ventas.
- En hospitales no hay una división objetiva entre costo directo y administración.
- El costo de servicios de perforación y laboratorios suele excluir DD&A; por SAB 11.B, "ingresos − costo" con esos tags no es una ganancia bruta GAAP.

### Gaps
- No se revisó cómo etiquetan las E&P chicas con un solo renglón de "production costs".
- Puede haber hechos dimensionales que no están en `num.csv`.

## 3. Elementos us-gaap 2018–2024: deprecaciones de 2018 (ASC 606) y reemplazos

### Takeaway
La taxonomía 2018-01-31 deprecó en bloque los elementos de costo e ingreso específicos de cada industria. El reemplazo oficial es casi siempre un elemento genérico más una dimensión (`CostOfGoodsAndServicesSold` o `RevenueFromContractWithCustomer…` con `ProductOrServiceAxis` y un miembro). Para `LeaseOperatingExpense` el reemplazo indicado es `OperatingLeaseExpense` (arrendamientos ASC 842). Los deprecados de 2018 siguen en el esquema 2018–2020 y no aparecen desde 2021.

### Cited Findings
Fuentes: taxonomías [2018](https://xbrl.fasb.org/us-gaap/2018/us-gaap-2018-01-31.zip), [2019](https://xbrl.fasb.org/us-gaap/2019/us-gaap-2019-01-31.zip), [2020](https://xbrl.fasb.org/us-gaap/2020/us-gaap-2020-01-31.zip), [2021](https://xbrl.fasb.org/us-gaap/2021/us-gaap-2021-01-31.zip), [2022](https://xbrl.fasb.org/us-gaap/2022/us-gaap-2022.zip), [2023](https://xbrl.fasb.org/us-gaap/2023/us-gaap-2023.zip), [2024](https://xbrl.fasb.org/us-gaap/2024/us-gaap-2024.zip) (etiquetas de `us-gaap-lab`, reemplazos de `us-gaap-depcon-def`, presencia en el `.xsd`).

| Deprecado | Fecha | Reemplazo (depcon-def) | En el esquema |
|---|---|---|---|
| CostOfGoodsSold | 2018-01-31 | CostOfGoodsAndServicesSold + ProductMember | 2018–2020 |
| CostOfServices | 2018-01-31 | CostOfGoodsAndServicesSold + ServiceMember | 2018–2020 |
| OilAndGasProductionExpense | 2018-01-31 | CostOfGoodsAndServicesSold + OilAndGasOperationAndMaintenanceMember | 2018–2020 |
| LeaseOperatingExpense ("Oil and Gas Property, Lease Operating Expense") | 2018-01-31 | **OperatingLeaseExpense** (concepto a concepto) | 2018–2020 |
| CostOfGoodsSoldOilAndGas | 2018-01-31 | CostOfGoodsAndServicesSold + OilAndGasMember | 2018–2020 |
| ExplorationAndProductionCosts | 2018-01-31 | CostOfGoodsAndServicesSold + OilAndGasExplorationAndProductionMember | 2018–2020 |
| CostOfPurchasedOilAndGas | 2018-01-31 | CostOfGoodsAndServicesSold + OilAndGasPurchasedMember | 2018–2020 |
| CostOfServicesEnergyServices | 2018-01-31 | CostOfGoodsAndServicesSold + EnergyServiceMember | 2018–2020 |
| CostOfServicesDirectLabor | 2018-01-31 | CostDirectLabor + ServiceMember | 2018–2020 |
| OilAndGasRevenue, OilAndGasSalesRevenue | 2018-01-31 | RevenueFromContractWithCustomerIncludingAssessedTax + OilAndGasMember | 2018–2020 |
| RevenueOilAndGasServices | 2018-01-31 | idem + OilAndGasServiceMember | 2018–2020 |
| HealthCareOrganizationRevenue | 2018-01-31 | idem + HealthCareMember | 2018–2020 |
| HealthCareOrganizationPatientServiceRevenue | 2018-01-31 | idem + HealthCarePatientServiceMember | 2018–2020 |
| HealthCareOrganizationResidentServiceRevenue | 2018-01-31 | idem + HealthCareResidentServiceMember | 2018–2020 |
| HealthCareOrganizationMedicalSuppliesAndDrugsExpense | 2018-01-31 | CostOfGoodsAndServicesSold + HealthCareMember | 2018–2020 |
| CostOfGoodsSoldExcludingDDA / CostOfServicesExcludingDDA | **2019**-01-31 | CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization (+ServiceMember) | 2019–2021 |
| CostOfServicesOilAndGas | 2019-01-31 | CostOfGoodsAndServicesSold + OilAndGasMember | hasta 2021 |

- También deprecados el 2018-01-31: SalesRevenueNet, SalesRevenueGoodsNet, SalesRevenueServicesNet, HealthCareOrganizationPremium/Capitation/OtherRevenue, ExplorationAndProductionRevenue, ExplorationExpenseMining y toda la familia CostOfGoodsSold…/CostOfServices….
- Elementos vigentes en 2024 relevantes:
  - Costo de ventas y márgenes: CostOfGoodsAndServicesSold, CostOfRevenue, CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization, GrossProfit.
  - Familia ASC 932: ResultsOfOperationsProductionOrLiftingCosts (ASC 932-235-50-21/28, 932-235-55-5), ResultsOfOperationsTransportationCosts, ResultsOfOperationsExpenseOther, ResultsOfOperationsDryHoleCosts.
  - ProductionCosts: según su definición es costo de producción *capitalizado*, no el gasto del estado de resultados.
  - Impuestos: ProductionTaxExpense, TaxesExcludingIncomeAndExciseTaxes.
  - Exploración y deterioro: ExplorationExpense, ExplorationAbandonmentAndImpairmentExpense, ImpairmentOfOilAndGasProperties.
  - DD&A: DepreciationDepletionAndAmortization, CostDepreciationAmortizationAndDepletion.
  - Agregados: OtherCostAndExpenseOperating, CostsAndExpenses ("Total costs of sales and operating expenses"), OperatingExpenses (incluye SG&A), OperatingCostsAndExpenses (excluye SG&A).
  - Personal e insumos: LaborAndRelatedExpense, SalariesWagesAndOfficersCompensation, SuppliesExpense, CostDirectLabor, CostDirectMaterial.
  - Arrendamientos: OperatingLeaseExpense ("Amount of operating lease expense", ASC 842-20-45-4(b)).
- En 2024 la familia HealthCareOrganization* solo conserva elementos de balance, seguros stop-loss y HealthCareOrganizationExpensesNet/HealthCareCostsGross. SupplyExpense, HealthCareOrganizationSalariesAndBenefits y HealthCareOrganizationSuppliesExpense no existen en ninguna taxonomía 2018–2024.
- Uso real (empresas distintas por año de presentación, `num.csv`): LeaseOperatingExpense 84 (2018) → 7 (2019) → 0 (casi todos con versión us-gaap/2017); OilAndGasProductionExpense 30 → 2 → 0; CostOfServices 30 → 1; CostOfGoodsSold 25 → 1; OilAndGasSalesRevenue 77 → 0; HealthCareOrganizationRevenue 18 → 0; CostOfGoodsAndServicesSold 58, 82, 76, 58, 58, 51, 49 (2018–2024); GrossProfit estable, 41–51 empresas por año.
- FASB depreca elementos todos los años y los quita del esquema cuando la versión que los deprecó deja de estar soportada — [SEC 2026 taxonomy note](https://www.sec.gov/newsroom/whats-new/fasb-technical-other-conforming-improvements-2026-sec-reporting-taxonomy) (solo resumen).

### Inferences
- Los tags sectoriales de costo solo existen en filings de 2018 hechos con la taxonomía 2017. Los deprecados de `costo_ventas` en `src/shared/concepts.py` (CostOfGoodsSold, CostOfServices, CostOfServicesOilAndGas, CostOfGoodsSoldOilAndGas) casi no tienen datos después de 2018.
- Con el reemplazo dimensional, el costo de producción puede estar en CostOfGoodsAndServicesSold *con* ProductOrServiceAxis; si se descartan los hechos con `segments` se pierde, y el total sin dimensión puede ser solo marketing o compras a terceros (Devon, Diamondback, Pioneer).
- **Trampa:** OperatingLeaseExpense es LOE en E&P y alquiler de inmuebles en hospitales (HCA, UHS, CHS).

### Gaps
- No hay release notes en prosa que justifiquen el reemplazo de LeaseOperatingExpense por OperatingLeaseExpense; el dato sale solo del linkbase (igual en 2019 y 2020).
- No se verificó si `num.csv` conserva hechos dimensionales.

## 4. ¿Las E&P crean extensiones propias para LOE después de 2018?

### Takeaway
Una minoría (~10–15 %). La mayoría usa OperatingLeaseExpense. Las extensiones son mucho más comunes en GP&T (~la mitad de esos renglones). No hay guía de FASB ni XBRL US para etiquetar LOE.

### Cited Findings
- 2022q1, 78 E&P con 10-K: 4 usan una extensión con "LeaseOperat" (LeaseOperatingExpenses, OilAndGasPropertyLeaseOperatingExpense, OilAndGasProducingActivitiesLeaseOperatingExpense, DirectCostsOfLeaseOperatingExpenses); 30 reportan OperatingLeaseExpense — [FSDS](https://www.sec.gov/dera/data/financial-statement-data-sets).
- En el renglón del estado de resultados: extensiones 4/35 (2022q1) y 5/35 (2024q1).
- Extensiones de GP&T: GasGatheringAndTransportationCost, GatheringAndProcessingCosts, OilAndGasGatheringTransportationMarketingAndProcessing, MidstreamOperatingExpense, AdValoremTaxes, etc.; en 2024q1, 14 de 27 renglones de GP&T.
- XBRL US DQC_0132 pide usar elementos estándar de arrendamiento en vez de extensiones — [DQC_0132](https://xbrl.us/data-rule/dqc_0132/) (solo resumen).

### Inferences
- El uso de OperatingLeaseExpense para LOE probablemente se debe al reemplazo explícito de FASB y a la presión por usar elementos estándar (inferencia sin documento).
- Las extensiones de GP&T existen porque no hay un elemento estándar de GP&T para el estado de resultados.

### Gaps
- No hay implementation guide de oil & gas. Solo se analizaron dos trimestres.

## 5. Métricas que reemplazan al margen bruto

### Takeaway
- **E&P:** netback / margen de caja por Boe = precio realizado − LOE − impuestos a la producción − GP&T (a veces también regalías y coberturas). No-GAAP, definición propia de cada empresa.
- **Hospitales:** margen EBITDA ajustado, salarios/ingresos e insumos/ingresos.

### Cited Findings
- Netback — [CFI](https://corporatefinanceinstitute.com/resources/valuation/netback/) (solo resumen); [Market Realist, COP](https://marketrealist.com/2017/06/chart-in-focus-conocophillipss-operating-netback); variantes con regalías y "cash netback" (resta G&A y gastos financieros) — [BOE Report/Cequence](https://boereport.com/2020/03/10/cequence-energy-announces-fourth-quarter-financial-results-and-2019-reserves/).
- Tenet publica Adjusted EBITDA margin por segmento, ~12–14 % en hospitales — [Tenet Q4-2024 supplemental](https://s23.q4cdn.com/674051945/files/doc_financials/2024/q4/Tenet-Fourth-Quarter-2024-Supplemental-Financial-Disclosures.pdf) (resumen del buscador; un 42,1 % que aparecía no está verificado, probablemente del segmento ambulatorio).
- Moody's sigue salarios/ingresos y EBITDA de HCA y Tenet — [Becker's](https://www.beckershospitalreview.com/finance/hca-tenet-ebitda-rises-as-labor-costs-cool).
- Márgenes que excluyen D&A = no-GAAP (SAB 11.B) — [Deloitte 4.9](https://dart.deloitte.com/USDART/home/accounting/sec/sec-reporting-interpretations-manual/roadmap-non-gaap-financial-measures/chapter-4-non-gaap-measures-that/4-9-non-gaap-measures-that).

### Inferences — qué se puede construir desde XBRL
- **Laboratorios, consultorios, atención domiciliaria, servicios petroleros:** sí: GrossProfit, o Revenues − CostOfRevenue/CostOfGoodsAndServicesSold, controlando si el costo excluye DD&A.
- **E&P:** no hay ganancia bruta; Revenues − CostOfGoodsAndServicesSold es engañoso. Se puede construir un margen de caja de producción: ingresos de petróleo y gas − (OperatingLeaseExpense / ResultsOfOperationsProductionOrLiftingCosts / extensión de LOE) − ProductionTaxExpense/TaxesExcludingIncomeAndExciseTaxes − (ResultsOfOperationsTransportationCosts / extensión de GP&T). Exige mapear empresa por empresa. El netback por Boe necesita volúmenes, que no están en el estado de resultados.
- **Hospitales y geriátricos:** no hay ganancia bruta; ingresos − (salarios + insumos + otros) ≈ EBITDAR. Construible: margen operativo, LaborAndRelatedExpense/ingresos, SuppliesExpense/ingresos (en CHS el tag es CostOfGoodsAndServicesSold), EBITDA aproximado = OperatingIncomeLoss + D&A. Ojo: Brookdale etiqueta su facility operating expense como CostOfGoodsAndServicesSold, así que un cálculo mecánico le asignaría una "ganancia bruta" no comparable.

### Gaps
- No hay una definición primaria de "cash margin" en 10-K de E&P de EE.UU.
- No hay márgenes EBITDA verificados de HCA, CHS ni UHS para 2018–2024.
