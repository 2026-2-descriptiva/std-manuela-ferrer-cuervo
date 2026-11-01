
# ============================================================
# LAB 02 - PANDAS
# Manu | Pregunta 11: Agrupación de letras por identificador
# ============================================================

import pandas as pd
from pathlib import Path


def pregunta_11():
    """
    Agrupa las letras de la columna c4 según su identificador c0.

    Ordena las letras alfabéticamente y las une mediante comas.
    Retorna un DataFrame con las columnas c0 y c4,
    organizado de forma ascendente por identificador.
    """

    # Manu: Ubicación del archivo de datos
    ruta_datos = Path(__file__).resolve().parents[1] / "data" / "tbl1.tsv"

    # Manu: Lectura de la tabla con Pandas
    tabla = pd.read_csv(ruta_datos, sep="\t")

    # Manu: Agrupar las letras según su identificador
    grupos_identificadores = tabla.groupby("c0")["c4"]

    # Manu: Función para ordenar y unir las letras
    def organizar_letras(letras):
        letras_ordenadas = sorted(letras)
        return ",".join(letras_ordenadas)

    # Manu: Aplicar la transformación a cada grupo
    letras_agrupadas = grupos_identificadores.apply(organizar_letras)

    # Manu: Recuperar c0 como columna del DataFrame
    resultado = letras_agrupadas.reset_index()

    # Manu: Ordenar los registros por identificador
    resultado = resultado.sort_values("c0").reset_index(drop=True)

    return resultado

