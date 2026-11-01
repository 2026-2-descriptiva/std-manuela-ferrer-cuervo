
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 02: Cantidad de columnas
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_02():
    """
    Calcula la cantidad total de columnas presentes
    en la tabla tbl0.tsv.

    Retorna el resultado como un número entero.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Identificar la cantidad de columnas
    total_columnas = tabla.shape[1]

    return int(total_columnas)

