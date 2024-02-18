from time import sleep

import board
import pwmio

motor = pwmio.PWMOut(board.D12, variable_frequency=False)
motor.frequency = 330

def rotate_servo(n):
    ON = 2 ** 16
    MOTOR_MIN = 0.15
    MOTOR_MAX = 0.80

    if type(n) is not int:
        exit("type mismatch")
    if n < 0 or n > 100:
        exit("n problem")

    delta = MOTOR_MAX - MOTOR_MIN
    duty = MOTOR_MIN + delta * n / 100

    if duty < MOTOR_MIN or duty > MOTOR_MAX:
        exit("duty math")
    print(duty)
    motor.duty_cycle = duty * ON

rotate_servo(0)
sleep(1)
rotate_servo(35)
sleep(1)
#rotate_servo(0)

#rotate_servo(15)
#rotate_servo(20)
#rotate_servo(25)
#rotate_servo(30)
#rotate_servo(35)