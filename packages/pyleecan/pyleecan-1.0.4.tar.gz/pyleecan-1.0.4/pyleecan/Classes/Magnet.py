# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Machine/Magnet.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Machine/Magnet
"""

from os import linesep
from logging import getLogger
from ._check import check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from ._frozen import FrozenClass

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Machine.Magnet.comp_angle_opening import comp_angle_opening
except ImportError as error:
    comp_angle_opening = error

try:
    from ..Methods.Machine.Magnet.comp_height import comp_height
except ImportError as error:
    comp_height = error

try:
    from ..Methods.Machine.Magnet.comp_mass import comp_mass
except ImportError as error:
    comp_mass = error

try:
    from ..Methods.Machine.Magnet.comp_ratio_opening import comp_ratio_opening
except ImportError as error:
    comp_ratio_opening = error

try:
    from ..Methods.Machine.Magnet.comp_surface import comp_surface
except ImportError as error:
    comp_surface = error

try:
    from ..Methods.Machine.Magnet.comp_volume import comp_volume
except ImportError as error:
    comp_volume = error

try:
    from ..Methods.Machine.Magnet.is_outwards import is_outwards
except ImportError as error:
    is_outwards = error

try:
    from ..Methods.Machine.Magnet.plot import plot
except ImportError as error:
    plot = error


from ._check import InitUnKnowClassError
from .Material import Material


class Magnet(FrozenClass):
    """abstract class of magnets"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Machine.Magnet.comp_angle_opening
    if isinstance(comp_angle_opening, ImportError):
        comp_angle_opening = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Magnet method comp_angle_opening: "
                    + str(comp_angle_opening)
                )
            )
        )
    else:
        comp_angle_opening = comp_angle_opening
    # cf Methods.Machine.Magnet.comp_height
    if isinstance(comp_height, ImportError):
        comp_height = property(
            fget=lambda x: raise_(
                ImportError("Can't use Magnet method comp_height: " + str(comp_height))
            )
        )
    else:
        comp_height = comp_height
    # cf Methods.Machine.Magnet.comp_mass
    if isinstance(comp_mass, ImportError):
        comp_mass = property(
            fget=lambda x: raise_(
                ImportError("Can't use Magnet method comp_mass: " + str(comp_mass))
            )
        )
    else:
        comp_mass = comp_mass
    # cf Methods.Machine.Magnet.comp_ratio_opening
    if isinstance(comp_ratio_opening, ImportError):
        comp_ratio_opening = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Magnet method comp_ratio_opening: "
                    + str(comp_ratio_opening)
                )
            )
        )
    else:
        comp_ratio_opening = comp_ratio_opening
    # cf Methods.Machine.Magnet.comp_surface
    if isinstance(comp_surface, ImportError):
        comp_surface = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Magnet method comp_surface: " + str(comp_surface)
                )
            )
        )
    else:
        comp_surface = comp_surface
    # cf Methods.Machine.Magnet.comp_volume
    if isinstance(comp_volume, ImportError):
        comp_volume = property(
            fget=lambda x: raise_(
                ImportError("Can't use Magnet method comp_volume: " + str(comp_volume))
            )
        )
    else:
        comp_volume = comp_volume
    # cf Methods.Machine.Magnet.is_outwards
    if isinstance(is_outwards, ImportError):
        is_outwards = property(
            fget=lambda x: raise_(
                ImportError("Can't use Magnet method is_outwards: " + str(is_outwards))
            )
        )
    else:
        is_outwards = is_outwards
    # cf Methods.Machine.Magnet.plot
    if isinstance(plot, ImportError):
        plot = property(
            fget=lambda x: raise_(
                ImportError("Can't use Magnet method plot: " + str(plot))
            )
        )
    else:
        plot = plot
    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self,
        mat_type=-1,
        type_magnetization=0,
        Lmag=0.95,
        init_dict=None,
        init_str=None,
    ):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for pyleecan type, -1 will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with property names as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if init_str is not None:  # Load from a file
            init_dict = load_init_dict(init_str)[1]
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "mat_type" in list(init_dict.keys()):
                mat_type = init_dict["mat_type"]
            if "type_magnetization" in list(init_dict.keys()):
                type_magnetization = init_dict["type_magnetization"]
            if "Lmag" in list(init_dict.keys()):
                Lmag = init_dict["Lmag"]
        # Set the properties (value check and convertion are done in setter)
        self.parent = None
        self.mat_type = mat_type
        self.type_magnetization = type_magnetization
        self.Lmag = Lmag

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        Magnet_str = ""
        if self.parent is None:
            Magnet_str += "parent = None " + linesep
        else:
            Magnet_str += "parent = " + str(type(self.parent)) + " object" + linesep
        if self.mat_type is not None:
            tmp = self.mat_type.__str__().replace(linesep, linesep + "\t").rstrip("\t")
            Magnet_str += "mat_type = " + tmp
        else:
            Magnet_str += "mat_type = None" + linesep + linesep
        Magnet_str += "type_magnetization = " + str(self.type_magnetization) + linesep
        Magnet_str += "Lmag = " + str(self.Lmag) + linesep
        return Magnet_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.mat_type != self.mat_type:
            return False
        if other.type_magnetization != self.type_magnetization:
            return False
        if other.Lmag != self.Lmag:
            return False
        return True

    def as_dict(self):
        """Convert this object in a json seriable dict (can be use in __init__)"""

        Magnet_dict = dict()
        if self.mat_type is None:
            Magnet_dict["mat_type"] = None
        else:
            Magnet_dict["mat_type"] = self.mat_type.as_dict()
        Magnet_dict["type_magnetization"] = self.type_magnetization
        Magnet_dict["Lmag"] = self.Lmag
        # The class name is added to the dict for deserialisation purpose
        Magnet_dict["__class__"] = "Magnet"
        return Magnet_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        if self.mat_type is not None:
            self.mat_type._set_None()
        self.type_magnetization = None
        self.Lmag = None

    def _get_mat_type(self):
        """getter of mat_type"""
        return self._mat_type

    def _set_mat_type(self, value):
        """setter of mat_type"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "pyleecan.Classes", value.get("__class__"), "mat_type"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = Material()
        check_var("mat_type", value, "Material")
        self._mat_type = value

        if self._mat_type is not None:
            self._mat_type.parent = self

    mat_type = property(
        fget=_get_mat_type,
        fset=_set_mat_type,
        doc=u"""The Magnet material

        :Type: Material
        """,
    )

    def _get_type_magnetization(self):
        """getter of type_magnetization"""
        return self._type_magnetization

    def _set_type_magnetization(self, value):
        """setter of type_magnetization"""
        check_var("type_magnetization", value, "int", Vmin=0, Vmax=5)
        self._type_magnetization = value

    type_magnetization = property(
        fget=_get_type_magnetization,
        fset=_set_type_magnetization,
        doc=u"""Permanent magnet magnetization type: 0 for radial, 1 for parallel, 2 for Hallbach

        :Type: int
        :min: 0
        :max: 5
        """,
    )

    def _get_Lmag(self):
        """getter of Lmag"""
        return self._Lmag

    def _set_Lmag(self, value):
        """setter of Lmag"""
        check_var("Lmag", value, "float", Vmin=0)
        self._Lmag = value

    Lmag = property(
        fget=_get_Lmag,
        fset=_set_Lmag,
        doc=u"""Magnet axial length

        :Type: float
        :min: 0
        """,
    )
