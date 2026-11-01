
# ============================================================
# LAB 05 - VALIDACIÓN DE DATOS
# Manu | Pregunta 01: Diagnóstico de calidad de datos
# ============================================================

import json
import re
from pathlib import Path

import pandas as pd


def main():
    """
    Evalúa la calidad de los datos del archivo ventas.csv.gz.

    Identifica problemas de estructura, valores faltantes,
    registros duplicados, correos inválidos, unidades
    incorrectas y diferencias en las categorías de países.

    Genera un reporte JSON sin modificar los datos originales.
    """

    # Manu: Definir las rutas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parents[1]
    ruta_datos = ruta_laboratorio / "data" / "ventas.csv.gz"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta de entrega si no existe
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Definir las columnas obligatorias
    columnas_requeridas = [
        "supplier_id",
        "supplier",
        "country",
        "city",
        "purchase_date",
        "amount",
        "discount",
        "weight",
        "units",
        "unit_price",
        "contact_email",
    ]

    # Manu: Leer los datos conservando sus valores originales
    tabla = pd.read_csv(
        ruta_datos,
        keep_default_na=False
    )

    # Manu: Normalizar únicamente los encabezados
    tabla.columns = [
        re.sub(r"\s+", "_", columna.replace("\ufeff", "").strip().lower())
        for columna in tabla.columns
    ]

    # Manu: Revisar la estructura general
    cantidad_filas = int(tabla.shape[0])
    cantidad_columnas = int(tabla.shape[1])

    # Manu: Identificar columnas faltantes y adicionales
    columnas_faltantes = sorted(
        columna
        for columna in columnas_requeridas
        if columna not in tabla.columns
    )

    columnas_adicionales = sorted(
        columna
        for columna in tabla.columns
        if columna not in columnas_requeridas
    )

    # Manu: Contar las filas duplicadas
    filas_duplicadas = int(tabla.duplicated().sum())

    # Manu: Detectar todos los registros con proveedor repetido
    proveedores_repetidos = 0

    if "supplier_id" in tabla.columns:
        proveedores_repetidos = int(
            tabla["supplier_id"].duplicated(keep=False).sum()
        )

    # Manu: Contar los valores faltantes por columna
    faltantes_por_columna = {}

    for columna in tabla.columns:
        valores = tabla[columna].astype(str).str.strip()
        es_faltante = valores.isin(["", "N/A"])

        faltantes_por_columna[columna] = int(es_faltante.sum())

    # Manu: Validar el formato de los correos electrónicos
    patron_correo = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    correos_invalidos = 0

    if "contact_email" in tabla.columns:
        for correo in tabla["contact_email"]:
            correo_texto = str(correo).strip()

            if not patron_correo.fullmatch(correo_texto):
                correos_invalidos += 1

    # Manu: Identificar unidades que no son enteros positivos
    unidades_invalidas = 0

    if "units" in tabla.columns:
        for unidad in tabla["units"]:
            unidad_texto = str(unidad).strip()

            # Manu: Excluir los valores faltantes del conteo
            if unidad_texto in ["", "N/A"]:
                continue

            try:
                numero = float(unidad_texto)

                if not (numero.is_integer() and numero > 0):
                    unidades_invalidas += 1

            except ValueError:
                unidades_invalidas += 1

    # Manu: Conservar los países exactamente como aparecen
    paises_registrados = []

    if "country" in tabla.columns:
        paises_registrados = sorted(
            tabla["country"].unique().tolist()
        )

    # Manu: Consolidar los resultados del diagnóstico
    reporte_calidad = {
        "row_count": cantidad_filas,
        "column_count": cantidad_columnas,
        "missing_required_columns": columnas_faltantes,
        "unexpected_columns": columnas_adicionales,
        "duplicate_row_count": filas_duplicadas,
        "duplicate_supplier_id_row_count": proveedores_repetidos,
        "missing_value_count_by_column": faltantes_por_columna,
        "invalid_email_count": correos_invalidos,
        "invalid_unit_count": unidades_invalidas,
        "country_values": paises_registrados,
    }

    # Manu: Guardar el reporte en la carpeta submission
    ruta_reporte = ruta_entregables / "data_quality_report.json"

    with open(ruta_reporte, "w", encoding="utf-8") as archivo:
        json.dump(
            reporte_calidad,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    # Manu: Retornar el diagnóstico como diccionario
    return reporte_calidad


# Manu: Mantener compatibilidad con el nombre de la actividad
pregunta_01 = main
