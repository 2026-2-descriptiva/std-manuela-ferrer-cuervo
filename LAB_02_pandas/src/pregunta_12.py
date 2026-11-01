
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 12: Combinación de valores por identificador
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_12():
    """
    Combina los valores de las columnas c5a y c5b
    utilizando dos puntos como separador.

    Agrupa los textos por identificador c0 y devuelve
    un DataFrame con las columnas c0 y c5.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl2.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Construir los textos con las columnas c5a y c5b
    tabla["c5"] = (
        tabla["c5a"].astype(str)
        .str.cat(tabla["c5b"].astype(str), sep=":")
    )

    # Manu: Agrupar los textos según su identificador
    grupos_identificadores = tabla.groupby("c0")["c5"]

    # Manu: Ordenar los textos y separarlos mediante comas
    def organizar_metricas(valores):
        textos_ordenados = sorted(valores)
        return ",".join(textos_ordenados)

    # Manu: Consolidar los valores de cada identificador
    resumen_metricas = grupos_identificadores.apply(organizar_metricas)

    # Manu: Convertir el resultado en un DataFrame
    resultado = resumen_metricas.reset_index(name="c5")

    # Manu: Organizar los registros por c0
    resultado = resultado.sort_values("c0").reset_index(drop=True)

    return resultado

