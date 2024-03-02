"""
state.py contains the implementation of State.
"""

from enum import Enum
import math

from constants import *

class State(Enum):
    """
    The State class enumerates the launch vehicle's possible states.
    """

    GROUND = 0
    LAUNCHED = 1
    BURNOUT = 2
    OVERSHOOT = 3
    APOGEE = 4

def determine_state(state, altitude, acceleration, velocity):
        # Ground -> Launched.
        if (state == State.GROUND and altitude > LAUNCH_ALTITUDE and acceleration > LAUNCH_ACCELERATION) or altitude > 200:
            return State.LAUNCHED
        # Launched -> Burnout.
        elif (state == State.LAUNCHED and altitude < APOGEE_ALTITUDE and acceleration < BURNOUT_ACCELERATION) or altitude > BURNOUT_ALTITUDE:
            return State.BURNOUT
        # Burnout -> Overshoot.
        elif (state == State.BURNOUT and altitude > APOGEE_ALTITUDE and acceleration < BURNOUT_ACCELERATION):
            return State.OVERSHOOT
        # Burnout -> Apogee.
        elif (state == State.BURNOUT and altitude < APOGEE_ALTITUDE and velocity < APOGEE_VELOCITY):
            return State.APOGEE
        # Overshoot -> Apogee.
        elif (state == State.OVERSHOOT and altitude > APOGEE_ALTITUDE and velocity < APOGEE_VELOCITY):
            return State.APOGEE
        else:
            return state

