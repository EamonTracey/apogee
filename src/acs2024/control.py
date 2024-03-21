from enum import Enum
import math
import time

# Physical constants.
G = 32.17405                        # feet / second^2

# State determination constants.
LAUNCH_ALTITUDE = 100               # feet
LAUNCH_ACCELERATION = 200           # feet / second^2
LAUNCH_ALTITUDE_CRITICAL = 300      # feet / second^2
BURNOUT_ALTITUDE = 1200             # feet
BURNOUT_ACCELERATION = 0            # feet / second^2
BURNOUT_ALTITUDE_CRITICAL = 1700    # feet
APOGEE_ALTITUDE = 5200              # feet
APOGEE_VELOCITY = 0                 # feet

# Launch vehicle constants.
VEHICLE_MASS = 1.2232296            # slugs

class ActuationController:
    def __init__(self):
        self.error_previous = 0
        self.time_previous = 0
        self.integral_previous = 0
        self.pi_previous = 0

        # Track the first time the actuate method is called during burnout.
        self._first = True

        # We want to log this.
        self.apogee_prediction = 5800

    def calculate_actuation(self, state, altitude, acceleration, velocity, time_, flap_angle):
        # Returns the value to pass to servo.rotate.

        if state == State.GROUND or state == State.LAUNCHED:
            return None
        if state == State.OVERSHOOT:
            return 40
        if state == State.APOGEE:
            return 0

        if self._first:
            drag = calculate_drag(flap_angle, velocity)
            apogee_prediction = predict_apogee(altitude, acceleration, velocity, drag)
            self.apogee_prediction = apogee_prediction

            self.error_previous = apogee_prediction - 5200
            self.time_previous = time_
            self.integral_previous = 0
            self.pi_previous = 0

            self._first = False
            return None

        # Predict apogee.
        drag = calculate_drag(flap_angle, velocity)
        apogee_prediction = predict_apogee(altitude, acceleration, velocity, drag)
        self.apogee_prediction = apogee_prediction

        # Calculate error and store timestep.
        apogee_error = apogee_prediction - 5200

        # Calculate the time delta.
        dt = time_ - self.time_previous

        # Calculate the PI terms.
        proportional = apogee_error
        integral = self.integral_previous + ((apogee_error + self.error_previous) * dt / 2)

        Kp = 50
        Ki = 8
        Kg = 0.01

        # Perform PI control!
        pi = dt * (Kp * proportional + Ki * integral) * Kg + self.pi_previous

        # Contain the PI algorithm output within the bounds of actuation.
        if pi <= 0:
            pi = 0
        elif pi >= 40:
            pi = 40

        # Store relevant previous values.
        self.error_previous = apogee_error
        self.time_previous = time_
        self.integral_previous = integral
        self.pi_previous = pi

        return pi

def determine_state(state, altitude, acceleration, velocity):
        # Ground -> Launched.
        if state == State.GROUND:
            if (altitude > LAUNCH_ALTITUDE and acceleration > LAUNCH_ACCELERATION) or altitude > LAUNCH_ALTITUDE_CRITICAL:
                return State.LAUNCHED
            else:
                return state
        # Launched -> Burnout.
        elif state == State.LAUNCHED:
            if (BURNOUT_ALTITUDE < altitude < APOGEE_ALTITUDE and acceleration < BURNOUT_ACCELERATION) or altitude > BURNOUT_ALTITUDE_CRITICAL:
                return State.BURNOUT
            else:
                return state
        # Burnout -> Overshoot.
        elif state == State.BURNOUT:
            if altitude > APOGEE_ALTITUDE:
                return State.OVERSHOOT
            else:
                return state
        # Burnout -> Apogee.
        elif state == State.BURNOUT:
            if velocity < APOGEE_VELOCITY:
                return State.APOGEE
            else:
                return state
        # Overshoot -> Apogee.
        elif state == State.OVERSHOOT:
            if velocity < APOGEE_VELOCITY:
                return State.APOGEE
            else:
                return state
        # Apogee -> Apogee.
        elif state == State.APOGEE:
            return state
        else:
            return state


class State(Enum):
    """
    The State class enumerates the launch vehicle's possible states.
    """

    GROUND = 0
    LAUNCHED = 1
    BURNOUT = 2
    OVERSHOOT = 3
    APOGEE = 4


def calculate_drag(flap_angle, velocity):
    # This is a rough calculation of mach number given velocity.
    # Improvement: calculate based on temperature.
    mach_number = velocity / 1125 

    # This equation is based on interpolated CFD results.
    # Output is pound-force.
    drag = 0.224809 * (
        -20.74
        + 4.351 * flap_angle
        + 131.1 * mach_number
        - 0.1112 * flap_angle**2
        - 19.77 * flap_angle * mach_number
        + 146 * mach_number**2
        + 0.5031 * flap_angle**2 * mach_number
        + 31.64 * flap_angle * mach_number ** 2
        + 117.8 * mach_number ** 3
    )

    return drag

def predict_apogee(altitude, acceleration, velocity, drag):
    if drag <= 0:
        return altitude + (velocity ** 2) / (2 * G)

    radicand = VEHICLE_MASS * G / drag
    velocity_terminal = velocity * math.sqrt(radicand)

    apogee_delta = velocity_terminal ** 2 * math.log(1 + velocity ** 2 / velocity_terminal ** 2) / (2 * G)
    apogee_prediction = altitude + apogee_delta

    return apogee_prediction
