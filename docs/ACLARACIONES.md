# Aclaraciones

## `inpth` en `pre.txt`: la tabla entre paréntesis

`inpth` dice si la línea es del estado principal (`0`) o de su tabla entre paréntesis (`1`).

En el balance impreso, algunas líneas traen números dentro del texto. Ejemplo: la línea 32 del balance del 10-K 2018 de Southwestern Energy (`adsh` `0000007332-19-000010`, zip `2019q1`) dice:

> Common stock, $0.01 par value; 1,250,000,000 shares authorized; issued 585,407,107 shares…

El monto de la línea es el valor contable de las acciones (`CommonStockValue`). Los otros números del texto (valor nominal, acciones autorizadas, acciones emitidas) también son datos XBRL (el formato de etiquetas de los estados contables). La empresa los presenta en un reporte aparte, la tabla «Parenthetical». Ese reporte tiene `inpth=1`:

| report | line | inpth | tag | plabel |
|---|---|---|---|---|
| 5 | 32 | 0 | `CommonStockValue` | Common stock, $0.01 par value; … |
| 6 | 2 | 1 | `CommonStockParOrStatedValuePerShare` | Common stock, par value |
| 6 | 3 | 1 | `CommonStockSharesAuthorized` | Common stock, shares authorized |
| 6 | 4 | 1 | `CommonStockSharesIssued` | Common stock, shares issued |

La prueba 1 de `src/concepts_justification.ipynb` usa solo `inpth=0` por dos razones:
- Las líneas con `inpth=1` no son líneas del estado. Son detalles de una línea: cantidades de acciones, valores por acción, tasas.
- La prueba busca en qué línea está el total, por ejemplo «Total assets». Un total nunca está en la tabla entre paréntesis.
