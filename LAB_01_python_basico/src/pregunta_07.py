
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 07: Agrupación de letras por valor
# ============================================================

import gzip
from pathlib import Path
from collections import defaultdict


def pregunta_07():
    """
    Agrupa las letras de la primera columna según el valor
    numérico de la segunda columna.

    Conserva las letras repetidas y su orden de aparición.
    Retorna una lista de tuplas (valor, letras) ordenada
    de menor a mayor valor.
    """

    # Manu: Ruta del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Diccionario para agrupar letras por valor
    letras_por_valor = defaultdict(list)

    # Manu: Lectura y agrupación de registros
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            letra = columnas[0]
            valor = int(columnas[1])

            letras_por_valor[valor].append(letra)

    # Manu: Ordenar por valor numérico y devolver resultados
    return sorted(letras_por_valor.items())

