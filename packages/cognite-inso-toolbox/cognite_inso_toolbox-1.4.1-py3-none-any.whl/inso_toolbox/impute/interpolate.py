import warnings
from datetime import datetime
from typing import Union

import numpy as np
import pandas as pd
import scipy.interpolate

from inso_toolbox.utils import pipeline_function
from inso_toolbox.utils.helpers import functional_mean, is_na_all


@pipeline_function
def interpolate(
    data: Union[pd.DataFrame, pd.Series],
    method: str = "linear",
    kind: str = "pointwise",
    granularity: str = "1s",
    start: Union[int, datetime] = None,
    end: Union[int, datetime] = None,
    outside_fill: str = None,
) -> Union[pd.DataFrame, pd.Series]:
    """ 
    Interpolates data for uniform timestamps between start and end with specified frequency.
    
    Args:
        data (pd.DataFrame or pd.Series): Time series to impute.
        method (str): Specifies the interpolation method:

            * 'linear': linear interpolation.
            * 'ffill': forward filling.
            * 'zero', ‘slinear’, ‘quadratic’, ‘cubic’: spline interpolation of zeroth, first, second or third order.
        kind (str): Specifies the kind of returned datapoints:

            * 'pointwise': returns the pointwise value of the interpolated function for each timestamp.
            * 'average': returns the average of the interpolated function within each time period. This is the same as CDF average aggregates.
        granularity (str): Frequency of output e.g. '1s' or '2h'.
        start (int or datetime, optional): Start datetime or timestamp of output dataframe.
        end (int or datetime, optional): End datetime or timestamp of output dataframe.
        outside_fill (str, optional): Specifies how to fill values outside input data range ('NaN' or 'extrapolate').
            Default behaviour is to raise a ValueError if the data range is not within start and end and no outside_fill method is specified.
        
    Returns:
        pd.DataFrame or pd.Series: Uniform, interpolated time series with specified frequency.

    """  # noqa
    # Only pd.Series and pd.DataFrame inputs are supported
    if not isinstance(data, (pd.Series, pd.DataFrame)):
        raise TypeError("Only pd.Series and pd.DataFrame inputs are supported.")

    # Check for empty time series
    if len(data) == 0:
        warnings.warn("The time series is empty.", RuntimeWarning)
        return data

    # Check if all values are NaN
    if is_na_all(data):
        warnings.warn("All values in the time series are NaN.", RuntimeWarning)
        return data

    # Allow for other ways of defining forward filling for stepwise functions
    method = "previous" if method in ("ffill", "stepwise") else method

    # Get outside fill value
    if outside_fill == "NaN":
        outside_fill = np.NaN
    if outside_fill not in (np.nan, "extrapolate") and outside_fill is not None:
        raise TypeError("outside_fill must be either 'NaN' or 'extrapolate'.")

    # Get start and end dates and store as datetime
    if not start:
        start = data.index[0]
    elif isinstance(start, int):
        # If milliseconds provided, recast to float as datetime will throw exception otherwise
        if len(str(start)) == 13:
            start = datetime.fromtimestamp(start / 1000)
        elif len(str(start)) == 10:
            start = datetime.fromtimestamp(start)
        else:
            raise ValueError("Start timestamp is outside valid range.")
    if not end:
        end = data.index[-1]
    elif isinstance(end, int):
        # If milliseconds provided, recast to float as datetime will throw exception otherwise
        if len(str(end)) == 13:
            end = datetime.fromtimestamp(end / 1000)
        elif len(str(end)) == 10:
            end = datetime.fromtimestamp(end)
        else:
            raise ValueError("End timestamp is outside valid range.")
    else:
        start = start

    # Change minute granulatiry to match CDF granularity
    if granularity.lower().endswith("m"):
        granularity = granularity.lower().replace("m", "T")

    # Output timestamps for uniform time series
    timestamps = pd.date_range(start, end, freq=granularity)

    # Only DatetimeIndex is supported
    if not isinstance(data.index, pd.DatetimeIndex):
        raise TypeError("Input data must have DatetimeIndex.")

    # Create uniform x values for output time series
    x_uniform = np.array([timestamp.timestamp() for timestamp in timestamps])

    # Loop over timeseries (univariate Series or multivariate DataFrame)
    series = []
    for ts in pd.DataFrame(data).columns:
        # extract timeseries as pd.Series and drop NaNs
        observations = pd.DataFrame(data)[ts].dropna()

        # x and y datapoints used to construct linear piecewise function
        x_observed = np.array([index.timestamp() for index in observations.index])
        y_observed = observations.values.squeeze()

        # interpolator function
        if outside_fill is None:
            interper = scipy.interpolate.interp1d(x_observed, y_observed, kind=method)
        else:
            interper = scipy.interpolate.interp1d(
                x_observed, y_observed, kind=method, bounds_error=False, fill_value=outside_fill
            )

        # If pointwise, sample directly from interpolated (or original) points
        if kind == "pointwise":
            y_uniform = interper(x_uniform)
        elif kind == "average":
            y_uniform = functional_mean(interper, x_uniform)
        else:
            raise TypeError('kind must be "pointwise" or "average"')

        series.append(pd.Series(data=y_uniform, index=timestamps))

    if isinstance(data, pd.Series):
        return series[0]
    else:
        # dict(zip(.)) recreates original data structure with named columns
        # timestamps as index is already defined by the indivdual Series
        return pd.DataFrame(dict(zip(data.columns, series)))
