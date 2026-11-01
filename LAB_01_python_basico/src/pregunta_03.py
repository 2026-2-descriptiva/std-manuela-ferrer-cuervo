
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 03: Suma de valores por categoría
# ============================================================

import gzip
from pathlib import Path
from collections import defaultdict


def pregunta_03():
    """
    Suma los valores numéricos de cada letra de la primera
    columna y devuelve una lista de tuplas ordenada
    alfabéticamente.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Diccionario para acumular valores por letra
    suma_por_letra = defaultdict(int)

    # Manu: Lectura del archivo y agrupación de los valores
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            letra = columnas[0]
            valor = int(columnas[1])

            suma_por_letra[letra] += valor

    # Manu: Retornar los resultados en orden alfabético
    return sorted(suma_por_letra.items())
