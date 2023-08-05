import warnings
from typing import Dict, Union

import pandas as pd
import scipy.signal as signal


def butterworth(data: Union[pd.DataFrame, pd.Series], butter_kwargs: Dict = {}) -> Union[pd.DataFrame, pd.Series]:
    """ Butterworth filter.
    Uses second-order section (sos) representation, polynomial (ba) representation,
    or zeros, poles, and system gain (zpk) representation.

    Args:
        data (pd.DataFrame or pd.Series): Time series to filter.
        butter_kwargs (Dict): Keyword arguments for scipy.signal.butter filter.

    Returns:
        pd.DataFrame or pd.Series: Filtered signal.
    """  # noqa

    # Only pd.Series and pd.DataFrame inputs are supported
    if not isinstance(data, pd.Series) and not isinstance(data, pd.DataFrame):
        raise ValueError("Only pd.Series and pd.DataFrame inputs are supported.")

    # Warn user if there are any missing values
    if data.isna().any(axis=None):
        warnings.warn("There are missing values present in the time series.", RuntimeWarning)

    if butter_kwargs.get("output") == "sos":
        # create filter
        filter_output = signal.butter(**butter_kwargs)
        # apply filter
        filtered = signal.sosfilt(filter_output, data, axis=0)
    elif butter_kwargs.get("output") == "ba":
        # create filter
        b, a = signal.butter(**butter_kwargs)
        # apply filter
        filtered = signal.lfilter(b, a, data, axis=0)
    elif butter_kwargs.get("output") == "zpk":
        # create filter
        z, p, k = signal.butter(**butter_kwargs)
        # Return polynomial transfer function representation from zeros and poles
        b, a = signal.zpk2tf(z, p, k)
        # apply filter
        filtered = signal.lfilter(b, a, data, axis=0)

    # Return series if that was the input type
    if isinstance(data, pd.Series):
        return pd.Series(filtered, index=data.index)

    # Return dataframe with same timestamps
    return pd.DataFrame(data=filtered, index=data.index, columns=data.columns)
