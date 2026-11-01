
# ============================================================
# LAB 04 - INGESTIÓN DE TEXTO EN DIRECTORIOS
# Manu | Pregunta 01: Construcción de datasets de sentimientos
# ============================================================

from pathlib import Path

import pandas as pd


def pregunta_01():
    """
    Construye los datasets de entrenamiento y prueba a partir
    de archivos de texto clasificados por sentimiento.

    Guarda los resultados en la carpeta submission con
    las columnas phrase y target, conservando el orden
    alfabético de las carpetas y los archivos.
    """

    # Manu: Definir las carpetas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parents[1]
    ruta_datos = ruta_laboratorio / "data"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta de entrega si no existe
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Procesar por separado entrenamiento y prueba
    for division in ["train", "test"]:

        registros = []
        carpeta_division = ruta_datos / division

        # Manu: Identificar las categorías en orden alfabético
        categorias = sorted(
            carpeta.name
            for carpeta in carpeta_division.iterdir()
            if carpeta.is_dir()
        )

        # Manu: Recorrer las categorías de sentimiento
        for categoria in categorias:
            carpeta_categoria = carpeta_division / categoria

            # Manu: Ordenar alfabéticamente los archivos de texto
            archivos_texto = sorted(
                carpeta_categoria.glob("*.txt")
            )

            # Manu: Leer cada frase y conservar su categoría
            for archivo in archivos_texto:
                frase = archivo.read_text(
                    encoding="utf-8"
                ).strip()

                registros.append({
                    "phrase": frase,
                    "target": categoria
                })

        # Manu: Construir el DataFrame de cada división
        tabla_sentimientos = pd.DataFrame(
            registros,
            columns=["phrase", "target"]
        )

        # Manu: Guardar el CSV sin incluir el índice
        ruta_salida = ruta_entregables / f"{division}_dataset.csv"

        tabla_sentimientos.to_csv(
            ruta_salida,
            index=False
        )

