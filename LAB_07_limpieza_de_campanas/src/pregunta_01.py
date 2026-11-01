
# ============================================================
# LAB 07 - LIMPIEZA DE CAMPAÑAS
# Manu | Pregunta 01: Construcción de tablas analíticas
# ============================================================

from pathlib import Path

import pandas as pd


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Procesa diez archivos comprimidos de campañas bancarias
    y construye tres tablas analíticas independientes.

    Genera los datasets de clientes, campañas y economía,
    guarda los CSV en submission y retorna los tres DataFrames.
    """

    # Manu: Definir las rutas del laboratorio
    ruta_laboratorio = Path(__file__).resolve().parents[1]
    ruta_datos = ruta_laboratorio / "data"
    ruta_entregables = ruta_laboratorio / "submission"

    # Manu: Crear la carpeta para los archivos de entrega
    ruta_entregables.mkdir(parents=True, exist_ok=True)

    # Manu: Identificar los archivos comprimidos en orden
    archivos_comprimidos = sorted(
        ruta_datos.glob("bank-marketing-campaing-*.csv.gz")
    )

    # Manu: Leer y unificar los datos sin descomprimir manualmente
    tablas_originales = [
        pd.read_csv(archivo, compression="gzip")
        for archivo in archivos_comprimidos
    ]

    datos = pd.concat(tablas_originales, ignore_index=True)

    # Manu: Ordenar los registros por identificador del cliente
    datos = datos.sort_values("client_id").reset_index(drop=True)

    # ========================================================
    # 1. TABLA DE CLIENTES
    # ========================================================

    # Manu: Limpiar los nombres de las ocupaciones
    ocupaciones = (
        datos["job"]
        .str.replace(".", "", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # Manu: Estandarizar la educación y conservar faltantes
    niveles_educativos = (
        datos["education"]
        .str.replace(".", "_", regex=False)
        .replace("unknown", pd.NA)
    )

    # Manu: Construir la información de clientes
    clientes = pd.DataFrame({
        "client_id": datos["client_id"].astype(int),
        "age": datos["age"].astype(int),
        "job": ocupaciones,
        "marital": datos["marital"],
        "education": niveles_educativos,
        "credit_default": (
            datos["credit_default"].eq("yes").astype(int)
        ),
        "mortgage": (
            datos["mortgage"].eq("yes").astype(int)
        ),
    })

    # ========================================================
    # 2. TABLA DE CAMPAÑAS
    # ========================================================

    # Manu: Relacionar los meses con su representación numérica
    equivalencia_meses = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    # Manu: Convertir el mes y ajustar el día a dos dígitos
    mes_contacto = (
        datos["month"].str.lower().map(equivalencia_meses)
    )

    dia_contacto = datos["day"].astype(str).str.zfill(2)

    # Manu: Construir la fecha del último contacto en 2022
    fechas_contacto = (
        "2022-" + mes_contacto + "-" + dia_contacto
    )

    # Manu: Construir la información de campañas
    campanas = pd.DataFrame({
        "client_id": datos["client_id"].astype(int),
        "number_contacts": datos["number_contacts"].astype(int),
        "contact_duration": datos["contact_duration"].astype(int),
        "previous_campaign_contacts": (
            datos["previous_campaign_contacts"].astype(int)
        ),
        "previous_outcome": (
            datos["previous_outcome"].eq("success").astype(int)
        ),
        "campaign_outcome": (
            datos["campaign_outcome"].eq("yes").astype(int)
        ),
        "last_contact_date": fechas_contacto,
    })

    # ========================================================
    # 3. TABLA DE CONTEXTO ECONÓMICO
    # ========================================================

    # Manu: Seleccionar y convertir las variables económicas
    economia = pd.DataFrame({
        "client_id": datos["client_id"].astype(int),
        "cons_price_idx": datos["cons_price_idx"].astype(float),
        "euribor_three_months": (
            datos["euribor_three_months"].astype(float)
        ),
    })

    # ========================================================
    # 4. GENERACIÓN DE LOS ARCHIVOS CSV
    # ========================================================

    # Manu: Organizar las tres tablas para su exportación
    entregables = {
        "client.csv": clientes,
        "campaign.csv": campanas,
        "economics.csv": economia,
    }

    # Manu: Guardar los CSV sin el índice de Pandas
    for nombre_archivo, tabla in entregables.items():
        ruta_salida = ruta_entregables / nombre_archivo

        tabla.to_csv(
            ruta_salida,
            index=False,
            encoding="utf-8"
        )

    # Manu: Retornar los DataFrames en el orden solicitado
    return clientes, campanas, economia


# Manu: Mantener compatibilidad con el nombre pregunta_01
pregunta_01 = clean_campaign_data
