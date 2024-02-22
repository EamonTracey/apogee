from time import sleep

import board
import pwmio


class ServoMotor:
    ON = 2 ** 16
    MOTOR_MIN = 0.15
    MOTOR_MAX = 0.80

    def __init__(self, pin, **kwargs):
        self.motor = pwmio.PWMOut(pin, variable_frequency=False, **kwargs)
        self.motor.frequency = 330

    def rotate(self, n):
        """
        Rotate the servo motor by the percentage indicates by n.
            n = 0 -> 0% = 0 degrees
            n = 50 -> 50% = 90 degrees
            n = 100 -> 100% = 180 degrees
        The servo motor 
        """
        if type(n) is not int:
            exit("SERVO ERROR: must pass an integer.")
        if n < 0 or n > 100:
            exit(f"SERVO ERROR: the percentage value ({n}) must be in [0, 100]")
        if n < 0 or n > 40:
            exit(f"SERVO ERROR: unsafe actuation percentage ({n}), stay in [0, 40]")

        delta = ServoMotor.MOTOR_MAX - ServoMotor.MOTOR_MIN
        duty = ServoMotor.MOTOR_MIN + delta * n / 100
        self.motor.duty_cycle = duty * ServoMotor.ON


SERVO = ServoMotor(board.D12)
while 1:
    n = input("Enter percentage to turn servo: ")
    if (n == "q"):
        SERVO.rotate(0)
        print(f"Rotating servo to {n}% = ({n / 100 * 180} degrees)")
        sleep(1)
        break
    n = int(n)
    print("Zeroing servo...")
    SERVO.rotate(0)
    sleep(2)
    print(f"Rotating servo to {n}% = ({n / 100 * 180} degrees)")
    SERVO.rotate(n)
    sleep(2)
# print("Zeroing servo...")
# SERVO.rotate(0)
