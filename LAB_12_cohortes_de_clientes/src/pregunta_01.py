
# ============================================================
# LAB 12 - COHORTES DE CLIENTES
# Manu | Pregunta 01: Análisis de retención de clientes
# ============================================================

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def build_cohort_analysis() -> pd.DataFrame:
    """
    Analiza la retención de clientes a partir de su
    primera compra.

    Agrupa los clientes por cohorte mensual, calcula
    su tasa de retención y genera una tabla y un
    mapa de calor con los resultados.
    """

    # ========================================================
    # 1. CARGA Y PREPARACIÓN DE LOS DATOS
    # ========================================================

    # Manu: Identificar las rutas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parent.parent

    ruta_datos = ruta_laboratorio / "data" / "sales.csv.gz"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta de resultados
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Cargar el archivo de ventas comprimido
    ventas = pd.read_csv(ruta_datos, compression="gzip")

    # Manu: Convertir las fechas de compra a formato mensual
    ventas["periodo_compra"] = (
        pd.to_datetime(ventas["OrderDate"]).dt.to_period("M")
    )

    # ========================================================
    # 2. IDENTIFICACIÓN DE LAS COHORTES
    # ========================================================

    # Manu: Identificar el primer mes de compra de cada cliente
    ventas["periodo_cohorte"] = (
        ventas.groupby("CustomerID")["periodo_compra"]
        .transform("min")
    )

    # Manu: Representar la cohorte con formato AAAA-MM
    ventas["cohort_month"] = (
        ventas["periodo_cohorte"].astype(str)
    )

    # Manu: Calcular los meses transcurridos desde la primera compra
    ventas["period_index"] = (
        (ventas["periodo_compra"].dt.year
         - ventas["periodo_cohorte"].dt.year) * 12
        +
        (ventas["periodo_compra"].dt.month
         - ventas["periodo_cohorte"].dt.month)
    )

    # ========================================================
    # 3. CÁLCULO DE CLIENTES ACTIVOS Y TAMAÑO DE COHORTE
    # ========================================================

    # Manu: Contar los clientes distintos de cada cohorte
    tamanos_cohorte = (
        ventas.groupby("cohort_month")["CustomerID"]
        .nunique()
        .to_dict()
    )

    # Manu: Contar clientes activos por cohorte y período
    tabla_retencion = (
        ventas.groupby(["cohort_month", "period_index"])["CustomerID"]
        .nunique()
        .reset_index()
        .rename(columns={"CustomerID": "active_customers"})
        .sort_values(["cohort_month", "period_index"])
        .reset_index(drop=True)
    )

    # Manu: Incorporar el tamaño original de cada cohorte
    tabla_retencion["cohort_size"] = (
        tabla_retencion["cohort_month"].map(tamanos_cohorte)
    )

    # Manu: Calcular la tasa de retención
    tabla_retencion["retention_rate"] = (
        tabla_retencion["active_customers"]
        / tabla_retencion["cohort_size"]
    )

    # ========================================================
    # 4. ORGANIZACIÓN Y EXPORTACIÓN DEL ARCHIVO CSV
    # ========================================================

    # Manu: Conservar las columnas en el orden solicitado
    columnas_resultado = [
        "cohort_month",
        "period_index",
        "active_customers",
        "cohort_size",
        "retention_rate",
    ]

    tabla_retencion = tabla_retencion[columnas_resultado]

    # Manu: Guardar la tabla sin el índice de Pandas
    tabla_retencion.to_csv(
        ruta_entregables / "cohort_retention.csv",
        index=False,
        encoding="utf-8"
    )

    # ========================================================
    # 5. CONSTRUCCIÓN DE LA MATRIZ DE RETENCIÓN
    # ========================================================

    # Manu: Organizar las cohortes en filas y períodos en columnas
    matriz_retencion = tabla_retencion.pivot(
        index="cohort_month",
        columns="period_index",
        values="retention_rate"
    )

    # Manu: Mantener vacíos los períodos sin datos observados
    # Pandas conserva estos valores como NaN, no como cero.

    # ========================================================
    # 6. VISUALIZACIÓN DEL MAPA DE CALOR
    # ========================================================

    # Manu: Definir el tamaño y estilo de la figura
    figura, eje = plt.subplots(figsize=(11, 6))

    mapa_calor = eje.imshow(
        matriz_retencion,
        cmap="Blues",
        vmin=0,
        vmax=1,
        aspect="auto"
    )

    # Manu: Configurar los períodos del eje horizontal
    eje.set_xticks(range(len(matriz_retencion.columns)))
    eje.set_xticklabels(matriz_retencion.columns)

    # Manu: Configurar las cohortes del eje vertical
    eje.set_yticks(range(len(matriz_retencion.index)))
    eje.set_yticklabels(matriz_retencion.index)

    # Manu: Agregar los títulos de la visualización
    eje.set_xlabel("Meses desde la primera compra")
    eje.set_ylabel("Mes de la primera compra")
    eje.set_title("Retención mensual de clientes por cohorte")

    # ========================================================
    # 7. PORCENTAJES DENTRO DEL MAPA DE CALOR
    # ========================================================

    # Manu: Escribir la tasa de retención en cada celda observada
    for fila in range(len(matriz_retencion.index)):
        for columna in range(len(matriz_retencion.columns)):

            valor = matriz_retencion.iloc[fila, columna]

            # Manu: No mostrar valores en períodos sin observaciones
            if pd.notna(valor):

                color_texto = (
                    "white" if valor > 0.5 else "black"
                )

                eje.text(
                    columna,
                    fila,
                    f"{valor:.1%}",
                    ha="center",
                    va="center",
                    color=color_texto,
                    fontsize=9
                )

    # Manu: Agregar una escala de colores porcentual
    barra_color = figura.colorbar(mapa_calor, ax=eje)
    barra_color.set_label("Tasa de retención")

    # Manu: Ajustar la distribución de los elementos
    figura.tight_layout()

    # Manu: Guardar el mapa de calor como imagen PNG
    figura.savefig(
        ruta_entregables / "cohort_retention_heatmap.png",
        dpi=150,
        bbox_inches="tight"
    )

    # Manu: Cerrar la figura para liberar memoria
    plt.close(figura)

    # ========================================================
    # 8. RETORNO DE RESULTADOS
    # ========================================================

    # Manu: Retornar la tabla de retención solicitada
    return tabla_retencion


# Manu: Mantener compatibilidad con las pruebas del laboratorio
pregunta_01 = build_cohort_analysis
