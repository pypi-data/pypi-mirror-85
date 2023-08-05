import enum
import functools
from typing import Callable, Union

import numpy as np

from .darcy_friction import (
    _colebrook_dimless,
    _colebrook_fast_dimless,
    _colebrook_solve_dimless,
    _friction_factor_laminar_dimless,
    _haaland_dimless,
)

Numerical = Union[float, np.ndarray]


@enum.unique
class DarcyMethods(enum.Enum):
    """Collection of functions for calculating the darcy friction factor for turbulent flow, as a function of Reynolds
    number and effective roughness.  Members of this enumeration can be called and have the syntax described below. The
    four methods are different ways of solving the Colebrook-White equation, and are the following,

    See individual methods in ´inso_toolbox.physics.darcy_friction.py´ for more documentation.

    Members:
        * COLEBROOK: Uses the Lambert W function. Solves the equation exactly, but is relatively slow as the Lambert W
          function is solved iteratively.
        * COLEBROOK_SLOW: Solves the Colebrook-White equation using an iterative method.
        * COLEBROOK_FAST: An approximation to the Colebrook-White equation developed by D. Biberg[1].
        * HAALAND: The Haaland approximation to the Colebrook-White equation[2].

    References:
        * [1]: "Fast and Accurate Approximations for the Colebrook Equation", Dag Biberg,
          Journal of Fluids Engineering Copyright VC 2017 by ASME MARCH 2017, Vol. 139 / 031401-1,
          https://doi.org/10.1115/1.4034950
        * [2]: Haaland, SE (1983). "Simple and Explicit Formulas for the Friction Factor in Turbulent Flow". Journal of
          Fluids Engineering. 105 (1): 89–90. doi:10.1115/1.3240948.
    """

    COLEBROOK = functools.partial(_colebrook_dimless)
    COLEBROOK_SLOW = np.vectorize(_colebrook_solve_dimless)
    COLEBROOK_FAST = functools.partial(_colebrook_fast_dimless)
    HAALAND = functools.partial(_haaland_dimless)

    def __call__(self, rey_num, epsilon_r, **kwargs):
        """
        Calls the function represented by the DarcyMethods member value.

        Args:
            rey_num (float or np.ndarray): Reynolds number = rho * u * D / mu
            epsilon_r (float): Pipe's relative roughness, given as pipe effective
                roughness (epsilon) scaled with the pipe diameter (D) - epsilon_r = epsilon / D

        Returns:
            f_c (float or np.ndarray): darcy_friction_factor for turbulent flow.

        """
        return self.value(rey_num, epsilon_r, **kwargs)


def darcy_friction_factor_dimless(
    rey_num: Numerical,
    epsilon_r: Numerical,
    laminar_limit: float = 2300,
    turbulent_limit: float = 4000,
    method: Union[DarcyMethods, Callable] = None,
) -> Numerical:
    """
    Computes the Darcy friction factor for pipe flow, for both laminar and turbulent regimes. The transition regime
    between laminar and turbulent is given as   . The laminar-turbulent transition is given by the transition limits

    Args:
        - rey_num (float or np.ndarray): Reynolds number = rho*u*D/mu.
        - epsilon_r (float or np.ndarray): Pipe's relative roughness, given as pipe effective
          roughness (epsilon) scaled with the pipe diameter (D) - epsilon_r = epsilon / D
        - laminar_limit (float): Limit where lower Reynolds numbers give pure laminar flow.
        - turbulent_limit (float): Limit where higher Reynolds numbers give pure turbulent flow.
        - method (callable): The method to calculate the darcy friction factor in the turbulent regime.
          Possible arguments:

            * Any DarcyMethods member
            * other callables with the signature f(Union[float, np.ndarray], float) -> float.
    """
    if method is None:
        method = DarcyMethods.COLEBROOK_FAST
    if not callable(method):
        raise TypeError("Method must be a callable or part of the DarcyMethods Enum.")

    rey_num = np.asarray(rey_num)

    if laminar_limit > turbulent_limit:
        raise ValueError("Turbulent limit must be higher than laminar limit.")

    lam_mask = rey_num < laminar_limit
    turb_mask = rey_num > turbulent_limit
    both_mask = ~(lam_mask | turb_mask)

    res_lam = np.array([], dtype=np.float64)
    res_turb = res_lam.copy()
    res_both = res_lam.copy()

    if np.any(lam_mask):
        res_lam = _friction_factor_laminar_dimless(rey_num[lam_mask])

    if np.any(turb_mask):
        res_turb = method(rey_num[turb_mask], epsilon_r)

    if np.any(both_mask):
        res_both_lam = _friction_factor_laminar_dimless(rey_num[both_mask])
        res_both_turb = method(rey_num[both_mask], epsilon_r)
        laminar_fraction = (rey_num[both_mask] - laminar_limit) / (turbulent_limit - laminar_limit)
        res_both = res_both_turb * laminar_fraction + (1 - laminar_fraction) * res_both_lam

    return np.concatenate([res_lam, res_both, res_turb]).reshape(rey_num.shape)
