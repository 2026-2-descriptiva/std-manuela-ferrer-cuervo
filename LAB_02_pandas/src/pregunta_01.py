
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 01: Cantidad de registros
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_01():
    """
    Calcula la cantidad total de registros de la tabla
    tbl0.tsv y devuelve el resultado como un número entero.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Conteo de registros
    total_registros = tabla.shape[0]

    return int(total_registros)

