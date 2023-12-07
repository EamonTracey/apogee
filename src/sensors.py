from functools import wraps
import time

import adafruit_bmp3xx
import adafruit_bno055
import board
import lib.adafruit_mpl3115a2 as adafruit_mpl3115a2

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


class _MPL3115A2:
    def __init__(self):
        self.altimeter = adafruit_mpl3115a2.MPL3115A2(I2C)

        # Conform to expectations of sensor_reading decorator.
        # self.readings = {"temperature": [], "pressure": [], "altitude": []}

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
        self.altimeter.sealevel_pressure = int(pressure_sum / n)


class _BNO055:
    def __init__(self) -> None:
        self.imu = adafruit_bno055.BNO055_I2C(I2C)
        self.imu.accel_range = adafruit_bno055.ACCEL_16G

    @sensor_reading
    def acceleration(self):
        return self.imu.acceleration

    @sensor_reading
    def gravity(self):
        return self.imu.gravity

    @sensor_reading
    def gyro(self):
        return self.imu.gyro
        
    @sensor_reading
    def magnetic(self):
        return self.imu.magnetic

    @sensor_reading
    def euler(self):
        return self.imu.euler

    @sensor_reading
    def quaternion(self):
        return self.imu.quaternion

    @sensor_reading
    def linear_acceleration(self):
        return self.imu.linear_acceleration

    @sensor_reading
    def temperature(self):
        return self.imu.temperature


ALTIMETER = _MPL3115A2() #_BMP390()
#IMU = _BNO055()
