
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 08: Creación de columna calculada
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_08():
    """
    Agrega una nueva columna llamada suma a la tabla tbl0.tsv,
    calculando la suma de c0 y c2 para cada registro.

    Retorna el DataFrame completo con la nueva columna
    ubicada al final.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla original con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Calcular la suma de las columnas c0 y c2
    valores_sumados = tabla["c0"].add(tabla["c2"])

    # Manu: Incorporar la columna calculada al final
    tabla = tabla.assign(suma=valores_sumados)

    return tabla

