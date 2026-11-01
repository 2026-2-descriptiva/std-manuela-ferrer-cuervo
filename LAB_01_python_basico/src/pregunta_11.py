
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 11: Suma de valores por código
# ============================================================

import gzip
from pathlib import Path
from collections import defaultdict


def pregunta_11():
    """
    Calcula la suma de los valores de cada registro según
    los códigos presentes en la cuarta columna.

    Devuelve un diccionario con los códigos ordenados
    alfabéticamente y sus respectivas sumas.
    """

    # Manu: Ubicación del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Diccionario para acumular las sumas por código
    suma_por_codigo = defaultdict(int)

    # Manu: Lectura y procesamiento de los registros
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")

            valor = int(columnas[1])
            codigos = set(columnas[3].split(","))

            # Manu: Sumar el valor a cada código único del registro
            for codigo in codigos:
                suma_por_codigo[codigo] += valor

    # Manu: Organizar las claves alfabéticamente
    return dict(sorted(suma_por_codigo.items()))

