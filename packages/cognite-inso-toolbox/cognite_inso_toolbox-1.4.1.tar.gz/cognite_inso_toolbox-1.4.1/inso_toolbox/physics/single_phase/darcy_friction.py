import math
import warnings
from typing import Union

import numpy as np
from scipy.optimize import root_scalar
from scipy.special import lambertw

Numerical = Union[float, np.ndarray]


def _friction_factor_laminar_dimless(rey_num: Numerical) -> Numerical:
    """
    Friction factor for laminar pipe flow.

    Args:
        rey_num (float or np.ndarray): Reynolds number = rho*u*D/mu

    Returns:
        laminar friction factor (float or np.ndarray) : defined as f_c = 64 / rey_num
    """
    return 64 / rey_num


def _colebrook_solve_dimless(rey_num: float, epsilon_r: float, **kwargs) -> float:
    """
    Colebrook equations for the Darcy friction factor. Solves the implicit colebrook equation using the brentq method.

    Args:
        rey_num (float): Reynolds number = rho*u*D/mu
        epsilon_r (float): Pipe's relative roughness, given as pipe effective roughness (epsilon) scaled with the pipe
            diameter (D) - epsilon_r = epsilon / D
        **kwargs: Extra arguments passed on to scipy.optimize.root_scalar. Can overwrite the default arguments
            given by

            * method = "brentq"
            * xtol = 1.48e-08
            * maxiter = 50

    Returns:
        darcy_friction, f (float or np.ndarray): The Darcy-Weisbach friction factor for a full-flowing circular pipe.
    """

    if np.size(rey_num) > 1 or np.size(epsilon_r) > 1:
        msg = "_colebrook_solve_dimless only available for scalar input."

        # note, this is because scipy does not include vectorized version of a stable root solver.
        raise ValueError(msg)

    f_init = _haaland_dimless(rey_num, epsilon_r)

    def res_colebrook(f, rey_num, epsilon_r):
        sqrtf = math.sqrt(f)
        res = 1 / sqrtf + 2 * math.log10(epsilon_r / 3.7 + 2.51 / (rey_num * sqrtf))
        return res

    # avoid zero-division error
    lower = 1 / (2 * math.log10(max(epsilon_r, 1e-15) / 3.7)) ** 2 / 2
    # ad hoc upper limit
    upper = 1e2

    root_kwargs = dict(xtol=1.48e-08, maxiter=50, method="brentq")
    root_kwargs.update(kwargs)

    res = root_scalar(res_colebrook, bracket=(lower, upper), args=(rey_num, epsilon_r), **root_kwargs)

    if res.converged:
        return res.root
    else:
        warnings.warn("Colebrook equation did not converge, using Haaland value instead.")
        return f_init


def _colebrook_dimless(rey_num: Numerical, epsilon_r: Numerical) -> Numerical:
    """
    Solves the colebrook equations using the Lambert W function.

    Args:
        rey_num (float or np.ndarray): Reynolds number = rho*u*D/mu
        epsilon_r (float or np.ndarray): Pipe's relative roughness, given as pipe effective
            roughness (epsilon) scaled with the pipe diameter (D) - epsilon_r = epsilon / D

    Returns:
        darcy_friction, f (float or np.ndarray): The Darcy-Weisbach friction factor for a full-flowing circular pipe.

    Note:
        Fails for values of Reynolds number > 5x10^8.
    """
    try:
        with np.errstate(divide="raise"):
            a = 2.51 / rey_num
    except (ZeroDivisionError, FloatingPointError) as e:
        raise ValueError("Reynolds number must be non-zero") from e

    b = epsilon_r / 3.7

    argument = math.log(10) / (2 * a) * 10 ** (b / (2 * a))
    denom = 2 * lambertw(argument) / math.log(10) - b / a

    if np.any(denom.imag != 0):
        if np.any(np.isinf(argument)):
            raise ValueError(
                "_colebrook_dimless overflows for large values of reynolds number and/or epsilon_r. "
                "Use another colebrook method"
            )
        else:
            raise ValueError("Numerical error in solving colebrook equation.")

    return (1 / denom ** 2).real


def _colebrook_fast_dimless(rey_num: Numerical, epsilon_r: Numerical) -> Numerical:
    """
    Fast approximation of the colebrook equation, from [1].

    Args:
        rey_num (float or np.ndarray): Reynolds number = rho*u*D/mu
        epsilon_r (float or np.ndarray): Pipe's relative roughness, given as pipe effective
            roughness (epsilon) scaled with the pipe diameter (D) - epsilon_r = epsilon / D

    Returns:
        darcy_friction, f (float or np.ndarray): The Darcy-Weisbach friction factor for a full-flowing circular pipe.

    References:
        [1] "Fast and Accurate Approximations for the Colebrook Equation", Dag Biberg,
            Journal of Fluids Engineering Copyright VC 2017 by ASME MARCH 2017, Vol. 139 / 031401-1,
            https://doi.org/10.1115/1.4034950
    """
    a = 2 / math.log(10)
    b = 2.51
    c = 3.7
    ab = a * b

    try:
        with np.errstate(divide="raise", invalid="raise"):
            log_re_ab = np.log(rey_num / ab)
    except FloatingPointError as e:
        raise ValueError("Reynolds number must be non-zero") from e

    x = log_re_ab + rey_num * epsilon_r / (ab * c)

    g = np.log(x) * (2 / x - 1)
    denominator = a * (log_re_ab + g)
    fric = (1 / denominator) ** 2
    return fric


def _haaland_dimless(rey_num: Numerical, epsilon_r: Numerical) -> Numerical:
    """
    Haaland approximation of the Colebrook equation,
    https://en.wikipedia.org/wiki/Darcy_friction_factor_formulae#Haaland_equation.

    Args:
        rey_num (float or np.ndarray): Reynolds number = rho*u*D/mu
        epsilon_r (float or np.ndarray): Pipe's relative roughness, given as pipe effective
            roughness (epsilon) scaled with the pipe diameter (D) - epsilon_r = epsilon / D

    Returns:
        darcy_friction, f (float or np.ndarray): The Darcy-Weisbach friction factor for a full-flowing circular pipe.
    """
    flow_rough = (epsilon_r / 3.7) ** 1.11
    try:
        with np.errstate(divide="raise"):
            flow_smooth = 6.9 / rey_num
    except (ZeroDivisionError, FloatingPointError) as e:
        raise ValueError("Reynolds number must be non-zero") from e

    try:
        with np.errstate(divide="raise", invalid="raise"):
            denom = -1.8 * np.log10(flow_rough + flow_smooth)
    except FloatingPointError as e:
        raise ValueError("Numerical error in solving colebrook equation, check input.") from e
    flow_rough = (epsilon_r / 3.7) ** 1.11
    flow_smooth = 6.9 / rey_num
    denom = -1.8 * np.log10(flow_rough + flow_smooth)
    f = (1 / denom) ** 2
    return f
