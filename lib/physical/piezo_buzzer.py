import time

import board
import pwmio


class PiezoBuzzer:
    def __init__(self, pin, **kwargs):
        self.buzzer = pwmio.PWMOut(pin, **kwargs)

    def beep(self, s, frequency=500, duty_cycle=2 ** 15):
        self.buzzer.frequency = frequency
        self.buzzer.duty_cycle = duty_cycle
        time.sleep(s)
        self.buzzer.duty_cycle = 0


BUZZER = PiezoBuzzer(board.D13)
