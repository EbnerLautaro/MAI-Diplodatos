# Alineacion trimestral

La regla que habiamos dicho era asignarlo al trimestre calendario que contiene la mayoría de esos meses, 2 de 3

┌───────────────┬────────────────────────────┬─────────────────────────────┬─────────────────────┐
│    Cierre     │ Meses del trimestre fiscal │        ¿Dónde caen?         │        Va a         │
├───────────────┼────────────────────────────┼─────────────────────────────┼─────────────────────┤
│ 31 de marzo   │ ene, feb, mar              │ los 3 en Q1                 │ Q1                  │
├───────────────┼────────────────────────────┼─────────────────────────────┼─────────────────────┤
│ 31 de enero   │ nov, dic, ene              │ 2 en Q4, 1 en Q1            │ Q4 del año anterior │
├───────────────┼────────────────────────────┼─────────────────────────────┼─────────────────────┤
│ 28 de febrero │ dic, ene, feb              │ 1 en Q4, 2 en Q1            │ Q1                  │
└───────────────┴────────────────────────────┴─────────────────────────────┴─────────────────────┘

# Quiebra: no se sale

Una empresa que quiebra no vuelve a salir de la quiebra. Desde el trimestre del primer 8-K con el ítem 1.03 (pedido de quiebra) queda sin datos y marcada como quebrada. Los 8-K posteriores (aprobación del plan, salida de la reorganización) no cuentan.

Ejemplo: Gulfport Energy pidió la quiebra el 2020-11-16 (2020Q4) y el plan se aprobó el 2021-04-29. En el panel su última fila es 2020Q3 y `fecha_quiebra` = 2020-11-16. Aunque siguió presentando 10-Q en 2021, esos datos no se usan, y el 8-K de 2021 tampoco cuenta como otra quiebra.

Consecuencia en `03_bankruptcy.ipynb`: alcanza con el primer 8-K con el ítem 1.03 dentro del período. La regla de 2 años (`NEW_CASE_GAP`) solo sirve para ignorar los 8-K de una quiebra que empezó antes de 2018. Por ejemplo, un pedido en 2017 con el plan aprobado en 2018: el 8-K de 2018 no es una quiebra nueva.

# Variable costo de ventas
En la reunion nunca hablamos de esa variable, pero se usa para calcular ganacia bruta (`ganancia bruta = ingresos netos - costo de ventas`). En este momento se utiliza solo para eso, es decir, la obtenemos, la usamos si corresponde y luego la borramos (no aparece en la lista de las cosas). Quieren que la agreguemos? Vale la pena?