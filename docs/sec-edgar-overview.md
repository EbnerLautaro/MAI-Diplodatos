# Guía de estudio: balances y datos de la SEC

Apuntes para el proyecto del MAI (Módulo de Aplicaciones Integradoras) sobre la base SEC EDGAR. Arranca desde cero en contabilidad y se va ampliando a medida que aparecen conceptos nuevos.

Todos los números de ejemplo son reales. Salen del zip `2026q2.zip` y corresponden a Walmart, al trimestre que terminó el 30 de abril de 2026. Están en **millones de dólares** salvo que se diga otra cosa.

---

## 1. De dónde salen los datos

La **SEC** (Securities and Exchange Commission) es el regulador del mercado de valores de Estados Unidos, el equivalente a la CNV (Comisión Nacional de Valores) en Argentina. Toda empresa que cotiza en una bolsa de Estados Unidos está obligada a presentarle sus estados contables.

Esas presentaciones quedan guardadas en **EDGAR** (Electronic Data Gathering, Analysis and Retrieval), que es el archivo público de la SEC. Cualquiera puede entrar y leer el informe de cualquier empresa.

Los dos documentos que importan para el proyecto son:

- **10-Q**: el informe trimestral. Cada empresa presenta tres por año.
- **10-K**: el informe anual. Es más completo, está auditado, y reemplaza al 10-Q del cuarto trimestre.

Desde 2009 los estados contables se presentan en **XBRL** (eXtensible Business Reporting Language). La idea es que cada número del balance viaje con una etiqueta estándar que dice qué es. En vez de un PDF con la palabra "Total assets" al lado de un número, el archivo dice explícitamente "este número es `Assets`". Eso es lo que permite que una computadora lea miles de balances sin interpretar texto.

Esas etiquetas se llaman **tags**, y vienen de un diccionario común llamado **taxonomía US-GAAP**. GAAP (Generally Accepted Accounting Principles) son las normas contables de Estados Unidos. La taxonomía se actualiza todos los años, por eso los tags vienen con una versión, como `us-gaap/2025`.

Cada tres meses la SEC junta todas las presentaciones XBRL del trimestre, las aplana en tablas, y las publica como un zip. Eso es lo que se descarga desde la página de los Financial Statement Data Sets.

---

## 2. Tres ideas antes de leer un balance

### Stock contra flujo

Hay dos tipos de números en contabilidad y confundirlos es el error más común.

- Un **stock** es una foto a una fecha. "Walmart tenía 289.607 millones en activos el 30 de abril". No tiene duración. Se mide en un instante.
- Un **flujo** es una película entre dos fechas. "Walmart vendió 177.751 millones entre el 1 de febrero y el 30 de abril". Tiene una duración: un trimestre, nueve meses, un año.

El balance contiene stocks. El estado de resultados y el de flujo de efectivo contienen flujos. En los datos de la SEC esto aparece en la columna `qtrs` (cantidad de trimestres que abarca el número): cero para un stock, uno o más para un flujo.

### Devengado contra caja

La contabilidad registra las cosas cuando **ocurren**, no cuando se cobran o se pagan. Esto se llama criterio de **lo devengado**.

Si Walmart le vende a un cliente con tarjeta en abril y la tarjeta le paga en mayo, la venta cuenta como ingreso de abril. La plata entra en mayo. Por eso una empresa puede tener ganancia y quedarse sin caja, o al revés. El estado de flujo de efectivo existe justamente para mostrar la caja real.

### Año fiscal

El **año fiscal** es el período de doce meses que la empresa usa para su contabilidad. No tiene por qué coincidir con el año calendario.

Walmart cierra su año fiscal el 31 de enero. Su "primer trimestre del año fiscal 2027" va de febrero a abril de 2026. Target y Home Depot también cierran en enero, Costco en agosto, y la mayoría de las empresas en diciembre. En el zip, 4.822 de las presentaciones trimestrales y anuales cierran en diciembre, pero hay cientos que cierran en enero, marzo, junio o septiembre.

---

## 3. Los estados contables

Un 10-Q o un 10-K contiene varios estados. En los datos de la SEC cada uno tiene un código de dos letras, que aparece en la columna `stmt` del archivo `pre.txt`.

