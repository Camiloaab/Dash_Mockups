"""Module to predict production."""
import itertools
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import scipy.integrate as integrate

from gaussian_utils import std_gaussian

def binary_argmin(ordered_list: list, number: float) -> int:
    """Find the position of the number in the ordered_list closest to given number."""
    if len(ordered_list) <= 2:
        return int(np.argmin([abs(x - number) for x in ordered_list]))
    half_length = len(ordered_list) // 2
    if number < ordered_list[half_length]:
        argmin = binary_argmin(ordered_list[:half_length], number)
    else:
        argmin = half_length + binary_argmin(ordered_list[half_length:], number)
    return argmin


def compute_day_integral(area: float, sigma: float, day: int, niv: list, partition: list) -> float:
    """Compute the integral between the given day and the previous day.

    This is done using the normalized integral vector (niv).
    """
    scaled = (day / sigma) - 3
    position = binary_argmin(partition, scaled)
    total_days = (partition[-1]-partition[0]) * sigma
    pieces_per_day = round(len(partition) / total_days)
    previous_day_position = position - pieces_per_day
    if previous_day_position < 0:
        integral = area * niv[position]
    else:
        integral = area * (niv[position] - niv[previous_day_position])
    return integral


def get_stalks_per_day_single_row(row: pd.Series, day: int, niv: list, partition: list) -> int:
    """Compute amount of stalks per day for a single row of the dataframe."""
    sigma = row["bell_sd"]
    area = row["expected_yield"]
    integral = compute_day_integral(area, sigma, day, niv, partition)
    return round(integral)


def get_production_prediction(df: pd.DataFrame) -> pd.DataFrame:
    """Add dates and stalks per day.

    The input must have the following columns:
    * planted_on: datetime
    * bell_sd: float
    * expected_yield: float
    * blooming_wait: int
    """
    production = df.copy()
    for col in ['mu', 'bell_sd', 'expected_yield']:
        production[col] = production[col].astype(float)
    partition = list(np.linspace(-5, 5, 4096))
    # niv stands for normalized integral vector
    niv = [integrate.quad(lambda x: std_gaussian(x), -np.inf, i)[0] for i in partition]
    for day_num in range(23):
        production[f"fecha_dia_{day_num+1}"] = production.apply(
            lambda row: row["planted_on"] + timedelta(days=row["blooming_wait"] + day_num), axis=1
        )
        production[f"tallos_dia_{day_num+1}"] = production.apply(
            lambda row: get_stalks_per_day_single_row(row, day_num, niv, partition),
            axis=1,
        )
    return production


def get_available_stalks(stalks_df: pd.DataFrame, date: datetime, var_duration: int) -> int:
    """
    Return available stalks at given date.

    The stalks_df dataframe must have the columns:
    fecha_dia_i: datetime64
    tallos_dia_i: float
    for i ranging from 1 to 23 (both inclusive).
    """
    initial = date - timedelta(days=var_duration)
    final = date
    dates = list(pd.date_range(initial, final, freq="D"))
    total_stalks = 0
    for date in dates:
        for i in range(23):
            if stalks_df[stalks_df[f"fecha_dia_{i+1}"] == date][f"tallos_dia_{i+1}"].sum():
                total_stalks += stalks_df[stalks_df[f"fecha_dia_{i+1}"] == date][
                    f"tallos_dia_{i+1}"
                ].sum()
    return total_stalks


def stalks_to_date(df: pd.DataFrame, cant_deseada_de_tallos: int):
    """Return the date on which the number of stems will be available."""
    small_dfs = []
    #quantity_of_cols = int(len(df.columns) / 2) + 1
    for k in range(1, 23):
        col1 = "fecha_dia_" + str(k)
        col2 = "tallos_dia_" + str(k)
        df_aux = df[[col1, col2]]
        df_aux = df_aux.rename(columns={col1: "fecha", col2: "cantidad_de_tallos"})
        df_aux = df_aux.set_index("fecha", drop=True)
        df_aux.reset_index(inplace=True)
        small_dfs.append(df_aux)
    all_small_dfs = pd.concat(small_dfs, ignore_index=True)
    acum_tallos_por_fecha = all_small_dfs.groupby("fecha").sum()
    acum_tallos_por_fecha.reset_index(inplace=True)
    acum_tallos_por_fecha_sin_ceros = acum_tallos_por_fecha[
        acum_tallos_por_fecha.cantidad_de_tallos != 0
    ]
    lista_acum_tallos_por_fecha_sin_ceros = acum_tallos_por_fecha_sin_ceros[
        "cantidad_de_tallos"
    ].to_list()
    sumas_parciales_tallos = list(itertools.accumulate(lista_acum_tallos_por_fecha_sin_ceros))
    if cant_deseada_de_tallos > sumas_parciales_tallos[-1]:
        rv = datetime(9999, 12, 31)
    else:
        indice = [cant_deseada_de_tallos <= k for k in sumas_parciales_tallos].index(True)
        date = acum_tallos_por_fecha_sin_ceros.loc[indice, "fecha"]
        rv = date
    return rv