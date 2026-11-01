
# ============================================================
# LAB 01 - PYTHON BÁSICO
# Manu | Pregunta 04: Conteo de registros por mes
# ============================================================

import gzip
from pathlib import Path
from collections import Counter


def pregunta_04():
    """
    Cuenta la cantidad de registros correspondientes a cada mes,
    utilizando la fecha de la tercera columna.
    Retorna una lista de tuplas ordenada por mes.
    """

    # Manu: Ruta del archivo comprimido
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"

    # Manu: Contador para almacenar los registros mensuales
    registros_por_mes = Counter()

    # Manu: Lectura de las fechas y extracción del mes
    with gzip.open(ruta_datos, "rt", encoding="utf-8") as archivo:
        for linea in archivo:
            if not linea.strip():
                continue

            columnas = linea.strip().split("\t")
            fecha = columnas[2]
            mes = fecha.split("-")[1]

            registros_por_mes[mes] += 1

    # Manu: Resultados ordenados cronológicamente por mes
    return sorted(registros_por_mes.items())
