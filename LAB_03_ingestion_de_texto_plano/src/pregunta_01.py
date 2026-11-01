
# ============================================================
# LAB 03 - INGESTIÓN DE TEXTO PLANO
# Manu | Pregunta 01: Transformación de reporte de clústeres
# ============================================================

import re
from pathlib import Path

import pandas as pd


def pregunta_01():
    """
    Convierte un reporte de clústeres de palabras clave
    en un DataFrame de Pandas.

    Extrae el identificador del clúster, la cantidad de
    palabras clave, su porcentaje y las palabras asociadas.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "clusters_report.txt"
    )

    # Manu: Patrón para identificar el inicio de cada clúster
    patron_cluster = re.compile(
        r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$"
    )

    # Manu: Almacenar los clústeres encontrados
    lista_clusters = []
    cluster_actual = None

    # Manu: Leer el reporte línea por línea
    with open(ruta_datos, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            coincidencia = patron_cluster.match(linea)

            if coincidencia:
                # Manu: Guardar el clúster anterior
                if cluster_actual is not None:
                    lista_clusters.append(cluster_actual)

                # Manu: Extraer los datos del nuevo clúster
                cluster_actual = {
                    "cluster": int(coincidencia.group(1)),
                    "cantidad_de_palabras_clave": int(
                        coincidencia.group(2)
                    ),
                    "porcentaje_de_palabras_clave": float(
                        coincidencia.group(3).replace(",", ".")
                    ),
                    "palabras": [coincidencia.group(4).strip()],
                }

            elif cluster_actual is not None and linea.strip():
                # Manu: Agregar las palabras de líneas adicionales
                cluster_actual["palabras"].append(linea.strip())

    # Manu: Incluir el último clúster del reporte
    if cluster_actual is not None:
        lista_clusters.append(cluster_actual)

    # Manu: Preparar los registros del DataFrame
    registros = []

    for cluster in lista_clusters:

        # Manu: Unificar las líneas de palabras clave
        texto_palabras = " ".join(cluster["palabras"])

        # Manu: Normalizar comas y espacios internos
        texto_limpio = ", ".join(
            " ".join(palabra.split())
            for palabra in texto_palabras.split(",")
            if palabra.strip()
        )

        # Manu: Eliminar el punto final del reporte
        if texto_limpio.endswith("."):
            texto_limpio = texto_limpio[:-1].strip()

        # Manu: Construir el registro de cada clúster
        registros.append({
            "cluster": cluster["cluster"],
            "cantidad_de_palabras_clave": (
                cluster["cantidad_de_palabras_clave"]
            ),
            "porcentaje_de_palabras_clave": (
                cluster["porcentaje_de_palabras_clave"]
            ),
            "principales_palabras_clave": texto_limpio,
        })

    # Manu: Crear el DataFrame con las columnas solicitadas
    resultado = pd.DataFrame(
        registros,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    return resultado


