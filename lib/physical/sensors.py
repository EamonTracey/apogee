import time

import adafruit_bmp3xx
import adafruit_bno055

class _BMP390:
    def __init__(self, i2c):
        self.altimeter = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        self.altimeter.pressure_oversampling = 1
    
    def temperature(self):
        return celsius_to_fahrenheit(self.altimeter.temperature)
    
    def altitude(self):
        return meters_to_feet(self.altimeter.altitude)

    def zero(self, n=100, wait=0.01):
        pressure_sum = 0
        for _ in range(n):
            pressure_sum += self.pressure()
            time.sleep(wait)
        self.altimeter.sea_level_pressure = pressure_sum / n

    def reset(self):
        self.altimeter.reset()


class _BNO055:
    def __init__(self, i2c) -> None:
        self.imu = adafruit_bno055.BNO055_I2C(i2c)

        # Configure the BNO055 to operate in 16g mode.
        # Unfortunately, a typo in the datasheet implied that
        # 16g mode is compatible with fusion (orientation) modes;
        # however, that is not true. We prioritize correct
        # acceleration values over Euler angles.
        self.imu.mode = adafruit_bno055.CONFIG_MODE
        self.imu.accel_range = adafruit_bno055.ACCEL_16G
        self.imu.mode = adafruit_bno055.AMG_MODE

    def acceleration(self):
        return tuple(map(meters_to_feet, self.imu.acceleration))

    def gyro(self):
        return tuple(map(meters_to_feet, self.imu.gyro))
        
    def magnetic(self):
        return tuple(map(meters_to_feet, self.imu.magnetic))

    def euler(self):
        return self.imu.euler


def meters_to_feet(n):
    return n * 3.28084

def celsius_to_fahrenheit(n):
    return n * 1.8 + 32

def newtons_to_pounds(n):
    return n * 0.224809
