
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 07: Suma de valores por categoría
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_07():
    """
    Calcula la suma de los valores de la columna c2
    para cada categoría presente en la columna c1.

    Retorna una Serie de Pandas con las categorías
    ordenadas alfabéticamente y sus respectivas sumas.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Agrupar los registros según su categoría
    grupos_categorias = tabla.groupby("c1")

    # Manu: Calcular la suma de los valores de cada grupo
    suma_categorias = grupos_categorias["c2"].sum()

    # Manu: Organizar alfabéticamente las categorías
    resultado = suma_categorias.sort_index()

    return resultado

