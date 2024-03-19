from constants import G, VEHICLE_MASS
import math
import time

from state import State

def calculate_drag(self, flap_angle, velocity):
    # This is a rough calculation of mach number given velocity.
    # Improvement: calculate based on temperature.
    mach_number = velocity / 1125 

    # This equation is based on interpolated CFD results.
    # Output is newtons.
    return (
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

def predict_apogee(self, altitude, acceleration, velocity, drag):
    radicand = VEHICLE_MASS * G / drag
    if radicand < 0:
        return 5769
    velocity_terminal = velocity * math.sqrt(radicand)

    apogee_delta = velocity_terminal ** 2 * math.log(1 + velocity ** 2 / velocity_terminal ** 2) / (2 * G)
    apogee_prediction = altitude + apogee_delta

    return apogee_prediction

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

    def determine_actuation(self, state, altitude, acceleration, velocity, time_):
        # Returns the value to pass to servo.rotate.

        if state == State.GROUND or state == State.LAUNCHED:
            return None
        if state == State.OVERSHOOT:
            return 40
        if state == State.APOGEE:
            return 0

        if self._first:
            drag = self.calculate_drag(velocity)
            apogee_prediction = self.predict_apogee(altitude, acceleration, velocity, drag)
            self.apogee_prediction = apogee_prediction

            self.error_previous = apogee_prediction - 5200
            self.time_previous = time_
            self.integral_previous = 0
            self.pi_previous = 0

            self._first = False
            return None

        # Predict apogee.
        drag = self.calculate_drag(velocity)
        apogee_prediction = self.predict_apogee(altitude, acceleration, velocity, drag)
        self.apogee_prediction = apogee_prediction

        # Calculate error and store timestep.
        apogee_error = apogee_prediction - 5200

        # Calculate the time delta.
        dt = time_ - self.time_previous

        # Calculate the PI terms.
        proportional = apogee_error
        integral = self.integral_previous + ((apogee_error + self.error_previous) * dt / 2)

        Kp = 12.5
        Ki = 1
        Kg = 0.01

        # Perform PI control!
        pi = dt * (Kp * proportional + Ki * integral) * Kg + self.pi_previous

        # Store relevant previous values.
        self.error_previous = apogee_error
        self.time_previous = time_
        self.integral_previous = integral
        self.pi_previous = pi

        return pi