| código | nombre en inglés | nombre en castellano | qué responde |
|---|---|---|---|
| BS | Balance Sheet | Estado de situación patrimonial, o balance | ¿Qué tiene la empresa y quién lo financió? |
| IS | Income Statement | Estado de resultados | ¿Ganó o perdió plata en el período? |
| CF | Cash Flow | Estado de flujo de efectivo | ¿Cuánta caja entró y salió, y por qué? |
| EQ | Equity | Estado de evolución del patrimonio neto | ¿Cómo cambió lo que es de los accionistas? |
| CI | Comprehensive Income | Estado de resultado integral | Ganancias y pérdidas que no pasan por el resultado |

Los tres primeros son los que se usan para construir ratios. Los otros dos casi no hacen falta para el proyecto.

### 3.1 Balance

El balance es una foto. Muestra, a una fecha, todo lo que la empresa **tiene** y de dónde salió la plata para tenerlo.

Se apoya en una identidad que siempre se cumple, llamada **ecuación contable**:

```
Activo = Pasivo + Patrimonio neto
```

- El **activo** es todo lo que la empresa tiene y le va a generar beneficios: caja, mercadería, edificios, plata que le deben.
- El **pasivo** es todo lo que la empresa debe a terceros: proveedores, bancos, impuestos.
- El **patrimonio neto** es lo que queda para los dueños si se vendiera todo el activo y se pagara todo el pasivo. En inglés se dice *equity* o *stockholders' equity*.

Leído de derecha a izquierda: los activos se financiaron con plata prestada (pasivo) o con plata de los dueños (patrimonio).

#### Activo corriente y no corriente

El activo se divide según cuánto tarda en convertirse en caja.

- **Activo corriente**: lo que se convierte en caja en menos de un año. Caja, cuentas a cobrar, inventario.
- **Activo no corriente**: lo que se usa durante varios años. Edificios, maquinaria, marcas.

Lo mismo con el pasivo:

- **Pasivo corriente**: lo que hay que pagar en menos de un año. Proveedores, sueldos, la cuota de deuda que vence este año.
- **Pasivo no corriente**: deuda de largo plazo.

#### El balance de Walmart

| línea | etiqueta en el balance | tag XBRL | valor |
|---|---|---|---:|
| **Activo corriente** | | | |
| Caja y equivalentes | Cash and cash equivalents | `CashAndCashEquivalentsAtCarryingValue` | 10.729 |
| Cuentas a cobrar | Receivables, net | `ReceivablesNetCurrent` | 10.662 |
| Inventario | Inventories | `InventoryNet` | 62.570 |
| Gastos pagados por adelantado | Prepaid expenses and other | `PrepaidExpenseAndOtherAssetsCurrent` | 4.433 |
| **Total activo corriente** | Total current assets | `AssetsCurrent` | **88.394** |
| **Activo no corriente** | | | |
| Bienes de uso | Property and equipment, net | `PropertyPlantAndEquipmentNet` | 137.789 |
| Derecho de uso por alquileres | Operating lease right-of-use assets | `OperatingLeaseRightOfUseAsset` | 15.220 |
| Derecho de uso por leasing financiero | Finance lease right-of-use assets | `FinanceLeaseRightOfUseAsset` | 6.033 |
| Llave de negocio | Goodwill | `Goodwill` | 28.152 |
| Otros | Other long-term assets | `OtherAssetsNoncurrent` | 14.019 |
| **Total activo** | Total assets | `Assets` | **289.607** |
| **Pasivo corriente** | | | |
| Préstamos de corto plazo | Short-term borrowings | `ShortTermBorrowings` | 10.673 |
| Deudas con proveedores | Accounts payable | `AccountsPayableCurrent` | 62.876 |
| Dividendos a pagar | Dividends payable | `DividendsPayableCurrent` | 5.921 |
| Gastos devengados a pagar | Accrued liabilities | `AccruedLiabilitiesCurrent` | 27.530 |
| Impuestos a pagar | Accrued income taxes | `AccruedIncomeTaxesCurrent` | 1.174 |
| Deuda de largo plazo que vence este año | Long-term debt due within one year | `LongTermDebtCurrent` | 3.896 |
| Alquileres y leasing que vencen este año | Operating/Finance lease obligations | (dos tags) | 2.513 |
| **Total pasivo corriente** | Total current liabilities | `LiabilitiesCurrent` | **114.583** |
| **Pasivo no corriente** | | | |
| Deuda de largo plazo | Long-term debt | `LongTermDebtNoncurrent` | 36.887 |
| Alquileres y leasing de largo plazo | Long-term lease obligations | (dos tags) | 20.210 |
| Impuestos diferidos y otros | Deferred income taxes and other | `DeferredIncomeTaxesAndOtherLiabilitiesNoncurrent` | 16.952 |
| **Patrimonio neto** | | | |
| Capital aportado | Common stock + Capital in excess of par | `CommonStockValue` + `AdditionalPaidInCapital` | 7.694 |
| Resultados acumulados | Retained earnings | `RetainedEarningsAccumulatedDeficit` | 100.241 |
| Otros resultados integrales acumulados | Accumulated other comprehensive loss | `AccumulatedOtherComprehensiveIncomeLossNetOfTax` | −13.605 |
| **Patrimonio de los accionistas de Walmart** | Total Walmart shareholders' equity | `StockholdersEquity` | **94.330** |
| Participación no controladora | Noncontrolling interest | `MinorityInterest` + redeemable | 6.645 |
| **Total pasivo + patrimonio** | | `LiabilitiesAndStockholdersEquity` | **289.607** |

