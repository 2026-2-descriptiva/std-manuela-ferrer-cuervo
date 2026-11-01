
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 10: Agrupación de valores en texto
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_10():
    """
    Agrupa los valores de la columna c2 según cada categoría
    de c1, ordenándolos de menor a mayor.

    Une los valores mediante dos puntos y retorna un
    DataFrame con las categorías como índice.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl0.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Agrupar los valores según su categoría
    grupos_categorias = tabla.groupby("c1")["c2"]

    # Manu: Ordenar los valores y unirlos en un texto
    def unir_valores(valores):
        valores_ordenados = sorted(valores)
        valores_texto = [str(valor) for valor in valores_ordenados]
        return ":".join(valores_texto)

    # Manu: Aplicar la transformación a cada categoría
    resumen_categorias = grupos_categorias.apply(unir_valores)

    # Manu: Convertir la Serie en un DataFrame
    resultado = resumen_categorias.to_frame(name="c2")

    return resultado.sort_index()

