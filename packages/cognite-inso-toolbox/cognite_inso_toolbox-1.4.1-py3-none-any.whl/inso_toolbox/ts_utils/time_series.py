from typing import List, Tuple

import numpy as np
import pandas as pd
from cognite.client import CogniteClient
from cognite.client.data_classes import DatapointsList, DatapointsQuery

PD_FREQ_HOUR = "h"
PD_FREQ_DAY = "D"
PD_FREQ_WEEK = "W"
PD_FREQ_MONTH_START = "MS"
LEGAL_PERIODIC_FREQS = {
    PD_FREQ_HOUR: "hour",
    PD_FREQ_DAY: "day",
    PD_FREQ_WEEK: "week",
    PD_FREQ_MONTH_START: "month start",
}
WEEK_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def _verify_and_convert_params_for_periodic_fetch(
    start: int, end: int, freq: str, week_start_day: str
) -> Tuple[pd.Timestamp, pd.Timestamp, str]:
    if freq not in LEGAL_PERIODIC_FREQS:
        raise ValueError(f"Periodic datapoint fetch only supports: {LEGAL_PERIODIC_FREQS}, got '{freq}'")

    if freq == PD_FREQ_WEEK:
        week_start_day = week_start_day.capitalize()
        if week_start_day not in WEEK_DAYS:
            raise ValueError(f"Expected 'week_start_day' to be one of {WEEK_DAYS}, got '{week_start_day}'")
        freq = "-".join((PD_FREQ_WEEK, week_start_day[:3].upper()))  # Match Pandas expectations

    round_freq = freq if freq == PD_FREQ_HOUR else PD_FREQ_DAY
    start = pd.Timestamp(start, unit="ms").floor(round_freq)
    end = pd.Timestamp(end, unit="ms").floor(round_freq)

    return start, end, freq


def _convert_dps_query_result_into_df(
    dpslst_lst: List[DatapointsList], ts_range_int: pd.DatetimeIndex, ts_range: np.ndarray
) -> pd.DataFrame:
    all_dps = [dps for dps_lst in dpslst_lst for dps in dps_lst]  # wut did I just read
    df = pd.concat(
        next((dp.to_pandas().assign(after_ts=ts) for dp in dps if dp.timestamp >= ts_int), pd.DataFrame({"value": []}),)
        for dps, ts_int, ts in zip(all_dps, ts_range_int, ts_range)
    ).dropna()
    return df.assign(lag_ms=(df.index - df["after_ts"]).astype(np.int64) / 1e6)


def fetch_periodic_datapoints(
    client: CogniteClient, external_id: str, start: int, end: int, freq: str, week_start_day: str = "Monday"
) -> pd.DataFrame:
    r"""
    Helper function to get the first raw, non-aggregated datapoint every hour/day/week/month.

    Args:
        client (CogniteClient): Instance of CogniteClient.
        external_id (str): External ID of the time series to fetch.
        start (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970 (UTC), minus leap seconds.
        end (int): The number of milliseconds since 00:00:00 Thursday, 1 January 1970 (UTC), minus leap seconds.
        freq (str): Wanted frequency of fetching, e.g.: ``h``: hour, ``D``: day, ``W``: week, ``MS``: month start.
        week_start_day (str): Only used for ``freq=W``, defines what day is considered the first in a week
            (default: ``Monday``).

    Returns:
        pd.DataFrame: Dataframe with three columns; *given external_id* and ``after_ts``, ``lag_ms`` indicating which
        query timestamp produces it - and its lag.

    Warning:
        Using ``freq=MS`` yields a non-fixed frequency, but is also one of the key selling points of this helper
        function(!).

    Hint:
        If you want higher resolution than ``hour``, it is likely that fetching all datapoints, then do the filtration
        yourself is faster

    Example:

        Get first datapoint each week, using Sunday as start of week:

            >>> client = CogniteClient(...)
            >>> first_datapoint_df = fetch_periodic_datapoints(
            ...        client, "foo-bar", start=123, end=456, freq="W", week_start_day="Sunday"
            ... )

    Note:
        This function sends a lot of parallel queries to CDF, so if performance is an issue, consider changing
        ``client.config.max_workers`` before calling (default: 10).
    """
    start, end, freq = _verify_and_convert_params_for_periodic_fetch(start, end, freq, week_start_day)
    ts_range = pd.date_range(start=start, end=end, freq=freq)
    ts_int_range = np.floor_divide(ts_range.asi8, 1e6).astype(int)
    dp_queries = [
        DatapointsQuery(external_id=external_id, start=ts_int, end=ts_int + 1, include_outside_points=True)
        for ts_int in ts_int_range
    ]
    api_results = client.datapoints.query(dp_queries)
    return _convert_dps_query_result_into_df(api_results, ts_int_range, ts_range).rename(columns={"value": external_id})