Algunos conceptos de la tabla que vale la pena entender:

- **Inventario** es la mercadería que la empresa compró y todavía no vendió. Para un minorista es el activo más importante del corto plazo. Para una empresa de software es casi cero.
- **Bienes de uso** (en inglés PP&E, Property, Plant and Equipment) son los edificios, terrenos, maquinaria y vehículos. Se muestran "netos", o sea, descontando la **depreciación** acumulada: el desgaste contable que se va restando año a año porque el activo pierde valor con el uso.
- **Derecho de uso** aparece porque desde 2019 los alquileres de largo plazo se registran como si fueran un activo (el derecho a usar el local) y un pasivo (la obligación de pagar el alquiler). Por eso Walmart tiene alquileres tanto del lado del activo como del pasivo.
- **Llave de negocio** (en inglés *goodwill*) aparece cuando una empresa compra otra pagando más que el valor contable de sus activos. Esa diferencia, que representa marca, clientes o sinergias, queda registrada como activo.
- **Gastos devengados a pagar** son gastos que ya ocurrieron pero todavía no se pagaron, como sueldos del mes. Es el criterio de lo devengado aplicado al pasivo.
- **Resultados acumulados** es la suma de todas las ganancias de la historia de la empresa que no se repartieron como dividendos. Es la parte del patrimonio que la empresa generó sola, sin que los accionistas pongan plata.
- **Participación no controladora** (en inglés *noncontrolling interest* o *minority interest*) aparece cuando Walmart es dueña de la mayoría de una subsidiaria pero no del 100 %. Por ejemplo, si tiene el 80 % de una empresa en otro país, el 20 % restante pertenece a otros accionistas. Esa porción figura separada del patrimonio de Walmart.

Comprobando la ecuación contable:

```
Total activo                          289.607
Total patrimonio (incluye minoritarios)  100.682 + 293 redimible
Pasivo total = 289.607 − 100.682 − 293 = 188.632
```

Fijate que Walmart **no informa una línea de "pasivo total"**. Hay que calcularla. En el zip, 618 de las 5.852 presentaciones que informan activo total no informan pasivo total. Es un caso típico de dato que hay que reconstruir.

### 3.2 Estado de resultados

El estado de resultados es una película. Muestra cuánto vendió la empresa en el período y qué se fue restando hasta llegar a la ganancia. Se lee de arriba hacia abajo como una cascada, y por eso cada nivel intermedio tiene nombre propio.

