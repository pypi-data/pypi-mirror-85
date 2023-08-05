from typing import Callable, List, Union

import numpy as np
import pandas as pd
import scipy.integrate


def check_uniform(data: pd.DataFrame, unit: str = "ns") -> bool:
    """
    Convenience method to verify input time series is uniform.
    Args:
        data (pandas.DataFrame): Time series to check. Object must have a datetime-like index.
        unit (str): Time unit of uniformity check. Follows Numpy DateTime Units convention.
    Returns:
        bool
    """
    # Get time difference between successive observations
    timediff = np.diff(data.index)
    # Round to desired time unit (e.g. uniform on second scale)
    rounded = timediff.astype(dtype=f"timedelta64[{unit}]")
    # Check whether uniform
    return len(np.unique(rounded)) == 1


def make_uniform(data: pd.DataFrame, resolution: str = "1s", interpolation: str = None) -> pd.DataFrame:
    """
    Convenience method to make an input time series dataframe uniform per specified temporal resolution.
    Object must have a datetime-like index.
    Args:
        resolution (str):  Temporal resolution of uniform time series. Follows Pandas DateTime convention.
        interpolation (optional str): Method for optional interpolation. Follows pandas Resampler.interpolate
    Returns:
        pandas.DataFrame
    """
    new_data = data.copy()
    # If no interpolation specified, do not perform interpolation
    if not interpolation:
        new_data = new_data.resample(resolution).mean()
    # Otherwise perform desired interpolation
    else:
        new_data = new_data.resample(rule=resolution).mean().interpolate(method=interpolation)
    return new_data


def functional_mean(function: Callable, x_vals: List) -> List:
    """
    Convenience method to calculate the mean of a function inbetween each x value.
    The last point is the function called at the last x value. This is required for the
    input and output lists to have the same lengths.
    """
    assert len(x_vals) > 0
    y_vals = np.zeros(len(x_vals))
    for i in range(len(x_vals) - 1):
        y_vals[i] = scipy.integrate.quad(function, x_vals[i], x_vals[i + 1])[0] / (x_vals[i + 1] - x_vals[i])
    y_vals[len(x_vals) - 1] = function(x_vals[-1])
    return y_vals


def is_na_all(data: Union[pd.DataFrame, pd.Series]) -> bool:
    """
    Convenience method to test if all values in dataframe/series are NaN.
    """
    if isinstance(data, pd.Series):
        return data.isnull().all()
    elif isinstance(data, pd.DataFrame):
        return pd.isna(data).all(axis=None)
    else:
        raise ValueError("Convenience method only supports Series or DataFrame.")


def is_na_initial(data):
    """
    Convenience method to test if any initial values in dataframe/series are NaN.
    """
    if isinstance(data, pd.Series):
        return pd.isna(data.iloc[0])
    elif isinstance(data, pd.DataFrame):
        return pd.isna(data.iloc[0]).any(axis=None)
    else:
        raise ValueError("Convenience method only supports Series or DataFrame.")


def is_na_final(data):
    """
    Convenience method to test if any final values in dataframe/series are NaN.
    """
    if isinstance(data, pd.Series):
        return pd.isna(data.iloc[-1])
    elif isinstance(data, pd.DataFrame):
        return pd.isna(data.iloc[-1]).any(axis=None)
    else:
        raise ValueError("Convenience method only supports Series or DataFrame.")
