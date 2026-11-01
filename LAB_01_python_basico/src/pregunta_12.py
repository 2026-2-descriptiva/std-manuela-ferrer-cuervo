
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 12: Suma de métricas por letra
# ============================================================

import gzip
from pathlib import Path
from collections import defaultdict


def pregunta_12():
    """
    Calcula la suma de todos los valores numéricos de
    la columna metrics, agrupados por la letra de cada registro.

    Retorna un diccionario con las letras ordenadas
    alfabéticamente y sus respectivas sumas.
    """

    # Manu: Ubicación del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Diccionario para acumular las métricas por letra
    suma_metricas = defaultdict(int)

    # Manu: Lectura y procesamiento de los registros
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            letra = columnas[0]
            metricas = columnas[4].split(",")

            # Manu: Sumar los valores numéricos de cada métrica
            total_registro = 0

            for metrica in metricas:
                clave, valor = metrica.split(":")
                total_registro += int(valor)

            # Manu: Acumular el resultado según la letra
            suma_metricas[letra] += total_registro

    # Manu: Devolver el diccionario ordenado alfabéticamente
    return dict(sorted(suma_metricas.items()))

