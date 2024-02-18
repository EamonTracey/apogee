"""
state.py contains the implementation of State.
"""

from enum import Enum
import ~/code/src/sensors.py
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



def hPa_to_altitude(pressure_hPa):
    # Constants
    T0 = 288.15  # Standard temperature at sea level (K)
    L = 0.0065   # Temperature lapse rate (K/m)
    P0 = 101325  # Standard atmospheric pressure at sea level (Pa)
    R = 287.05   # Specific gas constant for dry air (J/(kg·K))
    g = 9.81     # Acceleration due to gravity (m/s²)

    # Convert pressure from hPa to Pa
    pressure_Pa = pressure_hPa * 100

    # Calculate altitude using the barometric formula
    altitude = (T0 / L) * (1 - (pressure_Pa / P0)**(R * L / g))

    return altitude

def state(pressure, acc, vel):
    alt = hPa_to_altitude(pressure)
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