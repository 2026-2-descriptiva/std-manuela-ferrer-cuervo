
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 10: Conteo de códigos y métricas
# ============================================================

import gzip
from pathlib import Path


def pregunta_10():
    """
    Identifica la letra y cuenta los códigos y métricas
    asociados a cada registro del archivo.

    Devuelve una lista de tuplas (letra, cantidad de códigos,
    cantidad de métricas), conservando el orden original.
    """

    # Manu: Ubicación del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Lista para almacenar los resultados
    resumen_registros = []

    # Manu: Lectura y procesamiento de cada fila
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")

            letra = columnas[0]
            codigos = columnas[3].split(",")
            metricas = columnas[4].split(",")

            cantidad_codigos = len(codigos)
            cantidad_metricas = len(metricas)

            resumen_registros.append(
                (letra, cantidad_codigos, cantidad_metricas)
            )

    # Manu: Retornar las tuplas en el orden del archivo
    return resumen_registros

