import time

import adafruit_bmp3xx
import adafruit_bno055
import board

from utilsi import celsius_to_fahrenheit, meters_to_feet

I2C = board.I2C()

def sensor_reading(func):
    # @wraps(func)
    # def wrapper(self, *args, **kwargs):
    #     reading = func(self, *args, **kwargs)
    #     self.readings[func.__name__].append((time.time(), reading))
    #     return reading
    # return wrapper
    return func
        

class _BMP390:
    def __init__(self):
        self.altimeter = adafruit_bmp3xx.BMP3XX_I2C(I2C)
        self.altimeter.pressure_oversampling = 1

    @sensor_reading
    def temperature(self):
        return fahrenheit_to_celsius(self.altimeter.temperature)

    @sensor_reading
    def pressure(self):
        return self.altimeter.pressure

    @sensor_reading
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
    def __init__(self) -> None:
        self.imu = adafruit_bno055.BNO055_I2C(I2C)
        self.imu.accel_range = adafruit_bno055.ACCEL_16G

    @sensor_reading
    def acceleration(self):
        return meters_to_feet(self.imu.acceleration)

    @sensor_reading
    def gravity(self):
        return meters_to_feet(self.imu.gravity)

    @sensor_reading
    def gyro(self):
        return meters_to_feet(self.imu.gyro)
        
    @sensor_reading
    def magnetic(self):
        return meters_to_feet(self.imu.magnetic)

    @sensor_reading
    def euler(self):
        return self.imu.euler

    @sensor_reading
    def quaternion(self):
        return self.imu.quaternion

    @sensor_reading
    def linear_acceleration(self):
        return meters_to_feet(self.imu.linear_acceleration)

    @sensor_reading
    def temperature(self):
        return fahrenheit_to_celsius(self.imu.temperature)


ALTIMETER = _BMP390()
IMU = _BNO055()
