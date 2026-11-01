
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 08: Letras únicas por valor
# ============================================================

import gzip
from pathlib import Path
from collections import defaultdict


def pregunta_08():
    """
    Agrupa las letras de la primera columna según los valores
    de la segunda columna.

    Elimina las letras repetidas dentro de cada grupo y
    devuelve las listas ordenadas alfabéticamente.
    """

    # Manu: Ubicación del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Agrupar letras únicas para cada valor
    letras_por_valor = defaultdict(set)

    # Manu: Lectura y clasificación de los registros
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            letra = columnas[0]
            valor = int(columnas[1])

            letras_por_valor[valor].add(letra)

    # Manu: Ordenar tanto los valores como las letras
    resultados = []

    for valor, letras in sorted(letras_por_valor.items()):
        resultados.append((valor, sorted(letras)))

    return resultados

