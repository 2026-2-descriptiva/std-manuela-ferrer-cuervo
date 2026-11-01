
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 09: Frecuencia de claves en métricas
# ============================================================

import gzip
from pathlib import Path
from collections import Counter


def pregunta_09():
    """
    Cuenta las apariciones de cada clave de la columna metrics
    en todos los registros del archivo.

    Devuelve un diccionario ordenado alfabéticamente
    con la cantidad de apariciones por clave.
    """

    # Manu: Ubicación del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Contador de frecuencia para cada clave
    frecuencia_claves = Counter()

    # Manu: Lectura y extracción de las claves
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            metricas = columnas[4].split(",")

            for metrica in metricas:
                clave, valor = metrica.split(":")
                frecuencia_claves[clave] += 1

    # Manu: Organizar alfabéticamente el diccionario
    return dict(sorted(frecuencia_claves.items()))

