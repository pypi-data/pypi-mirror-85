# -*- coding: utf-8 -*-

from ....Classes.OutMag import OutMag
from ....Classes.Simulation import Simulation
from ....Methods.Simulation.Input import InputError


def gen_input(self):
    """Generate the input for the structural module (magnetic output)

    Parameters
    ----------
    self : InFlux
        An InFlux object
    """

    output = OutMag()

    # get the simulation
    if isinstance(self.parent, Simulation):
        simu = self.parent
    elif isinstance(self.parent.parent, Simulation):
        simu = self.parent.parent
    else:
        raise InputError(
            "ERROR: InputCurrent object should be inside a Simulation object"
        )

    # Set discretization
    if self.OP is None:
        N0 = None  # N0 can be None if time isn't
    else:
        N0 = self.OP.N0
    Time, Angle = self.comp_axes(simu.machine, N0)
    output.Time = Time
    output.Angle = Angle

    if self.B is None:
        raise InputError("ERROR: InFlux.B missing")
    if self.B.name is None:
        self.B.name = "Airgap flux density"
    if self.B.symbol is None:
        self.B.symbol = "B"
    B = self.B.get_data()
    output.B = B

    if self.parent.parent is None:
        raise InputError(
            "ERROR: The Simulation object must be in an Output object to run"
        )
    # Save the Output in the correct place
    self.parent.parent.mag = output

    # Define the electrical Output to set the Operating Point
    if self.OP is not None:
        self.OP.gen_input()
