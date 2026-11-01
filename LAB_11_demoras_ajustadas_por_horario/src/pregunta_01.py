
# ============================================================
# LAB 11 - DEMORAS AJUSTADAS POR HORARIO
# Manu | Pregunta 01: Comparación de puntualidad de aerolíneas
# ============================================================

from pathlib import Path

import pandas as pd


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analiza las demoras de las aerolíneas considerando
    el efecto de los horarios programados de salida.

    Calcula las tasas nacionales por hora, las demoras
    esperadas por aerolínea y dos rankings de puntualidad.

    Guarda los resultados en submission y retorna
    los dos DataFrames.
    """

    # Manu: Definir las rutas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parents[1]

    ruta_datos = (
        ruta_laboratorio
        / "data"
        / "flights_by_carrier_day_hour.csv.gz"
    )

    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta para los resultados
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Leer directamente el archivo comprimido
    tabla = pd.read_csv(ruta_datos, compression="gzip")

    # ========================================================
    # 1. TASAS NACIONALES DE DEMORA POR HORA
    # ========================================================

    # Manu: Agrupar los vuelos según la hora de salida
    resumen_horario = (
        tabla.groupby("scheduled_departure_hour")[
            ["operated_flights", "delayed_departure_15_flights"]
        ]
        .sum()
        .reset_index()
    )

    # Manu: Calcular la tasa nacional de demora por hora
    resumen_horario["delay_rate"] = (
        resumen_horario["delayed_departure_15_flights"]
        / resumen_horario["operated_flights"]
    )

    # Manu: Organizar las horas de menor a mayor
    resumen_horario = (
        resumen_horario
        .sort_values("scheduled_departure_hour")
        .reset_index(drop=True)
    )

    # ========================================================
    # 2. CÁLCULO DE DEMORAS ESPERADAS
    # ========================================================

    # Manu: Relacionar cada hora con su tasa nacional
    tasas_por_hora = (
        resumen_horario
        .set_index("scheduled_departure_hour")["delay_rate"]
        .to_dict()
    )

    # Manu: Asignar la tasa nacional a cada registro
    tabla["tasa_horaria_nacional"] = (
        tabla["scheduled_departure_hour"].map(tasas_por_hora)
    )

    # Manu: Calcular las demoras esperadas según el horario
    tabla["demoras_esperadas"] = (
        tabla["operated_flights"]
        * tabla["tasa_horaria_nacional"]
    )

    # ========================================================
    # 3. RESUMEN DE DEMORAS POR AEROLÍNEA
    # ========================================================

    # Manu: Agrupar los vuelos por aerolínea
    resumen_aerolineas = (
        tabla.groupby("reporting_airline")
        .agg({
            "operated_flights": "sum",
            "delayed_departure_15_flights": "sum",
            "demoras_esperadas": "sum",
        })
        .reset_index()
    )

    # Manu: Seleccionar aerolíneas con al menos 100000 vuelos
    resumen_aerolineas = resumen_aerolineas.loc[
        resumen_aerolineas["operated_flights"] >= 100000
    ].copy()

    # Manu: Asignar el nombre solicitado a las demoras esperadas
    resumen_aerolineas = resumen_aerolineas.rename(
        columns={
            "demoras_esperadas": "expected_delayed_flights"
        }
    )

    # ========================================================
    # 4. INDICADORES DE PUNTUALIDAD
    # ========================================================

    # Manu: Calcular la tasa de demora sin ajustar
    resumen_aerolineas["delay_rate"] = (
        resumen_aerolineas["delayed_departure_15_flights"]
        / resumen_aerolineas["operated_flights"]
    )

    # Manu: Comparar las demoras observadas con las esperadas
    resumen_aerolineas["observed_to_expected_ratio"] = (
        resumen_aerolineas["delayed_departure_15_flights"]
        / resumen_aerolineas["expected_delayed_flights"]
    )

    # ========================================================
    # 5. CONSTRUCCIÓN DE LOS RANKINGS
    # ========================================================

    # Manu: Ordenar de peor a mejor según la tasa sin ajustar
    resumen_aerolineas["crude_rank"] = (
        resumen_aerolineas["delay_rate"]
        .rank(ascending=False, method="min")
        .astype(int)
    )

    # Manu: Ordenar según la razón observada sobre esperada
    resumen_aerolineas["adjusted_rank"] = (
        resumen_aerolineas["observed_to_expected_ratio"]
        .rank(ascending=False, method="min")
        .astype(int)
    )

    # Manu: Ordenar la tabla según el ranking ajustado
    resumen_aerolineas = (
        resumen_aerolineas
        .sort_values("adjusted_rank")
        .reset_index(drop=True)
    )

    # ========================================================
    # 6. ORGANIZACIÓN DE LAS TABLAS FINALES
    # ========================================================

    # Manu: Definir las columnas del resumen por hora
    columnas_horarias = [
        "scheduled_departure_hour",
        "operated_flights",
        "delayed_departure_15_flights",
        "delay_rate",
    ]

    # Manu: Definir las columnas del ranking de aerolíneas
    columnas_aerolineas = [
        "reporting_airline",
        "operated_flights",
        "delayed_departure_15_flights",
        "delay_rate",
        "expected_delayed_flights",
        "observed_to_expected_ratio",
        "crude_rank",
        "adjusted_rank",
    ]

    # Manu: Conservar solamente las columnas solicitadas
    resumen_horario = resumen_horario[columnas_horarias]
    resumen_aerolineas = resumen_aerolineas[columnas_aerolineas]

    # ========================================================
    # 7. GENERACIÓN DE LOS ENTREGABLES
    # ========================================================

    # Manu: Guardar las tasas de demora por hora
    resumen_horario.to_csv(
        ruta_entregables / "hourly_delay_rates.csv",
        index=False,
        encoding="utf-8"
    )

    # Manu: Guardar el ranking ajustado de aerolíneas
    resumen_aerolineas.to_csv(
        ruta_entregables / "carrier_adjusted_delays.csv",
        index=False,
        encoding="utf-8"
    )

    # Manu: Retornar las tablas en el orden solicitado
    return resumen_horario, resumen_aerolineas
