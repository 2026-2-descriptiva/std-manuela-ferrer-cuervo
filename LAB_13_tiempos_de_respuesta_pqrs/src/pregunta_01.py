
# ============================================================
# LAB 13 - TIEMPOS DE RESPUESTA DE PQRS
# Manu | Pregunta 01: Cumplimiento de los plazos de respuesta
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Analiza el cumplimiento del plazo de respuesta de PQRS
    para los canales web y cartas.

    Calcula los tiempos de respuesta en días calendario y
    días hábiles, identifica solicitudes pendientes y genera
    tres reportes en formato CSV.
    """

    # ========================================================
    # 1. CARGA Y PREPARACIÓN DE LOS DATOS
    # ========================================================

    # Manu: Definir las rutas dentro del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parent.parent
    ruta_datos = ruta_laboratorio / "data"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta de entregables si no existe
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Leer las solicitudes recibidas por la página web
    solicitudes_web = pd.read_csv(
        ruta_datos / "historical_requests_web.csv.gz",
        compression="gzip"
    )

    # Manu: Leer las solicitudes recibidas por carta
    solicitudes_cartas = pd.read_csv(
        ruta_datos / "historical_requests_letter.csv.gz",
        compression="gzip"
    )

    # Manu: Eliminar únicamente las filas completamente duplicadas
    # Se conservan las solicitudes sin identificador.
    solicitudes_web = solicitudes_web.drop_duplicates().copy()
    solicitudes_cartas = solicitudes_cartas.drop_duplicates().copy()

    # Manu: Identificar el canal de origen de cada solicitud
    solicitudes_web["channel"] = "web"
    solicitudes_cartas["channel"] = "letter"

    # Manu: Unir ambos canales en una sola tabla
    solicitudes = pd.concat(
        [solicitudes_cartas, solicitudes_web],
        ignore_index=True
    )

    # ========================================================
    # 2. PREPARACIÓN DE FECHAS E INDICADORES
    # ========================================================

    # Manu: Convertir las fechas de entrada y respuesta
    fecha_entrada = pd.to_datetime(solicitudes["in_date"])
    fecha_respuesta = pd.to_datetime(solicitudes["out_date"])

    # Manu: Calcular los días calendario transcurridos
    solicitudes["calendar_days"] = (
        fecha_respuesta - fecha_entrada
    ).dt.days

    # Manu: Identificar el año de entrada de la solicitud
    solicitudes["year"] = fecha_entrada.dt.year

    # Manu: Identificar las solicitudes que ya tienen respuesta
    respondidas = fecha_respuesta.notna()

    # Manu: Preparar los límites para contar días hábiles
    # Se excluye el día de entrada y se incluye el de respuesta.
    inicio_habil = (
        fecha_entrada.loc[respondidas]
        .to_numpy(dtype="datetime64[D]")
        + np.timedelta64(1, "D")
    )

    final_habil = (
        fecha_respuesta.loc[respondidas]
        .to_numpy(dtype="datetime64[D]")
        + np.timedelta64(1, "D")
    )

    # Manu: Contar únicamente lunes a viernes, sin festivos
    solicitudes.loc[respondidas, "business_days"] = (
        np.busday_count(inicio_habil, final_habil)
    )

    # Manu: Una solicitud cumple si fue respondida en máximo
    # 15 días hábiles. Las pendientes no cuentan como cumplidas.
    solicitudes["on_time"] = (
        solicitudes["business_days"] <= 15
    ).fillna(False)

    # ========================================================
    # 3. RESUMEN DE CUMPLIMIENTO POR CANAL
    # ========================================================

    registros_canales = []

    # Manu: Mantener los canales en orden alfabético
    for canal in ["letter", "web"]:

        grupo = solicitudes.loc[
            solicitudes["channel"] == canal
        ]

        # Manu: Contar solicitudes recibidas y respondidas
        total_solicitudes = int(len(grupo))
        total_respondidas = int(grupo["out_date"].notna().sum())

        # Manu: Contar las solicitudes todavía pendientes
        total_pendientes = int(grupo["out_date"].isna().sum())

        # Manu: Calcular la mediana solo con solicitudes respondidas
        mediana_habiles = float(
            grupo.loc[
                grupo["out_date"].notna(),
                "business_days"
            ].median()
        )

        # Manu: El denominador incluye también las pendientes
        tasa_cumplimiento = float(grupo["on_time"].mean())

        registros_canales.append({
            "channel": canal,
            "requests": total_solicitudes,
            "answered": total_respondidas,
            "pending": total_pendientes,
            "median_business_days": mediana_habiles,
            "on_time_rate": tasa_cumplimiento,
        })

    # Manu: Construir el resumen de los dos canales
    resumen_canales = pd.DataFrame(registros_canales)

    # ========================================================
    # 4. RESUMEN DE CUMPLIMIENTO POR AÑO Y CANAL
    # ========================================================

    registros_anuales = []

    # Manu: Agrupar según el año de entrada y el canal
    for (anio, canal), grupo in solicitudes.groupby(
        ["year", "channel"]
    ):

        registros_anuales.append({
            "year": int(anio),
            "channel": canal,
            "requests": int(len(grupo)),
            "pending": int(grupo["out_date"].isna().sum()),
            "on_time_rate": float(grupo["on_time"].mean()),
        })

    # Manu: Ordenar por año y luego por canal
    resumen_anual = (
        pd.DataFrame(registros_anuales)
        .sort_values(["year", "channel"])
        .reset_index(drop=True)
    )

    # ========================================================
    # 5. RESUMEN SEGÚN EL DÍA DE ENTRADA
    # ========================================================

    # Manu: Definir el orden de lunes a domingo
    orden_dias = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    registros_dias = []

    # Manu: Analizar ambos canales de forma conjunta
    for dia in orden_dias:

        grupo = solicitudes.loc[
            solicitudes["day_name"] == dia
        ]

        # Manu: Seleccionar únicamente las solicitudes respondidas
        grupo_respondido = grupo.loc[
            grupo["out_date"].notna()
        ]

        # Manu: Comparar días calendario frente a días hábiles
        mediana_calendario = float(
            grupo_respondido["calendar_days"].median()
        )

        mediana_habiles = float(
            grupo_respondido["business_days"].median()
        )

        registros_dias.append({
            "day_name": dia,
            "requests": int(len(grupo)),
            "median_calendar_days": mediana_calendario,
            "median_business_days": mediana_habiles,
        })

    # Manu: Construir el resumen por día de entrada
    resumen_dias = pd.DataFrame(registros_dias)

    # ========================================================
    # 6. GENERACIÓN DE LOS ENTREGABLES
    # ========================================================

    # Manu: Asociar cada resultado con su archivo CSV
    archivos_salida = {
        "channel_summary.csv": resumen_canales,
        "yearly_summary.csv": resumen_anual,
        "entry_day_summary.csv": resumen_dias,
    }

    # Manu: Guardar los archivos sin el índice de Pandas
    for nombre_archivo, tabla in archivos_salida.items():
        tabla.to_csv(
            ruta_entregables / nombre_archivo,
            index=False,
            encoding="utf-8"
        )

    # ========================================================
    # 7. RETORNO DE LOS RESULTADOS
    # ========================================================

    # Manu: Retornar las tres tablas en el orden solicitado
    return resumen_canales, resumen_anual, resumen_dias

