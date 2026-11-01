
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 05: Valor máximo por categoría
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_05():
    """
    Identifica el valor máximo de la columna c2
    para cada categoría de la columna c1.

    Retorna una Serie de Pandas con las categorías
    organizadas alfabéticamente.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Agrupar los registros por categoría
    grupos_categorias = tabla.groupby("c1")

    # Manu: Identificar el valor máximo de cada grupo
    maximos_categorias = grupos_categorias["c2"].max()

    # Manu: Organizar los resultados alfabéticamente
    resultado = maximos_categorias.sort_index()

    return resultado

