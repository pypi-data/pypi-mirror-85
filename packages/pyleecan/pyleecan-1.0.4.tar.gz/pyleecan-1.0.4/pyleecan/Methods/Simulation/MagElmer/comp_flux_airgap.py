# -*- coding: utf-8 -*-

from ....Functions.GMSH.draw_GMSH import draw_GMSH


def comp_flux_airgap(self, output, axes_dict):
    """Build and solve Elmer model to calculate and store magnetic quantities

    Parameters
    ----------
    self : MagElmer
        a MagElmer object
    output : Output
        an Output object
    axes_dict: {Data}
        Dict of axes used for magnetic calculation
    """

    # Init output dict
    out_dict = dict()

    # Get time and angular axes
    Angle = axes_dict["Angle"]
    Time = axes_dict["Time"]

    # Set the angular symmetry factor according to the machine and check if it is anti-periodic
    sym, is_antiper_a = Angle.get_periodicity()

    # Import angular vector from Data object
    angle = Angle.get_values(
        is_oneperiod=self.is_periodicity_a,
        is_antiperiod=is_antiper_a and self.is_periodicity_a,
    )
    Na = angle.size

    # Check if the time axis is anti-periodic
    _, is_antiper_t = Time.get_periodicity()

    # Number of time steps
    time = Time.get_values(
        is_oneperiod=self.is_periodicity_t,
        is_antiperiod=is_antiper_t and self.is_periodicity_t,
    )
    Nt = time.size

    # Get rotor angular position
    angle_rotor = output.get_angle_rotor()[0:Nt]

    # Interpolate current on magnetic model time axis
    # Get stator current from elec out
    if self.is_mmfs:
        Is = output.elec.comp_I_mag(time, is_stator=True)
    else:
        Is = None
    # Get rotor current from elec out
    if self.is_mmfr:
        Ir = output.elec.comp_I_mag(time, is_stator=False)
    else:
        Ir = None

    # Setup the Elmer simulation
    # Geometry building
    if not self.import_file:  # True if None or len == 0
        self.get_logger().debug("Drawing machine in GMSH...")
        # output.mag.FEA_dict = draw_GMSH() # TODO add inputs
        pass
    else:
        self.get_logger().debug("Reusing the FEA file: " + self.import_file)
        # output.mag.FEA_dict = self.FEA_dict
        pass

    # post process GMSH mesh with ElmerGrid
    # TODO add respective function (or method)

    # setup Elmer solver
    # TODO add respective functions or methods

    # Solve for all time step and store all the results in output
    Br, Bt, Bz, Tem, Phi_wind_stator = self.solve_FEA(
        output, sym, angle, time, angle_rotor, Is, Ir
    )

    # Store standards Magnetics outputs in out_dict
    out_dict["Br"] = Br
    out_dict["Bt"] = Bt
    out_dict["Bz"] = Bz
    out_dict["Tem"] = Tem
    out_dict["Phi_wind_stator"] = Phi_wind_stator

    # TODO store other Elmer outputs in out_dict

    return out_dict
