import warnings
from typing import Union

import pandas as pd

from inso_toolbox.utils.helpers import check_uniform, make_uniform


def rolling_average_drift_detector(
    data: Union[pd.DataFrame, pd.Series],
    long_term_interval: str,
    short_term_interval: str,
    std_threshold: float,
    resolution: str,
    detect: str = "both",
) -> pd.DataFrame:
    """
        Drift detection algorithm comparing the rolling average of the a given long and short term interval.
        The deviation between the short and long term average is considered significant if it is above the given
        threshold times the rolling standard deviation of the long term interval.


        Args:
            data (Union[pd.DataFrame, pd.Series]): Data to detect drift on. Index must be datetime and dataframe can
             only contain one column in addition to index.
            long_term_interval (str): Length of long term interval. Follows Pandas DateTime convention.
            short_term_interval (str): Length of short term interval. Follows Pandas DateTime convention.
            std_threshold (float): Parameter that determines the threshold for what is considered a significant change.
             The threshold is set to long term rolling standard deviation times the parameter std_threshold.
            resolution (str): Temporal resolution for resampling if the timeseries is not uniform. Follows Numpy
             DateTime convention.
            detect (str, optional): Parameter to determine if the model should detect significant decreases, increases
             or both (either "decrease", "increase" or "both").


        Returns:
            pd.DataFrame: Dataframe with a new column ``drift`` which indicates if the time series is drifting (1) or
            steady (0).


        Warning:
            The returned dataframe does not include the first datapoints which are within the length of the long term
            interval, as rolling average and standard deviation cannot be computed for these values.


        Example:
            Drift detection setting the long term to 8 days, short term to 12 hours, threshold to 3 times rolling long
            term std, granularity to 1 minute, and detecting direction to both.

            >>> data = rolling_average_drift_detector(data, long_term_interval='3d', short_term_interval='4h',
            >>>                                       std_threshold=3, resolution='1 min', detect='both')

        """

    # Only pd.Series and pd.DataFrame inputs are supported
    assert isinstance(data, pd.Series) or isinstance(
        data, pd.DataFrame
    ), "Only pd.Series and pd.DataFrame inputs are supported."

    # Only one column in DataFrame
    if isinstance(data, pd.DataFrame):
        assert len(data.columns) == 1, "Input data can only have one column."

    if isinstance(data, pd.Series):
        df = data.to_frame()
    else:
        df = data.copy()

    # Warn user if there are any missing values
    if df.isna().any(axis=None):
        warnings.warn("There are missing values present in the time series.", RuntimeWarning)

    column_name = df.columns[0]

    # Control the data is uniform, if not then resample to given resolution
    if not check_uniform(df):
        df = make_uniform(df, resolution=resolution, interpolation="linear")

    # Compute long term average and std
    df["long_term_average"] = df[column_name].rolling(long_term_interval).mean()
    df["long_term_stds"] = df[column_name].rolling(long_term_interval).std()

    # Compute short term average
    df["short_term_average"] = df[column_name].rolling(short_term_interval).mean()

    # Remove values within the first long term interval
    start_ts = df.index[0] + pd.Timedelta(long_term_interval)
    df = df.loc[start_ts:, :].copy()

    # initialize boolean drift column
    df["drift"] = [0] * df.count().max()

    if detect == "both" or detect == "increase":
        df.loc[df["short_term_average"] > df["long_term_average"] + std_threshold * df["long_term_stds"], "drift"] = 1

    if detect == "both" or detect == "decrease":
        df.loc[df["short_term_average"] < df["long_term_average"] - std_threshold * df["long_term_stds"], "drift"] = 1

    df = df.dropna()

    return df[[column_name, "drift"]]
