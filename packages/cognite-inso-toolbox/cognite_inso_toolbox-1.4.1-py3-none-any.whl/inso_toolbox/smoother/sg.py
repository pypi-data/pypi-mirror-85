from typing import Dict, Union

import pandas as pd
from scipy.signal import savgol_filter

from inso_toolbox.utils import pipeline_function


@pipeline_function
def savitzky_golay(
    data: Union[pd.DataFrame, pd.Series], window_length: int = 9, polyorder: int = 2, optional_kwargs: Dict = {}
) -> Union[pd.DataFrame, pd.Series]:
    """ Savitzky-Golay smoother. Wrapper for scipy.signal.savgol_filter function.
    
    Does not assume uniform time series.

    Args:
        data (pd.DataFrame or pd.Series): Time series to smooth.
        window_length (int): Length of filter window.
        polyorder (int): Order of polynomial used to fit the samples.
        optional_kwargs (Dict): Optional keyword arguments for scipy.signal.savgol_filter.

    Returns:
        pd.DataFrame or pd.Series: Smoothed time series with the same timestamps.
    """  # noqa
    # Cannot contain any NaN values
    if data.isna().any(axis=None):
        raise ValueError("Input time series contains NaN value(s). All missing values must first be imputed.")

    # Apply filter on Series data
    if isinstance(data, pd.Series):
        filtered = savgol_filter(data.values.squeeze(), window_length, polyorder, **optional_kwargs)
        return pd.Series(data=filtered, index=data.index)

    # Otherwise apply filter on each column
    filtered_data = pd.DataFrame()
    for column_name, column_data in data.iteritems():
        filtered_data[column_name] = savgol_filter(
            column_data.values.squeeze(), window_length, polyorder, **optional_kwargs
        )

    filtered_data.index = data.index.values
    return filtered_data
