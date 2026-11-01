
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 01: Suma de valores
# ============================================================

import gzip
from pathlib import Path


def pregunta_01():
    """
    Calcula la suma de los valores de la segunda columna
    del archivo comprimido data.csv.gz.
    """

    # Manu: Ubicación del archivo original
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Lectura y acumulación de los valores
    suma_total = 0

    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            if len(columnas) > 1:
                suma_total += int(columnas[1])

    # Manu: Resultado final
    return suma_total

