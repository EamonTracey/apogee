"""
state.py contains the implementation of State.
"""

from enum import Enum
import ~/code/src/sensors.py

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

def state:
    acc = feet(sensors.acceleration())
    alt = 
