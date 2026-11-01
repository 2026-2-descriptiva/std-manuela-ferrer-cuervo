
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 09: Extracción del año de una fecha
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_09():
    """
    Extrae el año de las fechas de la columna c3
    y lo incorpora en una nueva columna llamada year.

    Retorna el DataFrame completo, conservando las
    columnas originales y el año como texto.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla original con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Convertir las fechas a formato de texto
    fechas = tabla["c3"].astype(str)

    # Manu: Extraer los cuatro caracteres correspondientes al año
    anios = fechas.str.slice(0, 4)

    # Manu: Incorporar la nueva columna al final de la tabla
    resultado = tabla.assign(year=anios)

    return resultado

