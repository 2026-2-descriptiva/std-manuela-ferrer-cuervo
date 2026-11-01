
# ============================================================
# LAB 08 - K-ANONIMATO DE ASEGURADOS
# Manu | Pregunta 01: Evaluación de privacidad de datos
# ============================================================

import json
from pathlib import Path

import numpy as np
import pandas as pd


def pregunta_01():
    """
    Evalúa el riesgo de reidentificación de los asegurados
    mediante k-anonimato y diversidad del atributo sensible.

    Compara dos esquemas de generalización, selecciona el
    que suprime menos registros y genera los entregables.
    """

    # Manu: Definir las rutas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parents[1]
    ruta_datos = ruta_laboratorio / "data" / "insurance.csv.gz"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta de entrega
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Leer directamente el archivo comprimido
    tabla = pd.read_csv(ruta_datos, compression="gzip")

    # ========================================================
    # 1. EVALUACIÓN DE LOS DATOS ORIGINALES
    # ========================================================

    # Manu: Identificar los cuasi-identificadores originales
    identificadores_originales = [
        "age",
        "sex",
        "bmi",
        "children",
        "region",
    ]

    # Manu: Calcular el tamaño de cada clase de equivalencia
    tamanos_originales = tabla.groupby(
        identificadores_originales
    )["age"].transform("size")

    # Manu: Calcular el anonimato y los registros únicos
    anonimato_original = int(tamanos_originales.min())

    registros_unicos = int(
        (tamanos_originales == 1).sum()
    )

    # ========================================================
    # 2. GENERALIZACIÓN DE LOS DATOS
    # ========================================================

    # Manu: Agrupar las edades en intervalos
    limites_edad = [18, 30, 40, 50, 65]
    grupos_edad = ["18-29", "30-39", "40-49", "50-64"]

    tabla["age_group"] = pd.cut(
        tabla["age"],
        bins=limites_edad,
        labels=grupos_edad,
        right=False
    ).astype(str)

    # Manu: Clasificar el índice de masa corporal
    limites_imc = [-np.inf, 18.5, 25, 30, np.inf]

    grupos_imc = [
        "bajo peso",
        "normal",
        "sobrepeso",
        "obesidad",
    ]

    tabla["bmi_group"] = pd.cut(
        tabla["bmi"],
        bins=limites_imc,
        labels=grupos_imc,
        right=False
    ).astype(str)

    # Manu: Agrupar la cantidad de hijos
    def clasificar_hijos(cantidad):
        if cantidad == 0:
            return "0"
        elif cantidad in [1, 2]:
            return "1-2"
        else:
            return "3+"

    tabla["children_group"] = (
        tabla["children"].apply(clasificar_hijos)
    )

    # ========================================================
    # 3. DEFINICIÓN DE LOS ESQUEMAS
    # ========================================================

    # Manu: Comparar la publicación con y sin número de hijos
    esquemas = {
        "with_children": [
            "age_group",
            "sex",
            "bmi_group",
            "children_group",
            "region",
        ],
        "without_children": [
            "age_group",
            "sex",
            "bmi_group",
            "region",
        ],
    }

    # Manu: Almacenar los resultados de cada alternativa
    resultados_esquemas = {}
    tablas_publicables = {}

    # Manu: Definir el mínimo de registros por clase
    k_minimo = 5

    # ========================================================
    # 4. EVALUACIÓN DE CADA ESQUEMA
    # ========================================================

    for nombre_esquema, identificadores in esquemas.items():

        # Manu: Calcular las clases de equivalencia
        grupos = tabla.groupby(
            identificadores,
            observed=True
        )

        tamanos_clases = grupos["age"].transform("size")

        total_clases = int(grupos.ngroups)
        k_antes = int(tamanos_clases.min())

        # Manu: Identificar los registros que pueden publicarse
        mascara_publicacion = tamanos_clases >= k_minimo

        registros_suprimidos = int(
            (~mascara_publicacion).sum()
        )

        registros_publicados = int(
            mascara_publicacion.sum()
        )

        # Manu: Conservar solamente las clases con mínimo 5 registros
        tabla_publicada = tabla.loc[mascara_publicacion].copy()

        tablas_publicables[nombre_esquema] = tabla_publicada

        # Manu: Agrupar los registros que sí pueden publicarse
        grupos_publicados = tabla_publicada.groupby(
            identificadores,
            observed=True
        )

        clases_publicadas = int(grupos_publicados.ngroups)

        # Manu: Identificar clases sin diversidad de fumadores
        diversidad_fumadores = (
            grupos_publicados["smoker"].nunique()
        )

        clases_sin_diversidad = int(
            (diversidad_fumadores == 1).sum()
        )

        # Manu: Contar los registros pertenecientes a esas clases
        tamanos_publicados = grupos_publicados.size()

        registros_sin_diversidad = int(
            tamanos_publicados[
                diversidad_fumadores == 1
            ].sum()
        )

        # Manu: Consolidar las estadísticas del esquema
        resultados_esquemas[nombre_esquema] = {
            "quasi_identifiers": identificadores,
            "equivalence_classes": total_clases,
            "k_before_suppression": k_antes,
            "suppressed_records": registros_suprimidos,
            "published_records": registros_publicados,
            "published_classes": clases_publicadas,
            "classes_without_smoker_diversity": clases_sin_diversidad,
            "records_without_smoker_diversity": registros_sin_diversidad,
        }

    # ========================================================
    # 5. SELECCIÓN DEL ESQUEMA DE PUBLICACIÓN
    # ========================================================

    # Manu: Elegir el esquema que suprime menos registros
    esquema_seleccionado = min(
        resultados_esquemas,
        key=lambda nombre: resultados_esquemas[nombre][
            "suppressed_records"
        ]
    )

    # Manu: Recuperar los registros que se pueden publicar
    datos_publicados = tablas_publicables[esquema_seleccionado]

    # ========================================================
    # 6. COMPARACIÓN DE INDICADORES
    # ========================================================

    # Manu: Calcular el costo promedio de los seguros
    promedio_original = float(tabla["charges"].mean())

    promedio_publicado = float(
        datos_publicados["charges"].mean()
    )

    # Manu: Calcular la proporción de fumadores
    proporcion_original = float(
        tabla["smoker"].eq("yes").mean()
    )

    proporcion_publicada = float(
        datos_publicados["smoker"].eq("yes").mean()
    )

    # ========================================================
    # 7. CONSTRUCCIÓN DEL REPORTE DE PRIVACIDAD
    # ========================================================

    # Manu: Organizar los indicadores del análisis
    reporte_privacidad = {
        "original_k": anonimato_original,
        "original_unique_records": registros_unicos,
        "schemes": resultados_esquemas,
        "selected_scheme": esquema_seleccionado,
        "mean_charges_original": promedio_original,
        "mean_charges_published": promedio_publicado,
        "smoker_rate_original": proporcion_original,
        "smoker_rate_published": proporcion_publicada,
    }

    # Manu: Guardar el reporte en formato JSON
    ruta_reporte = ruta_entregables / "privacy_report.json"

    with open(ruta_reporte, "w", encoding="utf-8") as archivo:
        json.dump(
            reporte_privacidad,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    # ========================================================
    # 8. GENERACIÓN DEL DATASET PUBLICABLE
    # ========================================================

    # Manu: Seleccionar únicamente las columnas autorizadas
    columnas_publicacion = (
        esquemas[esquema_seleccionado]
        + ["smoker", "charges"]
    )

    # Manu: Conservar el orden original de los registros
    dataset_publicable = datos_publicados[columnas_publicacion]

    # Manu: Exportar los registros sin el índice de Pandas
    ruta_csv = ruta_entregables / "insurance_published.csv"

    dataset_publicable.to_csv(
        ruta_csv,
        index=False,
        encoding="utf-8"
    )

    # Manu: Retornar el reporte como diccionario
    return reporte_privacidad
