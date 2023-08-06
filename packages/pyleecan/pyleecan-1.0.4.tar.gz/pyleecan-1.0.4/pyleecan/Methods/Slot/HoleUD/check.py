from ....Methods.Slot.Slot.check import SlotCheckError


def check(self):
    """Check that the HoleUD is correctly defined"""

    if len(self.surf_list) == 0:
        raise SlotCheckError("HoleUD must have at least one surface")
    for key in self.magnet_dict:
        if key[:7] != "magnet_":
            raise SlotCheckError(
                "HoleUD magnet_dict must use key like 'magnet_X' with X the index of the magnet. Found: "
                + key
            )
