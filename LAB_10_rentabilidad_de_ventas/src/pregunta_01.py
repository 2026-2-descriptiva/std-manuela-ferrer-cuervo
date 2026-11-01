
# ============================================================
# LAB 10 - RENTABILIDAD DE VENTAS
# Manu | Pregunta 01: Análisis de rentabilidad y pérdidas
# ============================================================

from pathlib import Path

import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Analiza la rentabilidad de las ventas de una cadena
    de suministros de oficina.

    Construye un resumen general, un análisis por descuentos
    y una tabla de segmentos prioritarios según sus pérdidas.

    Guarda los tres resultados en la carpeta submission.
    """

    # Manu: Definir las rutas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parents[1]
    ruta_datos = ruta_laboratorio / "data" / "superstore_orders.csv.gz"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta para los resultados
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Leer el archivo comprimido con su formato original
    tabla = pd.read_csv(
        ruta_datos,
        sep=";",
        decimal=",",
        compression="gzip"
    )

    # ========================================================
    # 1. RESUMEN GENERAL DE RENTABILIDAD
    # ========================================================

    # Manu: Calcular los indicadores principales
    cantidad_lineas = int(len(tabla))
    cantidad_pedidos = int(tabla["Order ID"].nunique())

    ventas_totales = float(tabla["Sales"].sum())
    utilidad_total = float(tabla["Profit"].sum())

    # Manu: Calcular el margen sobre las ventas
    margen_general = (
        utilidad_total / ventas_totales
        if ventas_totales != 0 else 0.0
    )

    # Manu: Identificar las líneas que generan pérdidas
    mascara_perdidas = tabla["Profit"] < 0

    lineas_con_perdida = int(mascara_perdidas.sum())

    proporcion_perdidas = (
        lineas_con_perdida / cantidad_lineas
        if cantidad_lineas != 0 else 0.0
    )

    # Manu: Expresar las pérdidas acumuladas en positivo
    perdidas_acumuladas = float(
        tabla.loc[mascara_perdidas, "Profit"].abs().sum()
    )

    # Manu: Construir la tabla de resumen general
    resumen_rentabilidad = pd.DataFrame([{
        "lines": cantidad_lineas,
        "orders": cantidad_pedidos,
        "sales": ventas_totales,
        "profit": utilidad_total,
        "profit_margin": margen_general,
        "loss_lines": lineas_con_perdida,
        "loss_line_rate": proporcion_perdidas,
        "lost_profit": perdidas_acumuladas,
    }])

    # ========================================================
    # 2. RENTABILIDAD POR RANGO DE DESCUENTO
    # ========================================================

    # Manu: Clasificar los descuentos según los rangos
    def clasificar_descuento(descuento):
        if descuento == 0:
            return "0%"
        elif descuento <= 0.05:
            return "1%-5%"
        elif descuento <= 0.10:
            return "6%-10%"
        else:
            return "más de 10%"

    tabla["discount_band"] = (
        tabla["Discount"].apply(clasificar_descuento)
    )

    # Manu: Conservar el orden de los rangos solicitado
    orden_descuentos = [
        "0%",
        "1%-5%",
        "6%-10%",
        "más de 10%",
    ]

    # Manu: Almacenar los indicadores por descuento
    registros_descuentos = []

    for rango in orden_descuentos:

        # Manu: Seleccionar las líneas del rango
        grupo = tabla.loc[tabla["discount_band"] == rango]

        total_lineas = int(len(grupo))
        total_ventas = float(grupo["Sales"].sum())
        total_utilidad = float(grupo["Profit"].sum())

        # Manu: Calcular el margen del rango
        margen = (
            total_utilidad / total_ventas
            if total_ventas != 0 else 0.0
        )

        # Manu: Calcular la frecuencia y monto de pérdidas
        lineas_negativas = grupo["Profit"] < 0

        cantidad_negativas = int(lineas_negativas.sum())

        tasa_perdidas = (
            cantidad_negativas / total_lineas
            if total_lineas != 0 else 0.0
        )

        monto_perdidas = float(
            grupo.loc[lineas_negativas, "Profit"].abs().sum()
        )

        # Manu: Registrar los indicadores de cada rango
        registros_descuentos.append({
            "discount_band": rango,
            "lines": total_lineas,
            "sales": total_ventas,
            "profit": total_utilidad,
            "profit_margin": margen,
            "loss_line_rate": tasa_perdidas,
            "lost_profit": monto_perdidas,
        })

    # Manu: Construir la tabla de descuentos
    resumen_descuentos = pd.DataFrame(registros_descuentos)

    # ========================================================
    # 3. SEGMENTOS PRIORITARIOS POR PÉRDIDAS
    # ========================================================

    # Manu: Agrupar ventas por segmento y categoría
    grupos_segmentos = tabla.groupby(
        ["Customer Segment", "Product Category"]
    )

    registros_segmentos = []

    for (segmento, categoria), grupo in grupos_segmentos:

        cantidad = int(len(grupo))

        # Manu: Considerar solamente grupos con 100 o más líneas
        if cantidad < 100:
            continue

        ventas = float(grupo["Sales"].sum())
        utilidad = float(grupo["Profit"].sum())

        # Manu: Calcular el margen del segmento
        margen_segmento = (
            utilidad / ventas
            if ventas != 0 else 0.0
        )

        # Manu: Acumular únicamente las pérdidas del grupo
        mascara_negativa = grupo["Profit"] < 0

        total_perdidas = float(
            grupo.loc[mascara_negativa, "Profit"].abs().sum()
        )

        registros_segmentos.append({
            "Customer Segment": segmento,
            "Product Category": categoria,
            "lines": cantidad,
            "sales": ventas,
            "profit": utilidad,
            "profit_margin": margen_segmento,
            "lost_profit": total_perdidas,
        })

    # Manu: Seleccionar los cinco segmentos con mayores pérdidas
    segmentos_prioritarios = (
        pd.DataFrame(registros_segmentos)
        .sort_values("lost_profit", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )

    # ========================================================
    # 4. GENERACIÓN DE LOS ENTREGABLES
    # ========================================================

    # Manu: Organizar las tablas para su exportación
    archivos_salida = {
        "profitability_summary.csv": resumen_rentabilidad,
        "discount_summary.csv": resumen_descuentos,
        "priority_segments.csv": segmentos_prioritarios,
    }

    # Manu: Guardar cada tabla sin el índice de Pandas
    for nombre_archivo, resultado in archivos_salida.items():
        ruta_salida = ruta_entregables / nombre_archivo

        resultado.to_csv(
            ruta_salida,
            index=False,
            encoding="utf-8"
        )

    # Manu: Retornar los DataFrames en el orden solicitado
    return (
        resumen_rentabilidad,
        resumen_descuentos,
        segmentos_prioritarios
    )

