
# ============================================================
# LAB 06 - LIMPIEZA DE SOLICITUDES DE CRÉDITO
# Manu | Pregunta 01: Construcción del dataset limpio
# ============================================================

from pathlib import Path

import pandas as pd


def pregunta_01():
    """
    Limpia la información de las solicitudes de crédito.

    Corrige formatos de texto, fechas y valores numéricos,
    elimina registros incompletos y duplicados, conservando
    los faltantes válidos de comuna_ciudadano.

    Guarda el dataset limpio en la carpeta submission.
    """

    # Manu: Definir las rutas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parents[1]
    ruta_datos = ruta_laboratorio / "data" / "solicitudes_de_credito.csv.gz"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta de entrega
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Definir las nueve columnas solicitadas
    columnas_finales = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]

    # Manu: Leer el archivo y excluir la columna de índice original
    tabla = pd.read_csv(
        ruta_datos,
        sep=";",
        index_col=0,
        encoding="utf-8"
    )

    # Manu: Asignar los nombres de las columnas
    tabla.columns = columnas_finales

    # Manu: Identificar los campos obligatorios
    columnas_obligatorias = [
        columna
        for columna in columnas_finales
        if columna != "comuna_ciudadano"
    ]

    # Manu: Eliminar registros incompletos, excepto los de comuna
    tabla = tabla.dropna(
        subset=columnas_obligatorias
    ).copy()

    # Manu: Seleccionar las columnas que contienen texto
    columnas_texto = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]

    # Manu: Estandarizar los textos en minúsculas y con espacios
    for columna in columnas_texto:
        tabla[columna] = (
            tabla[columna]
            .astype(str)
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.replace("_", " ", regex=False)
            .str.split()
            .str.join(" ")
        )

    # Manu: Convertir el estrato a número entero
    tabla["estrato"] = tabla["estrato"].astype(int)

    # Manu: Estandarizar las fechas
    def organizar_fecha(fecha):
        texto_fecha = str(fecha).strip().replace("-", "/")
        partes = texto_fecha.split("/")

        if len(partes) == 3:
            if len(partes[0]) == 4:
                anio, mes, dia = partes
            else:
                dia, mes, anio = partes

            return f"{int(anio):04d}-{int(mes):02d}-{int(dia):02d}"

        return fecha

    tabla["fecha_de_beneficio"] = (
        tabla["fecha_de_beneficio"].apply(organizar_fecha)
    )

    # Manu: Limpiar símbolos y separadores del monto
    def organizar_monto(monto):
        texto_monto = (
            str(monto)
            .replace("$", "")
            .replace(",", "")
            .strip()
        )

        return int(float(texto_monto))

    tabla["monto_del_credito"] = (
        tabla["monto_del_credito"].apply(organizar_monto)
    )

    # Manu: Eliminar registros duplicados después de normalizar
    tabla = tabla.drop_duplicates()

    # Manu: Conservar únicamente las columnas y el orden solicitado
    tabla = tabla[columnas_finales]

    # Manu: Guardar el dataset limpio separado por punto y coma
    ruta_salida = ruta_entregables / "solicitudes_de_credito.csv"

    tabla.to_csv(
        ruta_salida,
        sep=";",
        index=False,
        encoding="utf-8"
    )

