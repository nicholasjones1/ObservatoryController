from enum import Enum


class Mount(Enum):
    PARKED = 1
    UNPARKED = 2
    TRACKING = 3
    SLEWING = 4
    UNKNOWN = 5
