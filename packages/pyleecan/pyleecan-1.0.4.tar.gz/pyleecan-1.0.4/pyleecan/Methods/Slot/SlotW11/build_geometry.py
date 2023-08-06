# -*- coding: utf-8 -*-

from ....Classes.Arc1 import Arc1
from ....Classes.Arc3 import Arc3
from ....Classes.Segment import Segment


def build_geometry(self):
    """Compute the curve (Line) needed to plot the object.
    The ending point of a curve is the starting point of the next curve
    in the list

    Parameters
    ----------
    self : SlotW11
        A SlotW11 object

    Returns
    -------
    curve_list: list
        A list of 7 Segment and 2 Arc1

    """

    [Z1, Z2, Z3, Z4, Z5, Z6, Z7, Z8, Z9, Z10, rot_sign] = self._comp_point_coordinate()

    # Creation of curve
    curve_list = list()
    curve_list.append(Segment(Z1, Z2))
    curve_list.append(Segment(Z2, Z3))
    curve_list.append(Segment(Z3, Z4))
    if self.R1 * 2 < self.W2:
        curve_list.append(
            Arc1(Z4, Z5, rot_sign * self.R1, is_trigo_direction=self.is_outwards())
        )
        curve_list.append(Segment(Z5, Z6))
        curve_list.append(
            Arc1(Z6, Z7, rot_sign * self.R1, is_trigo_direction=self.is_outwards())
        )
    else:
        curve_list.append(Arc3(Z4, Z7, self.is_outwards()))
    curve_list.append(Segment(Z7, Z8))
    curve_list.append(Segment(Z8, Z9))
    curve_list.append(Segment(Z9, Z10))

    return curve_list
