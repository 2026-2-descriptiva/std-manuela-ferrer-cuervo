
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 13: Combinación de tablas y suma por categoría
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_13():
    """
    Combina las tablas tbl0.tsv y tbl2.tsv mediante
    la columna c0, compartida por ambas.

    Calcula la suma de c5b para cada categoría de c1
    y retorna una Serie de Pandas ordenada alfabéticamente.
    """

    # Manu: Ubicación de los archivos de datos
    carpeta_datos = Path(__file__).resolve().parents[1] / "data"

    ruta_tabla_0 = carpeta_datos / "tbl0.tsv"
    ruta_tabla_2 = carpeta_datos / "tbl2.tsv"

    # Manu: Lectura de las dos tablas con Pandas
    tabla_principal = pd.read_csv(ruta_tabla_0, sep="\t")
    tabla_complementaria = pd.read_csv(ruta_tabla_2, sep="\t")

    # Manu: Combinar ambas tablas utilizando el identificador c0
    tabla_combinada = tabla_principal.merge(
        tabla_complementaria,
        on="c0",
        how="inner"
    )

    # Manu: Agrupar los registros según su categoría
    grupos_categorias = tabla_combinada.groupby("c1")

    # Manu: Calcular la suma de c5b para cada grupo
    suma_categorias = grupos_categorias["c5b"].sum()

    # Manu: Organizar alfabéticamente las categorías
    resultado = suma_categorias.sort_index()

    return resultado

