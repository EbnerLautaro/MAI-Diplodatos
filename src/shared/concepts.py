"""Concepto -> tags XBRL en orden de prioridad. Tags de la guía de la mentora y de docs/rumbo-mai.pdf."""

CONCEPTS = {
    # Ingresos netos totales
    "ingresos_netos": [
        "Revenues",
        "SalesRevenueNet",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
    ],
    # Resultado operativo (EBIT)
    "resultado_operativo": ["OperatingIncomeLoss"],
    # Resultado neto (ProfitLoss incluye a los accionistas minoritarios)
    "resultado_neto": ["NetIncomeLoss", "ProfitLoss"],
    # Activos totales
    "activos_totales": ["Assets"],
    # Activos corrientes
    "activos_corrientes": ["AssetsCurrent"],
    # Pasivos totales
    "pasivos_totales": ["Liabilities"],
    # Pasivos corrientes
    "pasivos_corrientes": ["LiabilitiesCurrent"],
    # Patrimonio neto
    "patrimonio_neto": [
        "StockholdersEquity",
        "StockholdersEquityAttributableToParent",
    ],
    # Flujo de caja operativo
    "flujo_caja_operativo": [
        "NetCashProvidedByUsedInOperatingActivities",
        "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
    ],
    # Ganancia bruta. Si falta, build_panel la construye: ingresos_netos - costo_ventas
    "ganancia_bruta": ["GrossProfit"],
    # Caja
    "caja": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],
    # Costo de ventas: solo para construir la ganancia bruta, no queda en el panel
    "costo_ventas": ["CostOfRevenue", "CostOfGoodsSold"],
}

# Conceptos que miden un período (qtrs de 1 a 4). Los demás son saldos a una fecha (qtrs = 0).
FLOWS = [
    "ingresos_netos",
    "resultado_operativo",
    "resultado_neto",
    "flujo_caja_operativo",
    "ganancia_bruta",
    "costo_ventas",
]
