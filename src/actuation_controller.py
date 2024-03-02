from constants import G, VEHICLE_MASS
import math
import time

# Assume servo actuation percentage = flap angle.
class ActuationController:
    def __init__(self, servo):
        self.servo = servo

        self.error_previous = 0
        self.time_previous = 0
        self.integral_previous = 0
        self.pid_previous = 0

        # Track the first time the actuate method is called during burnout.
        self._first = True

        self.servo.rotate(0)
        time.sleep(2)
        self.servo.rotate(30)
        time.sleep(2)
        self.servo.rotate(0)

    def calculate_drag(self, velocity):
        # Assume flap angle equals servo actuation percentage.
        # This is not perfectly accurate but a decent approximation.
        flap_angle = self.servo.percentage

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
            return None
        velocity_terminal = velocity * math.sqrt(radicand)

        apogee_delta = velocity_terminal ** 2 * math.log(1 + velocity ** 2 / velocity_terminal ** 2) / (2 * G)
        apogee_prediction = altitude + apogee_delta

        return apogee_prediction

    def actuate(self, state, altitude, acceleration, velocity, time_):
        if state == State.GROUND or state == State.LAUNCHED:
            return
        if state == State.OVERSHOOT:
            self.servo.rotate(40)
            return
        if state == State.APOGEE:
            self.servo.rotate(0)
            return

        if self._first:
            drag = self.calculate_drag(velocity)
            apogee_prediction = self.predict_apogee(altitude, acceleration, velocity, drag)

            self.error_previous = apogee_prediction - 5200
            self.time_previous = time_
            self.integral_previous = 0
            self.pid_previous = 0

            self._first = False
            return

        # Predict apogee.
        drag = self.calculate_drag(velocity)
        apogee_prediction = self.predict_apogee(altitude, acceleration, velocity, drag)
        apogee_error = apogee_prediction - 5200

        # Calculate error and store timestep.
        apogee_error = apogee_prediction - 5200

        # Calculate the time delta.
        dt = time_ - time_previous

        # Calculate the PID terms.
        proportional = apogee_prediction
        integral = integral_previous + ((apogee_error + error_previous) * dt / 2)
        derivative = (apogee_error - error_previous) / dt

        Kp = 3
        Ki = 2
        Kd = 0.001
        Kg = 1

        # Perform PID control!
        pid = dt * (Kp * proportional + Ki * integral + Kd * derivative) * Kg + pid_previous
        # self.servo.rotate(0)

        # Store relevant previous values.
        error_previous = apogee_error
        time_previous = time_
        integral_previous = integral
        pid_previous = pid
