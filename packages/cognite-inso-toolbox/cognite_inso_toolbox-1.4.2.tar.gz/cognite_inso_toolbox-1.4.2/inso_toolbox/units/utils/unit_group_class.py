from typing import Callable, List, Optional

from .converter_class import Converter
from .unit_class import Unit


class UnitGroup:
    def __init__(self, name: str, units: List[Unit], converters: List[Converter] = None):
        self.name = name.upper()
        self.units = units
        self.converters = converters  # type: ignore

        if not self.si_unit:
            raise ValueError(f"No SI unit specified for {self.name}")

    @property
    def si_unit(self) -> Unit:
        si_units = [unit for unit in self.units if unit.is_si_unit]

        if len(si_units) != 1:
            raise ValueError(f"Exactly one of the {self.name} units has to be marked as a SI unit.")

        return si_units[0]

    @property
    def converters(self) -> List[Converter]:
        return self._converters

    @converters.setter
    def converters(self, converters: List[Converter]):
        if converters:
            unit_names = [unit.name for unit in self.units]
            for converter in converters:
                if not (converter.from_unit in unit_names and converter.to_unit in unit_names):
                    err_msg = f"""
                        Cannot find both [{converter.from_unit}] and [{converter.to_unit}]
                        among the {self.name} units: {unit_names}
                    """
                    raise ValueError(err_msg)
        else:
            converters = []
        self._converters = converters

    @property
    def unit_names(self):
        return [unit.name for unit in self.units]

    @property
    def recognized_unit_names(self):
        """Unit names and synonyms"""
        all_synonyms = []
        for unit in self.units:
            all_synonyms.extend(unit.synonyms)
        return self.unit_names + all_synonyms

    def __iter__(self):
        yield from self.units

    def find_unit_name(self, name: Optional[str] = None) -> str:
        for unit in self.units:
            if name in unit:
                return unit.name

        raise ValueError(f"Unit {name} not recognized.")

    def get_converter(self, from_unit: str, to_unit: Optional[str] = None) -> Callable:
        if not to_unit:
            to_unit = self.si_unit.name
        return self._get_converter(from_unit, to_unit)

    def _get_converter(self, from_unit: str, to_unit: Optional[str] = None) -> Callable:
        """Returns None if conversion is from the """
        if from_unit not in self.unit_names:
            from_unit = self.find_unit_name(from_unit)

        if to_unit not in self.unit_names:
            to_unit = self.find_unit_name(to_unit)

        if from_unit != to_unit:
            # Find and return the converter between the two units
            for converter in self.converters:
                if from_unit == converter.from_unit and to_unit == converter.to_unit:
                    return converter.function
        else:
            # If conversion to and from same unit
            return lambda x: x

        raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported.")
