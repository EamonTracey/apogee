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
        if (
            (state == State.GROUND) and
            ((altitude > LAUNCH_ALTITUDE and acceleration > LAUNCH_ACCELERATION) or altitude > LAUNCH_ALTITUDE_CRITICAL)
            ):
            return State.LAUNCHED
        # Launched -> Burnout.
        elif (
            (state == State.LAUNCHED) and 
            ((BURNOUT_ALTITUDE < altitude < APOGEE_ALTITUDE and acceleration < BURNOUT_ACCELERATION) or altitude > BURNOUT_ALTITUDE_CRITICAL)
            ):
            return State.BURNOUT
        # Burnout -> Overshoot.
        elif (
            (state == State.BURNOUT) and
            (altitude > APOGEE_ALTITUDE)
            ):
            return State.OVERSHOOT
        # Burnout -> Apogee.
        elif (
            (state == State.BURNOUT) and
            (velocity < APOGEE_VELOCITY and altitude < APOGEE_ALTITUDE)
            ):
            return State.APOGEE
        # Overshoot -> Apogee.
        elif (
            (state == State.OVERSHOOT) and
            (velocity < APOGEE_VELOCITY and altitude > APOGEE_ALTITUDE)
            ):
            return State.APOGEE
        # No state transition.
        else:
            return state

