import time

# Assume servo actuation percentage = flap angle.
class ActuationController:
    def __init__(self, servo):
        self.servo = servo

        self.errors = []
        self.times = []
        self.integrals = []

        SERVO.rotate(0)
        time.sleep(2)
        SERVO.rotate(30)
        time.sleep(2)
        SERVO.rotate(0)

    def calculate_drag(self, velocity):
        # Assume flap angle equals servo actuation percentage.
        # This is not perfectly accurate but a decent approximation.
        flap_angle = self.servo.percentage

        # This is a rough calculation of mach number given velocity.
        # Improvement: calculate based on temperature.
        mach_number = velocity / 1125 

        # This equation is based on interpolated CFD results.
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
        
    def predict_apogee(altitude, acceleration, velocity, drag):
        ...

    def actuate(self, state, altitude, acceleration, velocity, time_):
        if state == State.GROUND or state == State.LAUNCHED:
            return
        if state == State.OVERSHOOT:
            SERVO.rotate(35)
            return
        if state == State.APOGEE:
            SERVO.rotate(0)
            return
        
        # Predict apogee.
        drag = self.calculate_drag(velocity)
        apogee_prediction = self.predict_apogee(altitude, acceleration, velocity, drag)

        # Calculate error and store timestep.
        apogee_error = apogee_prediction - 5200
        self.errors.append(apogee_error)
        times.append(time_)
        if len(self.errors) < 2:
            self.integrals.append(0)
            self.us.append(drag)
            return

        dt = times[-1] - times[-2]
        proportional = self.errors[-1]
        integral = integrals[-1] + ((errors[-1] + errors[-2]) * dt / 2) ; self.integrals.append(integral)
        derivative = (self.errors[-1] - self.errors[-2]) / dt

        Kp = 3
        Ki = 2
        Kd = 0.001
        Kg = 1

        u = dt * (Kp * proportional + Ki * integral + Kd * derivative) * Kg + self.us[-1] ; self.us.append(u)
