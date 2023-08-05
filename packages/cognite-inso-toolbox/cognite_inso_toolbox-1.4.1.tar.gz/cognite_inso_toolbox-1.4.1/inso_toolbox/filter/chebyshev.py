import warnings
from typing import Dict, Union

import pandas as pd
from scipy import signal

from inso_toolbox.utils import pipeline_function


@pipeline_function
def chebyshev(
    data: Union[pd.DataFrame, pd.Series], filter_type: int = 1, cheby_kwargs: Dict = {}
) -> Union[pd.DataFrame, pd.Series]:
    """ Chebyshev filter of type 1 and 2.
    Uses second-order section (sos) output filter type.

    Args:
        data (pd.DataFrame or pd.Series): Time series to filter.
        filter_type (int): Chebyshev filter type (either 1 or 2).
        cheby_kwargs (Dict): Keyword arguments for scipy.signal.cheby filter (must include "output":"sos").

    Returns:
        pd.DataFrame or pd.Series: Filtered signal.
    """  # noqa
    # Only pd.Series and pd.DataFrame inputs are supported
    assert isinstance(data, pd.Series) or isinstance(data, pd.DataFrame)

    # Only type 1 and 2 chebyshev filters exist
    if filter_type not in {1, 2}:
        raise ValueError("Filter type must be either 1 or 2.")

    # Scipy also supports output types "ab" and "zpk". Here only "sos" is supported.
    if cheby_kwargs.get("output") != "sos":
        raise ValueError("Only sos output filter type is supported.")

    # Warn user if there are any missing values
    if data.isna().any(axis=None):
        warnings.warn("There are missing values present in the time series.", RuntimeWarning)

    # Get type 1 and 2 chebyshev filter
    cheby_filters = {1: signal.cheby1, 2: signal.cheby2}

    # Get filter output
    filter_output = cheby_filters[filter_type](**cheby_kwargs)

    # Filter the data
    filtered = signal.sosfilt(filter_output, data, axis=0)

    # Return series if that was the input type
    if isinstance(data, pd.Series):
        return pd.Series(filtered, index=data.index)

    # Return dataframe with same timestamps
    return pd.DataFrame(data=filtered, index=data.index, columns=data.columns)
