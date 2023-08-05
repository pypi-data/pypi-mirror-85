from typing import List


class Unit:
    """
    Creates a unit. The name and synonymns must be unique from all other unit names.

    Args:
        name (str): Name of the unit. Must be unique.
        synonyms (List(str), optional): Other possible names for the unit. Must all be unique.
        is_si_unit (bool, optioanl): Specifies whether to use this as the default unit.

    Returns:
        None
    """

    def __init__(self, name: str, synonyms: List[str] = None, is_si_unit: bool = False):
        self.name = name
        self.is_si_unit = is_si_unit
        self.synonyms = synonyms if synonyms else []

    def __iter__(self):
        """Iterates over all possible names"""
        yield self.name
        yield from self.synonyms
