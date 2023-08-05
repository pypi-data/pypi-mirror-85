import warnings
from typing import List, Optional

import pandas as pd
from cognite.client import CogniteClient

from .convert import convert


def convert_from_cdf(
    data: pd.DataFrame,
    client: CogniteClient,
    external_id: str,
    columns: List[str],
    to_unit: Optional[str] = None,
    inplace: bool = False,
) -> pd.DataFrame:
    """
    Convert specified columns in data from given unit in CDF to another unit.
    
    Args:
        data (pd.DataFrame): Data to be converted.
        client (CogniteClient): Client from which the time series unit will be retrieved.
        external_id (str): External id of time series.
        columns (List[str]): List of columns to convert.
        to_unit (str, optional): Specifies which unit the columns should be converted to.
            Default is to convert to SI units.
        inplace (bool, optional): Specifies whether to convert the data inplace or not.
    
    Returns:
        pd.DataFrame: Data with converted columns.
    """  # noqa
    from_unit = client.time_series.retrieve(external_id=external_id).unit

    if from_unit is not None:
        return convert(data, data.columns, from_unit, to_unit, inplace)

    else:
        warnings.warn(f"No unit was found for {external_id}. No unit conversion was done.", RuntimeWarning)
        return data
