from typing import Callable, List, Optional

from .converter_class import Converter
from .unit_class import Unit
from .unit_group_class import UnitGroup


class Units:
    def __init__(self):
        self._unit_groups = {}
        self._unit_to_group_mapping = {}
        self._group_names = set()
        self._unit_names = dict()
        self._docstring = """"""

    @property
    def _recognized_unit_names(self):
        return self._unit_to_group_mapping.keys()

    def _add_unit_mapping(self, unit_group: UnitGroup) -> None:
        for unit_name in unit_group.recognized_unit_names:
            self._unit_to_group_mapping[unit_name] = unit_group.name

    def add_group(self, group_name: str, units: List[Unit], converters: List[Converter] = None) -> None:
        """
        Method to add a group of units. A group consists of one units and converters between those units.
        Each group must exactly have one SI (default) unit.

        Args:
            group_name (str): A unique name for the unit grouping.
            units (List[Unit]): Units to include in the group. All units added to this class must have unique names
                and synonyms.
            converters (List[Converter]): Converters between units in the group.

        Returns:
            None
        """
        # Check for unique group name
        if group_name in self._group_names:
            raise ValueError(f"Duplicate group name: {group_name}.")
        self._group_names.add(group_name)
        self._docstring += fr"""
        Group: {group_name}

        """

        # Store names of units in the current group
        group_units = set()

        # Check that all unit names and synonyms are unique with all previously added units
        for unit in units:
            equivalent_names = []
            for name in unit:
                if name in self._unit_names:
                    raise ValueError(
                        f"Duplicate unit {name} (exists in both {self._unit_names[name]} and {group_name} unit groups)."
                    )
                self._unit_names[name] = group_name
                group_units.add(name)

                equivalent_names.append(name)

            # Add to docstring
            if unit.is_si_unit:
                self._docstring += fr"""
                * {", ".join(equivalent_names)} (SI Unit)

                """
            else:
                self._docstring += fr"""
                * {", ".join(equivalent_names)}

                """

        # Check that converters convert between units only present in the current group
        if converters is not None:
            for converter in converters:
                if converter.from_unit not in group_units:
                    raise ValueError(
                        "Converting from {} to {} is not possible because {} is not in the {} unit group".format(
                            converter.from_unit, converter.to_unit, converter.from_unit, group_name
                        )
                    )
                if converter.to_unit not in group_units:
                    raise ValueError(
                        "Converting from {} to {} is not possible because {} is not in the {} unit group.".format(
                            converter.from_unit, converter.to_unit, converter.to_unit, group_name
                        )
                    )

        # Assert that there is exactly one SI unit in the group
        if sum(unit.is_si_unit for unit in units) != 1:
            raise ValueError(f"There must be exactly one SI (default) unit in the {group_name} unit group.")

        # Add the unit group to the interal list
        self._add_unit_group(UnitGroup(group_name, units, converters))

    def _add_unit_group(self, unit_group: UnitGroup) -> None:
        self._unit_groups[unit_group.name] = unit_group
        self._add_unit_mapping(unit_group)

    def get_converter(self, from_unit: str, to_unit: Optional[str] = None) -> Callable:
        """Find which UnitGroup to delegate converter search to"""
        # Convert units to lower case
        from_unit = from_unit.lower()
        to_unit = to_unit.lower() if to_unit else None

        # Check if conversion is supported and return converter function
        if from_unit in self._recognized_unit_names and (to_unit in self._recognized_unit_names or not to_unit):
            unit_group_name = self._unit_to_group_mapping.get(from_unit)
            unit_group = self._unit_groups.get(unit_group_name)
            return unit_group.get_converter(from_unit, to_unit)
        else:
            err_msg = f"""
                Conversion from {from_unit} to {to_unit} not supported
                or {from_unit} and/or {to_unit} not a recognized unit.

                Please add the unit or converter to the inso_toolbox.units.units.py file.
            """
            raise ValueError(err_msg)

    def get_docstring(self):
        msg = "Units are placed in groups and can be converted to any other unit within its group. "
        msg += (
            "Each unit group has exactly one default (SI) unit. Most units can be referenced by various names. If there"
        )
        msg += " are any units or unit groups missing please add them to the ``inso_toolbox.units.units.py`` file. "
        msg += "These are the currently existing unit groups:"
        docstring = f"""{msg}

        """
        docstring += self._docstring
        return docstring
