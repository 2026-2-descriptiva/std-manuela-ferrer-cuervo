
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 02: Conteo de registros por letra
# ============================================================

import gzip
from pathlib import Path
from collections import Counter


def pregunta_02():
    """
    Cuenta los registros correspondientes a cada letra
    de la primera columna y devuelve una lista de tuplas
    ordenada alfabéticamente.
    """

    # Manu: Ruta del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Inicialización del contador
    conteo_letras = Counter()

    # Manu: Lectura y conteo de los registros
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            columnas = linea.strip().split("\t")

            if columnas[0]:
                conteo_letras[columnas[0]] += 1

    # Manu: Ordenar alfabéticamente y devolver las tuplas
    return sorted(conteo_letras.items())

