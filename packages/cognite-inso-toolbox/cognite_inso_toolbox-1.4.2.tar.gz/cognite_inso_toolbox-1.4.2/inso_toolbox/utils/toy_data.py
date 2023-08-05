import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# random.seed(0)


def create_uniform_data(values: tuple, start_date: datetime = datetime(2020, 7, 23, 15, 27, 0), frequency: str = "1s"):
    values = np.hstack(values)
    return pd.DataFrame({"value": values}, index=pd.date_range(start=start_date, freq=frequency, periods=len(values)))


def create_non_uniform_data(
    values: tuple, start_date: datetime = datetime(2020, 7, 23, 15, 27, 0), time_delta: timedelta = timedelta(seconds=1)
):
    values = np.hstack(values)
    indices = [start_date]
    for i in range(1, len(values)):
        indices.append(indices[i - 1] + time_delta * random.randint(1, 1000))
    return pd.DataFrame({"value": values}, index=indices)


def delete_random_data(data: pd.DataFrame, percentage: float = 0.5) -> pd.DataFrame:
    num_points_to_change = min(int(len(data) * percentage), len(data) - 2)
    indices = np.random.choice(data.index[1:-1], size=num_points_to_change, replace=False)
    return data.drop(indices)


def set_na_random_data(data: pd.DataFrame, percentage: float = 0.5) -> pd.DataFrame:
    new_data = data.copy()
    num_points_to_change = min(int(len(new_data) * percentage), len(new_data) - 2)
    indices = np.random.choice(new_data.index[1:-1], size=num_points_to_change, replace=False)
    new_data.loc[indices] = np.nan
    return new_data


def create_uniform_multidata(
    values: list, start_date: datetime = datetime(2020, 7, 23, 15, 27, 0), frequency: str = "1s"
):
    data = create_uniform_data(values[0], start_date, frequency)
    for i in range(1, len(values)):
        more_data = create_uniform_data(values[i], start_date, frequency)
        m_data = data.merge(more_data, on=data.index)
        m_data.index = data.index
        m_data.drop(columns="key_0", inplace=True)
        data = m_data
    return data
