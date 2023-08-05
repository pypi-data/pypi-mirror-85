from typing import Callable


class Converter:
    """
    Creates a converter function between two units.

    Args:
        from_unit (str): Name of unit to convert from.
        to_unit (str): Name of unit to convert to.
        function (Callable): Function that converts from_unit to to_unit.
            The function must have one input argument and return a scalar.

    Returns:
        None
    """

    __slots__ = ["from_unit", "to_unit", "function"]

    def __init__(self, from_unit: str, to_unit: str, function: Callable):
        self.from_unit = from_unit
        self.to_unit = to_unit
        self.function = function
