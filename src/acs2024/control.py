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
APOGEE_ALTITUDE = 5000              # feet
APOGEE_VELOCITY = 0                 # feet

# Launch vehicle constants.
VEHICLE_MASS = 1.154                # slugs

# Weather constants.
GROUND_TEMPERATURE = 50             # fahrenheit
GROUND_PRESSURE = 2127              # pounds / foot^2

# Luke constants.
LUKE_APOGEE = 5723                  # feet


class State(Enum):
    """
    The State class enumerates the launch vehicle's possible states.
    """

    GROUND = 0
    LAUNCHED = 1
    BURNOUT = 2
    OVERSHOOT = 3
    APOGEE = 4


def determine_state(state, altitude, velocity, acceleration):
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

    def calculate_actuation(self, time_, state, flap_angle, altitude, velocity):
        # Returns the value to pass to servo.rotate.

        if state == State.GROUND or state == State.LAUNCHED:
            return None
        if state == State.OVERSHOOT:
            return 40
        if state == State.APOGEE:
            return 0

        if self._first:
            apogee_prediction = predict_apogee(flap_angle, altitude, velocity)
            self.apogee_prediction = apogee_prediction

            self.error_previous = apogee_prediction - APOGEE_ALTITUDE
            self.time_previous = time_
            self.integral_previous = 0
            self.pi_previous = 0

            self._first = False
            return None

        # Predict apogee.
        apogee_prediction = predict_apogee(flap_angle, altitude, velocity)
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
        Kg = 0.0125

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


def predict_apogee(flap_angle, altitude, velocity):
    # Use 0.5 second timestep.
    dt = 1 / 2

    # The apogee prediction and current velocity
    # are updated in each timestep.
    apogee_prediction = altitude
    velocity_current = velocity

    # Fp calculates the acceleration at each timestep.
    Fp = lambda a, v: -G - calculate_drag(flap_angle, a, v) / VEHICLE_MASS

    # RK4 magic.
    while velocity_current > 0:
        kx1 = velocity_current
        kp1 = Fp(apogee_prediction, velocity_current)

        kx2 = velocity_current + 0.5 * kp1 * dt
        kp2 = Fp(apogee_prediction + 0.5 * kx1 * dt, velocity_current + 0.5 * kp1 * dt)

        kx3 = velocity_current + 0.5 * kp2 * dt
        kp3 = Fp(apogee_prediction + 0.5 * kx2 * dt, velocity_current + 0.5 * kp2 * dt)

        kx4 = velocity_current + kp3 * dt
        kp4 = Fp(apogee_prediction + kx3 * dt, velocity_current + kp3 * dt)

        apogee_prediction += (1 / 6) * (kx1 + 2 * kx2 + 2 * kx3 + kx4) * dt
        velocity_current += (1 / 6) * (kp1 + 2 * kp2 + 2 * kp3 + kp4) * dt

    return apogee_prediction

def calculate_drag(flap_angle, altitude, velocity):
    # This is a rough calculation of mach number given velocity.
    pressure = atmosphere_pressure(altitude)
    density = atmosphere_density(altitude)
    mach_number = velocity / math.sqrt(1.4 * pressure / density)

    # This equation is based on interpolated CFD results.
    # Output is pound-force.
    drag = 0.224809 * (
        -2.5641
        - 1.125 * flap_angle
        + 42.1162 * mach_number
        + 0.1118 * flap_angle**2
        - 12.5214 * flap_angle * mach_number
        + 305.9836 * mach_number**2
        - 0.0021 * flap_angle**3
        + 0.3263 * flap_angle**2 * mach_number
        + 31.0821 * flap_angle * mach_number**2
        + 5.1398 * mach_number**3
    )

    # Drag is proportional to air density.
    drag *= atmosphere_density(altitude) / 0.0025845

    # If our interpolation is below 0, return 0.
    if drag <= 0:
        return 0

    return drag

def servo_percentage_to_flap_angle(servo_percentage):
    # Assume servo percentage = flap angle.
    return servo_percentage

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
