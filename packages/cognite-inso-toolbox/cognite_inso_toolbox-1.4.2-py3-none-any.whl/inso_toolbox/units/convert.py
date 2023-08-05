from typing import List, Optional

import pandas as pd

from inso_toolbox.utils import pipeline_function

from .units import _UNITS
from .utils.units_docstring import list_units_docstring


@pipeline_function
@list_units_docstring
def convert(
    data: pd.DataFrame, columns: List[str], from_unit: str, to_unit: Optional[str] = None, inplace: bool = False
) -> pd.DataFrame:
    """
    Convert specified columns in data from given unit to another unit.
    
    Args:
        data (pd.DataFrame): Data to be converted.
        columns (List[str]): List of columns to convert.
        from_unit (str): Current unit of the specified columns.
        to_unit (str, optional): Specifies which unit the columns should be converted to.
            Default is to convert to SI units.
        inplace (bool, optional): Specifies whether to convert the data inplace or not.
    
    Returns:
        pd.DataFrame: Data with converted columns.
    """  # noqa
    f = _UNITS.get_converter(from_unit=from_unit, to_unit=to_unit)

    if not inplace:
        data = data.copy(deep=True)

    data[columns] = f(data[columns])

    return data
