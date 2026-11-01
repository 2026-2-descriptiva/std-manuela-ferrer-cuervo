
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 05: Valores máximos y mínimos por letra
# ============================================================

import gzip
from pathlib import Path
from collections import defaultdict


def pregunta_05():
    """
    Identifica el valor máximo y mínimo para cada categoría
    de la primera columna.

    Retorna una lista de tuplas (letra, máximo, mínimo)
    organizada alfabéticamente.
    """

    # Manu: Ubicación del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Almacenar los valores asociados a cada letra
    valores_por_letra = defaultdict(list)

    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            letra = columnas[0]
            valor = int(columnas[1])

            valores_por_letra[letra].append(valor)

    # Manu: Calcular máximo y mínimo por categoría
    resultados = []

    for letra, valores in sorted(valores_por_letra.items()):
        maximo = max(valores)
        minimo = min(valores)

        resultados.append((letra, maximo, minimo))

    return resultados
