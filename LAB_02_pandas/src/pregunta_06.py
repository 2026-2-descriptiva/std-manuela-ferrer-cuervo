
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 06: Valores únicos en mayúsculas
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_06():
    """
    Identifica los valores distintos de la columna c4
    de la tabla tbl1.tsv y los convierte a mayúsculas.

    Retorna una lista de valores únicos ordenados
    alfabéticamente.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Convertir los valores de c4 a mayúsculas
    categorias_mayusculas = tabla["c4"].str.upper()

    # Manu: Identificar los valores únicos
    categorias_unicas = categorias_mayusculas.drop_duplicates()

    # Manu: Ordenar alfabéticamente y convertir a lista
    resultado = sorted(categorias_unicas.tolist())

    return resultado

