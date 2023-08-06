# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Machine/MagnetFlat.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Machine/MagnetFlat
"""

from os import linesep
from logging import getLogger
from ._check import check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Magnet import Magnet

from ._check import InitUnKnowClassError
from .Material import Material


class MagnetFlat(Magnet):
    """abstract class of magnets with rectangular base"""

    VERSION = 1

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
        # Call Magnet init
        super(MagnetFlat, self).__init__(
            mat_type=mat_type, type_magnetization=type_magnetization, Lmag=Lmag
        )
        # The class is frozen (in Magnet init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        MagnetFlat_str = ""
        # Get the properties inherited from Magnet
        MagnetFlat_str += super(MagnetFlat, self).__str__()
        return MagnetFlat_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Magnet
        if not super(MagnetFlat, self).__eq__(other):
            return False
        return True

    def as_dict(self):
        """Convert this object in a json seriable dict (can be use in __init__)"""

        # Get the properties inherited from Magnet
        MagnetFlat_dict = super(MagnetFlat, self).as_dict()
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        MagnetFlat_dict["__class__"] = "MagnetFlat"
        return MagnetFlat_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        # Set to None the properties inherited from Magnet
        super(MagnetFlat, self)._set_None()