| | etiqueta en el estado | tag XBRL | valor |
|---|---|---|---:|
| Ventas netas | Net sales | `RevenueFromContractWithCustomerExcludingAssessedTax` | 175.684 |
| Otros ingresos (membresías de Sam's Club) | Membership and other income | `OtherIncome` | 2.067 |
| **Ingresos totales** | Total revenues | `Revenues` | **177.751** |
| − Costo de ventas | Cost of sales | `CostOfRevenue` | 133.058 |
| = Margen bruto (no viene informado) | | | 44.693 |
| − Gastos operativos, de venta y administración | Operating, selling, general and administrative | `SellingGeneralAndAdministrativeExpense` | 37.200 |
| **= Resultado operativo** | Operating income | `OperatingIncomeLoss` | **7.493** |
| − Intereses netos | Interest, net | `InterestIncomeExpenseNonoperatingNet` | 620 |
| + Otras ganancias | Other (gains) and losses | `NonoperatingIncomeExpense` | 275 |
| **= Resultado antes de impuestos** | Income before income taxes | `IncomeLossFromContinuingOperationsBeforeIncome...` | **7.148** |
| − Impuesto a las ganancias | Provision for income taxes | `IncomeTaxExpenseBenefit` | 1.658 |
| = Resultado neto consolidado | Consolidated net income | `ProfitLoss` | 5.490 |
| − Parte de los minoritarios | ...attributable to noncontrolling interest | `NetIncomeLossAttributableToNoncontrollingInterest` | 160 |
| **= Resultado neto de Walmart** | ...attributable to Walmart | `NetIncomeLoss` | **5.330** |
| Ganancia por acción | Diluted net income per share | `EarningsPerShareDiluted` | 0,67 USD |

Cada nivel de la cascada mide algo distinto:

- **Ingresos** (en inglés *revenue*, *sales* o *top line*) son las ventas del período. Es la primera línea y la más grande.
- **Costo de ventas** (en inglés COGS, Cost of Goods Sold) es lo que le costó a la empresa la mercadería que vendió. Para Walmart es lo que le pagó al proveedor por los productos que salieron de las góndolas.
- **Margen bruto** es ingresos menos costo de ventas. Mide cuánto le queda a la empresa por cada producto antes de pagar sueldos, alquileres y todo lo demás. Muchas empresas no lo informan como línea separada y hay que calcularlo.
- **Gastos operativos** son los gastos de funcionar: sueldos, alquileres, publicidad, administración. En inglés se agrupan como SG&A (Selling, General and Administrative). En empresas de tecnología aparece además **I+D** (Investigación y Desarrollo, en inglés R&D), con el tag `ResearchAndDevelopmentExpense`. Walmart no lo informa.
- **Resultado operativo** es lo que gana el negocio en sí, antes de pensar en cómo se financia y en impuestos. En inglés se le dice *operating income* o **EBIT** (Earnings Before Interest and Taxes). Es la mejor medida de si el negocio funciona.
- **Intereses** es el costo de la deuda. Walmart pagó 574 por préstamos y 125 por leasing, y cobró 79 de intereses sobre su caja. El neto es 620.
- **Resultado neto** (en inglés *net income*, *earnings* o *bottom line*) es la ganancia final después de todo. Es la última línea y la que va a resultados acumulados del balance.
- **Ganancia por acción** (en inglés EPS, Earnings Per Share) es el resultado neto dividido por la cantidad de acciones. Es el número que los analistas miran en cada presentación de resultados. Se informa "básico" y "diluido". El diluido supone que se ejercen todas las opciones de compra de acciones que tienen los empleados, lo que aumenta la cantidad de acciones.

Otro número que vas a escuchar mucho es el **EBITDA** (Earnings Before Interest, Taxes, Depreciation and Amortization). Es el resultado operativo sumándole la depreciación y la **amortización**, que es lo mismo que la depreciación pero para activos intangibles como software o patentes. La idea es aproximar cuánta caja genera la operación, porque la depreciación es un gasto contable que no implica salida de plata. No viene en el estado de resultados de Walmart. Se calcula con la depreciación que aparece en el estado de flujo de efectivo:

```
EBITDA = 7.493 + 3.821 = 11.314
```

### 3.3 Estado de flujo de efectivo

Este estado muestra cuánta caja real entró y salió en el período. Existe porque el resultado neto, por el criterio de lo devengado, no es caja. Se divide en tres bloques.

| bloque | qué incluye | Walmart |
|---|---|---:|
| **Operativo** | La caja que genera el negocio: cobrar ventas, pagar proveedores y sueldos | +4.738 |
| **Inversión** | Comprar o vender activos de largo plazo: locales, centros de distribución, otras empresas | −6.737 |
| **Financiación** | Pedir o devolver préstamos, pagar dividendos, recomprar acciones | +2.328 |
| Efecto del tipo de cambio | | −331 |
| **Variación de caja** | | **−2** |

En inglés, el flujo operativo se abrevia **CFO** (Cash Flow from Operations). Su tag es `NetCashProvidedByUsedInOperatingActivities`.

El bloque operativo arranca del resultado neto y lo va corrigiendo para llegar a la caja. Vale la pena mirarlo con Walmart:

```
Resultado neto consolidado                5.490
+ Depreciación y amortización             3.821   (gasto contable, no salió plata)
− Aumento de inventario                  −3.833   (compró mercadería y la pagó o la debe)
+ Aumento de deudas con proveedores       1.177   (compró sin pagar todavía)
− Disminución de gastos devengados       −3.351   (pagó cosas que debía)
  ... otros ajustes ...
= Flujo operativo                         4.738
```

A las variaciones de inventario, cuentas a cobrar y deudas con proveedores se las llama **capital de trabajo** (en inglés *working capital*). Es la plata que queda "atrapada" en el ciclo del negocio. En este trimestre Walmart llenó sus depósitos y eso consumió caja.

Un número derivado muy usado es el **flujo de caja libre** (en inglés FCF, Free Cash Flow): flujo operativo menos inversión en bienes de uso. La inversión en bienes de uso se llama **capex** (Capital Expenditure) y su tag es `PaymentsToAcquirePropertyPlantAndEquipment`.

```
Flujo de caja libre = 4.738 − 6.684 = −1.946
```

Walmart tuvo flujo libre negativo este trimestre. Eso no es una alarma para una empresa de este tamaño: el primer trimestre suele tener compras de inventario fuertes. Por eso conviene mirar estos números en series de varios trimestres y no en uno solo.

### 3.4 Cómo se conectan los tres

- El **resultado neto** del estado de resultados se suma a los **resultados acumulados** del balance.
- La **variación de caja** del estado de flujo de efectivo explica cuánto cambió la línea de **caja** del balance entre una fecha y la otra.
- Las variaciones de **inventario, cuentas a cobrar y proveedores** del flujo operativo son la diferencia entre el balance de inicio y el de cierre.

---

## 4. Ratios financieros

Un **ratio** es un cociente entre dos números de los estados contables. Sirve para comparar empresas de distinto tamaño: Walmart vende cien veces más que una cadena regional, pero las dos pueden tener el mismo margen.

Estos son los ratios que aparecen en las tres opciones del proyecto, calculados para Walmart:

| ratio | fórmula | qué mide | Walmart |
|---|---|---|---:|
| Margen bruto | (Ingresos − Costo de ventas) / Ingresos | Cuánto queda por cada dólar vendido después de pagar la mercadería | 25,1 % |
| Margen operativo | Resultado operativo / Ingresos | Cuánto gana el negocio por cada dólar vendido | 4,2 % |
| Margen neto | Resultado neto / Ingresos | Cuánto queda al final por cada dólar vendido | 3,0 % |
| ROA | Resultado neto / Activo total | Cuánto rinde cada dólar de activos | 1,84 % trimestral |
| ROE | Resultado neto / Patrimonio neto | Cuánto rinde cada dólar de los accionistas | 5,65 % trimestral |
| Liquidez corriente | Activo corriente / Pasivo corriente | Si puede pagar lo que vence este año con lo que tiene a corto plazo | 0,77 |
| Endeudamiento | Pasivo total / Activo total | Qué parte de los activos se financia con plata de terceros | 65,1 % |
| Deuda / Patrimonio | Deuda financiera / Patrimonio neto | Cuánta deuda bancaria hay por cada dólar de los accionistas | 0,55 |
| Deuda neta | Deuda financiera − Caja | La deuda que quedaría si se usara toda la caja para pagarla | 40.727 |
| Cobertura de intereses | Resultado operativo / Intereses pagados | Cuántas veces el negocio cubre el costo de su deuda | 10,7 veces |
| Flujo operativo / Ingresos | CFO / Ingresos | Cuánta caja real genera cada dólar vendido | 2,7 % |
| I+D / Ingresos | Gasto en I+D / Ingresos | Cuánto reinvierte en innovación | no aplica |

**ROA** es Return on Assets (rentabilidad sobre activos). **ROE** es Return on Equity (rentabilidad sobre patrimonio). Son los dos ratios de rentabilidad más usados y son los que las tres opciones del proyecto usan como variable objetivo.

La **deuda financiera** es la deuda con bancos y bonistas, sin contar proveedores. Para Walmart suma préstamos de corto plazo, la porción corriente de la deuda de largo plazo y la deuda de largo plazo: 10.673 + 3.896 + 36.887 = 51.456. Hay quienes también suman los leasing; es una decisión que hay que documentar.

Algunas cosas a tener en cuenta al usar ratios:

- **Anualizar.** El ROA y el ROE calculados con un trimestre de ganancia dan números chicos. Para compararlos con cifras anuales se multiplican por cuatro: el ROE de Walmart anualizado es 22,6 %. Lo importante es ser consistente.
- **Promedio o cierre.** Los ratios que mezclan un flujo (resultado neto) con un stock (activo o patrimonio) se calculan mejor con el promedio del stock entre el inicio y el cierre del período. Con el valor de cierre es más simple y suele alcanzar.
- **Denominadores negativos.** Una empresa con patrimonio neto negativo, algo común en empresas que recompraron muchas acciones o acumularon pérdidas, da un ROE sin sentido. Una pérdida dividida por patrimonio negativo da un ROE positivo. Hay que detectar y tratar esos casos.
- **El sector cambia todo.** La liquidez corriente de Walmart es 0,77, que en un manual diría "peligro". Pero Walmart vende la mercadería antes de pagarle al proveedor, así que vive bien con eso. Un supermercado y una empresa de software tienen márgenes, inventarios y deudas completamente distintos. Por eso los ratios se comparan dentro del mismo sector.

---

## 5. Los archivos del zip

Cada zip trimestral trae cuatro archivos de texto separados por tabulador, con la primera fila como encabezado, más un `readme.htm` con la documentación oficial. Juntos son cuatro tablas de una base de datos relacional.

```
                 sub.txt
           (una fila por documento)
                    │ adsh
        ┌───────────┴───────────┐
        ▼                       ▼
     num.txt                 pre.txt
  (los números)        (dónde y cómo se mostraron)
        │ tag + version         │ tag + version
        └───────────┬───────────┘
                    ▼
                 tag.txt
         (diccionario de etiquetas)
```

La columna que une todo es **`adsh`**, el *accession number* o número de acceso. Es el identificador único que EDGAR le asigna a cada documento presentado, parecido a un número de expediente. Tiene la forma `0000104169-26-000102`: los primeros diez dígitos identifican a quien presentó, los dos del medio el año, y los últimos seis son correlativos. Cada 10-Q de cada empresa tiene su propio `adsh`.

### sub.txt: los documentos presentados

"Sub" viene de *submissions*, presentaciones. Tiene una fila por documento, 7.714 en este zip. Es la tabla para elegir qué empresas y qué períodos entran al proyecto.

| columna | qué es | ejemplo Walmart |
|---|---|---|
| `adsh` | Número de acceso del documento | 0000104169-26-000102 |
| `cik` | Número que identifica a la empresa en la SEC. A diferencia del `adsh`, es el mismo en todas sus presentaciones. CIK es Central Index Key | 104169 |
| `name` | Razón social a la fecha de presentación | WALMART INC. |
| `sic` | Código de sector. SIC es Standard Industrial Classification: cuatro dígitos que indican la industria | 5331 (tiendas de variedades) |
| `form` | Tipo de documento | 10-Q |
| `period` | Fecha de cierre del balance, redondeada a fin de mes | 20260430 |
| `fy` | Año fiscal al que corresponde | 2027 |
| `fp` | Período dentro del año fiscal: Q1, Q2, Q3 o FY para el anual | Q1 |
| `fye` | Mes y día de cierre del año fiscal | 0131 |
| `filed` | Fecha en que se presentó | 20260529 |
| `prevrpt` | Vale 1 si este documento fue reemplazado después por una corrección | 0 |
| `afs` | Categoría de la empresa según su tamaño. `1-LAF` son las más grandes, `5-SML` las más chicas | 1-LAF |
| `former`, `changed` | Nombre anterior y fecha del cambio, si la empresa cambió de nombre | WAL MART STORES INC, 19920703 |
| `countryba`, `stprba`, `cityba`... | Dirección comercial: país, estado, ciudad, código postal. Las que terminan en `ma` son la dirección postal | US, AR, BENTONVILLE |
| `countryinc`, `stprinc` | País y estado donde está constituida legalmente | US, DE |
| `instance` | Nombre del archivo XBRL original. Suele empezar con el *ticker*, el código con el que cotiza en bolsa | wmt-20260430_htm.xml |

El código SIC es lo que define las opciones del proyecto. Los rangos que importan son:

| rango SIC | sector | opción |
|---|---|---|
| 5200–5999 | Comercio minorista | 1 |
| 7370–7379 | Software y servicios informáticos | 2 |
| 8000–8099 | Servicios de salud | 3 |
| 1300–1399 | Extracción de petróleo y gas | 3 |

### num.txt: los números

Es la tabla principal, con 3,6 millones de filas en este zip. Cada fila es un número que apareció en algún estado contable de algún documento.

| columna | qué es | ejemplo |
|---|---|---|
| `adsh` | Documento al que pertenece | 0000104169-26-000102 |
| `tag` | Etiqueta XBRL del concepto | Revenues |
| `version` | Versión de la taxonomía. Si el tag es inventado por la empresa, acá va su `adsh` | us-gaap/2025 |
| `ddate` | Fecha de cierre del período del número | 20260430 |
| `qtrs` | Duración en trimestres. 0 es un stock, 1 un trimestre, 4 un año | 1 |
| `uom` | Unidad de medida. Casi siempre USD; para cantidad de acciones es `shares`, para ganancia por acción `USD/shares` | USD |
| `segments` | Vacío si el número es de la empresa entera. Si tiene algo, es un desglose por unidad de negocio, región o producto | (vacío) |
| `coreg` | Vacío si el número es del grupo consolidado. Si tiene algo, es de una entidad específica dentro del grupo | (vacío) |
| `value` | El número, sin escalar: en dólares, no en millones | 177751000000 |
| `footnote` | Texto de la nota al pie, si la hay | |

Un mismo documento trae varios valores del mismo tag. El 10-Q de Walmart informa `Revenues` del trimestre actual y del mismo trimestre del año anterior, para que se puedan comparar. Lo que distingue a cada uno es `ddate`.

Cuando se arma la tabla para el proyecto, cada valor queda identificado por cinco cosas: la empresa (vía `adsh` → `cik`), el tag, la fecha `ddate`, la duración `qtrs`, y que `segments` y `coreg` estén vacíos.

### tag.txt: el diccionario

Tiene una fila por cada etiqueta usada en el trimestre, con su definición. Sirve para saber qué significa un tag que no conocés.

| columna | qué es | ejemplo para `Revenues` |
|---|---|---|
| `tag` | Nombre de la etiqueta | Revenues |
| `version` | Taxonomía de origen, o `adsh` si es inventada | us-gaap/2025 |
| `custom` | 1 si la inventó una empresa, 0 si es estándar | 0 |
| `abstract` | 1 si es un título de sección sin número asociado | 0 |
| `datatype` | Tipo de dato: `monetary`, `shares`, `perShare`, `percent`... | monetary |
| `iord` | `I` si es un stock (instante), `D` si es un flujo (duración) | D |
| `crdr` | Saldo natural de la cuenta: `D` deudor o `C` acreedor | C |
| `tlabel` | Nombre legible | Revenues |
| `doc` | Definición completa en inglés | Amount of revenue recognized from goods sold... |

La columna `crdr` viene de la **partida doble**, el sistema de registro de la contabilidad. Cada cuenta tiene un saldo "normal". Los activos y los gastos tienen saldo **deudor** (`D`). Los pasivos, el patrimonio y los ingresos tienen saldo **acreedor** (`C`). En la práctica sirve para saber si un número positivo suma o resta: un `CostOfRevenue` positivo es un gasto, que se resta de los ingresos.

El 90 % de las filas de este archivo son tags inventados por alguna empresa, porque la taxonomía estándar no tenía uno que le sirviera. Pero en `num.txt` solo el 8,5 % de los números usa un tag inventado. Para los ratios del proyecto alcanza con los estándar.

### pre.txt: cómo se presentaron

"Pre" viene de *presentation*. Tiene una fila por cada renglón de cada estado contable, con el texto que la empresa escribió. Sirve para entender qué tag eligió cada empresa para cada concepto, y para reconstruir el estado contable en orden.

| columna | qué es | ejemplo |
|---|---|---|
| `adsh` | Documento | 0000104169-26-000102 |
| `report` | Número de estado dentro del documento | 2 |
| `line` | Número de renglón dentro del estado | 6 |
| `stmt` | Qué estado es: BS, IS, CF, EQ, CI. Ver la tabla de la sección 3 | IS |
| `inpth` | 1 si el número se mostró entre paréntesis dentro de otro renglón, como "Cuentas a cobrar (neto de previsión de 200)" | 0 |
| `rfile` | Formato del archivo original, sin importancia para el proyecto | H |
| `tag` | Etiqueta usada en ese renglón | CostOfRevenue |
| `version` | Versión de la taxonomía | us-gaap/2025 |
| `plabel` | El texto del renglón como lo escribió la empresa | Cost of sales |
| `negating` | 1 si el número se muestra con el signo invertido | 0 |

El mismo tag puede aparecer en dos estados. El resultado neto aparece en el estado de resultados y también como primer renglón del flujo de efectivo.

La columna `negating` importa para el signo. En el flujo de Walmart, el aumento de inventario está guardado en `num.txt` como +3.833 pero se muestra como (3.833), porque comprar inventario consume caja. Para los ratios se usa el valor de `num.txt`, pero hay que saber qué significa su signo para cada tag.

### Un ejemplo de cómo se cruzan

```python
import pandas as pd

d = "materiales/MAI/tmp"
sub = pd.read_csv(f"{d}/sub.txt", sep="\t", dtype=str)
num = pd.read_csv(f"{d}/num.txt", sep="\t", dtype=str)

# 1. Elegir documentos: retail, trimestrales o anuales
sub["sic"] = pd.to_numeric(sub["sic"])
docs = sub[sub["sic"].between(5200, 5999) & sub["form"].isin(["10-Q", "10-K"])]

# 2. Quedarse con los números de esos documentos, solo consolidados
n = num[num["adsh"].isin(docs["adsh"]) & num["segments"].isna() & num["coreg"].isna()]

# 3. Un concepto: ingresos del trimestre
rev = n[(n["tag"] == "Revenues") & (n["qtrs"] == "1")]
rev = rev.merge(docs[["adsh", "cik", "name", "fy", "fp"]], on="adsh")
```

El repositorio oficial de la SEC con notebooks de ejemplo está en <https://github.com/sec-gov/python-for-dera-financial-datasets>. La documentación de las columnas está en <https://www.sec.gov/files/financial-statement-data-sets.pdf> y en el `readme.htm` del zip.

---

## 6. Trampas al armar el dataset

Cosas que no son obvias y que, si se ignoran, generan números incorrectos sin dar error.

- **El zip es por fecha de presentación.** `2026q2.zip` contiene lo que se presentó entre abril y junio de 2026, sin importar a qué período corresponda. Para tener balances de 2015 a 2023 hay que bajar los zips desde `2015q2` hasta `2024q1` o `2024q2`, porque los informes anuales se presentan hasta 90 días después del cierre.

- **El cuarto trimestre casi nunca viene solo.** El 10-K trae el año completo (`qtrs=4`). Para tener el cuarto trimestre de un flujo hay que restar: año completo menos los tres trimestres anteriores, o año menos el acumulado a nueve meses. Esto vale para ingresos, resultado y flujo de efectivo. Los stocks del balance no tienen este problema.

- **Los 10-Q traen trimestre y acumulado.** El 10-Q del segundo trimestre trae los ingresos del trimestre (`qtrs=1`) y del semestre acumulado (`qtrs=2`). El del tercero trae `qtrs=1` y `qtrs=3`. Si no se filtra por `qtrs`, se mezclan.

- **El estado de flujo de efectivo suele venir solo acumulado.** Muchas empresas informan el flujo de efectivo solo desde el inicio del año fiscal, sin el trimestre aislado. El trimestre se obtiene restando el acumulado del trimestre anterior.

- **Comparativos repetidos.** Cada documento trae también el período del año anterior. El mismo número aparece en dos zips distintos. Hay que quedarse con uno, normalmente el del documento más reciente, porque puede venir corregido.

- **Documentos corregidos.** Si una empresa corrige un 10-Q, presenta uno nuevo (con `form` 10-Q/A) y el viejo queda marcado con `prevrpt=1`. Hay que descartar los marcados.

- **Desgloses mezclados con el total.** De las 381 filas del 10-Q de Walmart, solo 215 son de la empresa entera. El resto tiene `segments` con valores como `BusinessSegments=WalmartInternational`. Sin filtrar `segments` vacío, se suman ventas de Walmart Internacional a las de Walmart total.

- **El mismo concepto con tags distintos.** De las 5.885 presentaciones trimestrales y anuales del zip, 1.848 informan ingresos con `Revenues`, 2.320 con `RevenueFromContractWithCustomerExcludingAssessedTax`, y 1.855 con ninguno de los dos. Para cada variable del proyecto hay que armar una lista de tags posibles en orden de preferencia y documentarla. La consigna del checkpoint 1 lo pide explícitamente.

- **Totales que hay que calcular.** Walmart no informa pasivo total ni margen bruto. Otras empresas no informan resultado operativo. Hay que reconstruirlos a partir de otras líneas.

- **Años fiscales desalineados.** El trimestre febrero–abril de Walmart y el enero–marzo de una empresa que cierra en diciembre son ambos "Q1". Se puede alinear por trimestre fiscal (`fy` + `fp`) o por fecha calendario (`ddate`). Las dos opciones son válidas, pero hay que elegir una y justificarla. Para estudiar el quiebre del COVID, alinear por fecha calendario tiene más sentido.

- **`fy` puede adelantarse.** Walmart llama "año fiscal 2027" al año que termina en enero de 2027, aunque casi todo transcurra en 2026. Otras empresas usan el criterio contrario.

- **Valores sin escalar.** `value` está en dólares, no en miles ni millones. Para leer, dividir por un millón.
