from inso_toolbox.units.units import _UNITS


def list_units_docstring(func):
    """
    Fetches all units and adds them in a list to the docstring.
    """

    def _decorator(func):
        func.__doc__ = "".join([func.__doc__, _UNITS.get_docstring()])
        return func

    return _decorator(func)
