"""
state.py contains the implementation of State.
"""

from enum import Enum
import math

from utils import meters_to_feet

class State(Enum):
    """
    The State class enumerates the launch vehicle's possible states.
    """

    GROUND = 0
    LAUNCHED = 1
    BURNOUT = 2
    OVERSHOOT = 3
    APOGEE = 4

def state_determination(altitude, acceleration, velocity):
    altitude = meters_to_feet(altitude)
    acceleration = meters_to_feet(acceleration)
    velocity = meters_to_feet(velocity)
    if acceleration < 200 and altitude < 150:
        return State.GROUND
    elif acceleration > 200 and altitude > 150:
        return State.LAUNCHED
    elif acceleration < -20 and altitude < 5200:
        return State.BURNOUT
    #elif velocity > 0 and altitude > 5200:
        #return  State.OVERSHOOT
    #elif velocity < 0
        #return State.APOGEE
