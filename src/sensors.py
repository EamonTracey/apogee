from functools import wraps
import time

import adafruit_bmp3xx
import board

I2C = board.I2C()

def sensor_reading(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        reading = func(self, *args, **kwargs)
        self.readings[func.__name__].append((time.time(), reading))
        return reading
    return wrapper
        

class _BMP390:
    def __init__(self):
        self.altimeter = adafruit_bmp3xx.BMP3XX_I2C(I2C)
        self.altimeter.pressure_oversampling = 4

        # Conform to expectations of sensor_reading decorator.
        self.readings = {"temperature": [], "pressure": [], "altitude": []}

    @sensor_reading
    def temperature(self):
        return self.altimeter.temperature

    @sensor_reading
    def pressure(self):
        return self.altimeter.pressure

    @sensor_reading
    def altitude(self):
        return self.altimeter.altitude

    def zero(self, n=100, wait=0.01):
        pressure_sum = 0
        for _ in range(n):
            pressure_sum += self.pressure()
            time.sleep(wait)
        self.altimeter.sea_level_pressure = pressure_sum / n

    def reset(self):
        self.altimeter.reset()
        

ALTIMETER = _BMP390()
