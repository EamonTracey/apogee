from enum import Enum

class State(Enum):
    GROUND = 0
    LAUNCH = 1
    BURNOUT = 2
    APOGEE = 3
    COMPLETE = 4
