from time import sleep
from ~/code/tests/servo_test.py import rotate_servo()
import board
import pwmio

motor = pwmio.PWMOut(board.D12, variable_frequency=False)

motor.freqency = 330




