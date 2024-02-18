"""
state.py contains the implementation of State.
"""

from enum import Enum
import math

class State(Enum):
    """
    The State class enumerates the launch vehicle's possible states.
    """

    GROUND = 0
    LAUNCHED = 1
    BURNOUT = 2
    OVERSHOOT = 3
    APOGEE = 4

def feet(n):
    return n * 3.28084

def state(, acc, vel):
    alt = feet(alt)
    acc = feet(acc)
    if acc < 200 and alt < 150:
        return State.GROUND
    elif acc > 200 and alt > 150:
        return State.LAUNCHED
    elif acc < -20 and alt < 5200:
        return State.BURNOUT
    #elif vel > 0 and alt > 5200:
        #return  State.OVERSHOOT
    #elif vel < 0
        #return State.APOGEE