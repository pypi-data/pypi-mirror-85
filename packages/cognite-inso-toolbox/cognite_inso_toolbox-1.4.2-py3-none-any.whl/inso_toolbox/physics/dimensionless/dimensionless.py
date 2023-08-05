from typing import Union

import numpy as np

# coming in the next numpy version!
# from numpy.typing import Numerical


Numerical = Union[float, np.ndarray]


def roughness_ratio(eps: Numerical, D: Numerical) -> Numerical:
    """
    Calculates the effective dimensionless roughness parameter eps_r as eps_r = eps / D.

    eps: Pipe roughness [m]
    D:   Pipe diameter  [m]
    """

    if np.any(D <= 0):
        raise ValueError("D must be a positive, non-zero number")

    roughness_r = eps / D
    return roughness_r


def reynolds_number(u: Numerical, rho: Numerical, mu: Numerical, L: Numerical,) -> Numerical:
    """
    Computes the Reynolds number as Re = rho*u*L / mu.

    Args:
        u (float or arraylike): Velocity [m/s]
        rho (float or arraylike): Density [kg/m3]
        mu (float or arraylike): Viscosity [kg/ms]
        L (float or arraylike): Length scale [m]     Often pipe diameter

    Returns:
        Reynolds number (float or arraylike)
    """

    if np.any(mu <= 0):
        raise ValueError("Viscosity mu must be a positive, non-zero number")

    rey_num = rho * u * L / mu
    return rey_num
