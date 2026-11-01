
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 03: Frecuencia de registros por categoría
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_03():
    """
    Calcula la frecuencia de cada categoría presente
    en la columna c1 de la tabla tbl0.tsv.

    Retorna una Serie de Pandas con las categorías
    ordenadas alfabéticamente.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Contar los registros de cada categoría
    frecuencia_categorias = tabla["c1"].value_counts()

    # Manu: Organizar las categorías alfabéticamente
    resultado = frecuencia_categorias.sort_index()

    return resultado

