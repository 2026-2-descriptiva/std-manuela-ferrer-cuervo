
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 04: Promedio de valores por categoría
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_04():
    """
    Calcula el promedio de los valores de la columna c2
    para cada categoría presente en la columna c1.

    Retorna una Serie de Pandas con las categorías
    ordenadas alfabéticamente.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Agrupar los registros por categoría
    grupos = tabla.groupby("c1")

    # Manu: Calcular el promedio de los valores de c2
    promedio_categorias = grupos["c2"].mean()

    # Manu: Ordenar alfabéticamente las categorías
    resultado = promedio_categorias.sort_index()

    return resultado

