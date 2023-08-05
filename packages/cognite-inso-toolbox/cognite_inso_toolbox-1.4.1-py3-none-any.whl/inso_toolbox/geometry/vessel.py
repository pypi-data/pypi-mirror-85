import enum
from typing import Dict, List, Optional, Set, Union

import numpy as np
from scipy.optimize import brentq


@enum.unique
class VesselHeads(enum.Enum):
    """Defines unique key value pairs to specify the implemented vessel heads."""

    SPHERICAL = "spherical"
    ELLIPSOIDAL = "ellipsoidal 2:1"
    CYLINDRICAL = "flat"
    AMSE_TORISPHERICAL = "amse torispherical"


available_vessel_heads = [head.name for head in VesselHeads]


class Vessel:
    """Class for the calculation of liquid volumes from liquid elevation and vice versa in pressure vessels.

    The heads (or dishes) are approximated as ellipsoidal, specified by the ratio of the semi-minor to the semi-major
    axis. Also supports the use of a weir to divide the vessel in two, where the word weir is a misnomer as it is
    assumed to cover the entire tank diameter.

    Args:
        length (float): length of cylindrical part of vessel
        inner_diameter (float): inner diameter of cylindrical part of vessel
        head_ratio (float, optional):
            Ratio of the semi minor axis to the semi major axis.  Values of C = 1 and C = 0.5
            gives exact partial volumes for spherical and 2:1 ellipsoidal heads,
            respectively. Errors of total volume calculations for AMSE heads are less 0.001%[1].
        head_type (VesselHeads, optional): Specifies the head-type if ``head_ratio`` is not given. See available
            types in inso_toolbox.geometry.vessel.available_vessel_heads. Default ``spherical``
        head_params: (dict, optional): Additional head parameters for non-ellipsoidal heads.

    References:
        [1] : B. Wiencke, Computing the partial volume of pressure vessels,
              https://www.sciencedirect.com/science/article/abs/pii/S0140700709002734
    """

    _required_head_params: Dict[VesselHeads, List[str]] = {
        VesselHeads.SPHERICAL: [],
        VesselHeads.ELLIPSOIDAL: [],
        VesselHeads.CYLINDRICAL: [],
        VesselHeads.AMSE_TORISPHERICAL: ["vessel_wall_thickness"],
    }

    def __init__(
        self,
        length: float,
        inner_diameter: float,
        head_type: VesselHeads = VesselHeads.SPHERICAL,
        head_ratio: Optional[float] = None,
        head_params: Dict[str, float] = {},
    ):
        self._length = length
        self._inner_diameter = inner_diameter

        if head_ratio is None:
            head_ratio = self.get_head_ratio(head_type, inner_diameter=inner_diameter, **head_params)
        self._head_ratio = head_ratio

    @property
    def inner_diameter(self):
        """Inner diameter of vessel"""
        return self._inner_diameter

    @property
    def head_ratio(self):
        """Ratio between semi-major and semi-minor axis of the vessel head when approximated as ellipsoidal."""
        return self._head_ratio

    @property
    def length(self):
        """Length of cylindrical part of vessel, excluding the head."""
        return self._length

    @staticmethod
    def get_head_ratio(head_type: VesselHeads, **head_params) -> float:
        """Calculates the ratio between semi-major axis and semi-minor axis for a given vessel head approximated as an
        ellipsoid.

        Args:
            head_type (VesselHeads): See VesselHeads class for implemented head types.
            **head_params: Additional keyword parameters for different head types. Required arguments:

                * inner_diameter for amse torispherical
                * vessel_wall_thickness for amse torispherical and,
                * inside_knuckle_radius for amse torispherical heads (optional, default = 3 * vessel_wall_thickness)

        Returns:
            ratio (float): ratio between semi-major and semi-minor axis of an ellipsoid approximating the vessel head
        """

        try:
            missing_params: Set[str] = set(Vessel._required_head_params[head_type]) - set(head_params.keys())
        except KeyError:
            raise NotImplementedError(f"Head type {head_type} not implemented")
        if missing_params:
            raise ValueError(f"Head type {head_type} requires parameters {missing_params}")

        if head_type is VesselHeads.SPHERICAL:
            return 1.0
        elif head_type is VesselHeads.ELLIPSOIDAL:
            return 0.5
        elif head_type is VesselHeads.CYLINDRICAL:
            return 0.0
        elif head_type is VesselHeads.AMSE_TORISPHERICAL:
            t = head_params["vessel_wall_thickness"]
            D_i = head_params["inner_diameter"]
            R_k = head_params.get("inside_knuckle_radius", t * 3)
            D_o = t + D_i  # outside diameter
            return 0.30939 + 1.7197 * (R_k - 0.06 * D_o) / D_i - 0.16116 * (t / D_o) + 0.98997 * (t / D_o) ** 2
        else:
            raise NotImplementedError(f"Head type {head_type} not implemented")

    @staticmethod
    def head_volume(h: Union[float, np.ndarray], D_i: float, C: float) -> Union[float, np.ndarray]:
        """
        Approximates the filled volume of a single head as the volume of a semi-ellipsoidal vessel head.

        The parameter C is the between the semi-major and semi-minor axis a and b, respectively, given as C = b / a.
        Corresponding values are defined by AMSE for different head standards. C=1 and C=0.5 corresponds to spherical
        and 2:1 ellipsoidal heads.

        Args:
            h (float or np.ndarray): Height of liquid, 0 < h < D_i. [length]
            D_i (float): Semi-major axis, given by inner diameter of vessel. [length]
            C (float): Ratio between semi-major and semi-minor axis. [unitless]

        Returns:
            The filled volume of the head. [length^3]
        """

        # ensure height is between 0 and diameter
        if np.any(h < 0) or np.any(h > D_i):
            raise ValueError(f"All values of liquid height 'h' must be between 0 and inner diameter D_i = {D_i}")

        # calculate volume
        return D_i ** 3 * C * np.pi / 12 * (3 * (h / D_i) ** 2 - 2 * (h / D_i) ** 3)

    @staticmethod
    def cylinder_volume(h: Union[float, np.ndarray], L: float, D_i: float) -> Union[float, np.ndarray]:
        """
        Calculates the filled volume for a liquid at elevation h inside a a horizontal cylinder of length L and diameter
        D_i, for a liquid at elevation h.  See [1] for derivation.

        Args:
            h (float or np.ndarray): Height of liquid, 0 < h < D_i. [length]
            L (float): Length of cylinder . [length]
            D_i (float): Inner diameter of cylinder. [length]

        Returns:
            The filled volume of the cylinder. [length^3]

        References:
            [1] : Barderas, Stephania, Rodea, How to calculate the volumes of partially full tanks,
                https://www.researchgate.net/publication/301674653_HOW_TO_CALCULATE_THE_VOLUMES_OF_PARTIALLY_FULL_TANKS
        """

        # ensure height is between 0 and diameter
        if np.any(h < 0) or np.any(h > D_i):
            raise ValueError(f"All values of liquid height 'h' must be between 0 and inner diameter D_i = {D_i}")

        R = D_i / 2  # inner radius of vessel

        # calculate volume
        sector_area = L * R ** 2 * np.arccos(1 - h / R)
        triangle_area = L * (R - h) * np.sqrt(2 * R * h - h ** 2)
        return sector_area - triangle_area

    def partially_filled_volume(
        self, elevation: Union[float, np.ndarray], weir_loc: float = 0
    ) -> Union[float, np.ndarray]:
        """
        Calculates the volume of a liquid at a given elevation, possibly with a weir dividing the vessel in two.

        Args:
            elevation (float or np.ndarray): Height of liquid inside vessel
            weir_loc (float, optional): Location of weir, weir_loc = 0 indicates no weir. If present, a single head and
                the cylindrical portion up to the weir is used for volume calculation.

        Returns:
            The filled volume of the vessel (float or np.ndarray)
        """

        # ensure weir is in the cylindrical part of vessel
        if weir_loc < 0 or weir_loc > self.length:
            raise ValueError(f"Expected weir_loc between 0 and length of vessel L = {self.length}, got {weir_loc}")

        effective_length = self.length - weir_loc
        vol_cyl = self.cylinder_volume(elevation, effective_length, self.inner_diameter)
        vol_head = self.head_volume(elevation, self.inner_diameter, self.head_ratio)

        # if no weir, add vol of both heads
        if not weir_loc:
            vol_head *= 2

        return vol_cyl + vol_head

    def full_volume(self, weir_loc: float = 0) -> float:
        """
        Calculates the full volume of the vessel, possibly with a weir dividing the vessel in two.

        Args:
            weir_loc (float, optional): Location of weir, weir_loc = 0 indicates no weir. If present, a single head and
                the cylindrical portion up to the weir is used for volume calculation.
        Returns:
            The full volume of the vessel (float)
        """

        return self.partially_filled_volume(elevation=self.inner_diameter, weir_loc=weir_loc)

    def elevation_from_volume(self, volume: float, weir_loc: float = 0, **minimize_kwargs):
        """
        Calculates the inverse of ``partially_filled_volume``, i.e. calculates the liquid elevation as a function of the
        filled volume.

        A weir boundary may be included at a location given by weir_loc, with which only the volume inside weir_loc is
        used.

        Args:
            volume (float): Volume of the liquid.
            weir_loc (float, optional): Weir location. If present, only a single head and the cylindrical length up to
                the weir location is used for the volume calculation.

        Returns:
            Liquid elevation (float).
        """

        max_volume = self.full_volume(weir_loc=weir_loc)

        if volume < 0 or volume > max_volume:
            raise ValueError(f"Expected volume between 0 and self.full_volume()={max_volume}, got {volume}")

        def minimize_func(h: float, weir_loc: float) -> float:
            return self.partially_filled_volume(h, weir_loc=weir_loc) - volume

        return brentq(minimize_func, args=(weir_loc,), a=0, b=self.inner_diameter, **minimize_kwargs)
