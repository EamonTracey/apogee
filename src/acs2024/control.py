from enum import Enum
import math
import time

# Physical constants.
G = 32.17405                        # feet / second^2

# State determination constants.
LAUNCH_ALTITUDE = 100               # feet
LAUNCH_ACCELERATION = 200           # feet / second^2
LAUNCH_ALTITUDE_CRITICAL = 300      # feet / second^2
BURNOUT_ALTITUDE = 800              # feet
BURNOUT_ACCELERATION = 0            # feet / second^2
BURNOUT_ALTITUDE_CRITICAL = 1200    # feet
APOGEE_ALTITUDE = 5200              # feet
APOGEE_VELOCITY = 0                 # feet

# Launch vehicle constants.
VEHICLE_MASS = 1.154                # slugs

# Weather constants.
GROUND_TEMPERATURE = 35             # fahrenheit
GROUND_PRESSURE = 2116              # pounds / foot^2

# Luke constants.
LUKE_APOGEE = 5723                  # feet

class ActuationController:
    def __init__(self):
        self.error_previous = 0
        self.time_previous = 0
        self.integral_previous = 0
        self.pi_previous = 0

        # Track the first time the actuate method is called during burnout.
        self._first = True

        # We want to log this.
        self.apogee_prediction = LUKE_APOGEE

    def calculate_actuation(self, state, altitude, acceleration, velocity, time_, flap_angle):
        # Returns the value to pass to servo.rotate.

        if state == State.GROUND or state == State.LAUNCHED:
            return None
        if state == State.OVERSHOOT:
            return 40
        if state == State.APOGEE:
            return 0

        if self._first:
            drag = calculate_drag(flap_angle, velocity, altitude)
            apogee_prediction = predict_apogee(altitude, acceleration, velocity, drag)
            self.apogee_prediction = apogee_prediction

            self.error_previous = apogee_prediction - APOGEE_ALTITUDE
            self.time_previous = time_
            self.integral_previous = 0
            self.pi_previous = 0

            self._first = False
            return None

        # Predict apogee.
        drag = calculate_drag(flap_angle, velocity, altitude)
        apogee_prediction = predict_apogee(altitude, acceleration, velocity, drag)
        self.apogee_prediction = apogee_prediction

        # Calculate error and store timestep.
        apogee_error = apogee_prediction - APOGEE_ALTITUDE

        # Calculate the time delta.
        dt = time_ - self.time_previous

        # Calculate the PI terms.
        proportional = apogee_error
        integral = self.integral_previous + ((apogee_error + self.error_previous) * dt / 2)

        # These are our proportional constants.
        Kp = 50
        Ki = 8
        Kg = 0.01

        # Servo can deploy at a maximum speed of 35 degrees per 0.33 seconds.
        max_servo_delta = dt * 35 / 0.33

        # Perform PI control!
        pi_delta = dt * (Kp * proportional + Ki * integral) * Kg
        if pi_delta >= max_servo_delta:
            pi_delta = max_servo_delta
        elif pi_delta <= -max_servo_delta:
            pi_delta = -max_servo_delta
        pi = pi_delta + self.pi_previous

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


def calculate_drag(flap_angle, velocity, altitude):
    # This is a rough calculation of mach number given velocity.
    mach_number = velocity / math.sqrt(2403.044 * (atmosphere_temperature(altitude) + 459.67))

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
        + 31.64 * flap_angle * mach_number**2
        + 117.8 * mach_number**3
    )

    # Drag is proportional to air density.
    drag *= atmosphere_density(altitude) / atmosphere_density(0)

    return drag

def predict_apogee(altitude, acceleration, velocity, drag):
    if drag <= 0:
        return altitude + (velocity ** 2) / (2 * G)

    radicand = VEHICLE_MASS * G / drag
    velocity_terminal = velocity * math.sqrt(radicand)

    apogee_delta = velocity_terminal ** 2 * math.log(1 + velocity ** 2 / velocity_terminal ** 2) / (2 * G)
    apogee_prediction = altitude + apogee_delta

    return apogee_prediction

def atmosphere_temperature(altitude):
    # Returns temperature in Fahrenheit.
    return GROUND_TEMPERATURE - 0.00356 * altitude

def atmosphere_pressure(altitude):
    # Returns pressure in pounds / foot^2.
    return GROUND_PRESSURE * ((atmosphere_temperature(altitude) + 459.7) / 518.6)**5.256

def atmosphere_density(altitude):
    # Returns density in slugs / foot^3.
    temperature = atmosphere_temperature(altitude)
    pressure = atmosphere_pressure(altitude)
    return pressure / (1718 * (temperature + 459.7))
