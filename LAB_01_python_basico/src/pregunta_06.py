
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 06: Mínimos y máximos de métricas
# ============================================================

import gzip
from pathlib import Path
from collections import defaultdict


def pregunta_06():
    """
    Identifica el valor mínimo y máximo de cada clave
    presente en la columna metrics.

    Retorna una lista de tuplas (clave, mínimo, máximo),
    ordenada alfabéticamente.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Diccionario para agrupar los valores por clave
    valores_metricas = defaultdict(list)

    # Manu: Lectura y separación de las métricas
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            pares_metricas = columnas[4].split(",")

            for par in pares_metricas:
                clave, valor = par.split(":")
                valores_metricas[clave].append(int(valor))

    # Manu: Cálculo del mínimo y máximo por clave
    resultados = []

    for clave, valores in sorted(valores_metricas.items()):
        minimo = min(valores)
        maximo = max(valores)

        resultados.append((clave, minimo, maximo))

    return resultados

