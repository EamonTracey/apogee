import csv
import time

import sensors

OUTPUT_PATH = "/home/acs/data/subscale"

HEADERS = [
    "Time",
    "State",
    "Temperature ALT",
    "Pressure",
    "Altitude",
    "Acceleration X",
    "Acceleration Y",
    "Acceleration Z",
    "Gravity X",
    "Gravity Y",
    "Gravity Z",
    "Gyro X",
    "Gyro Y",
    "Gyro Z",
    "Magnetic X",
    "Magnetic Y",
    "Magnetic Z",
    "Euler X",
    "Euler Y",
    "Euler Z",
    "Quaternion X",
    "Quaternion Y",
    "Quaternion Z",
    "Quaternion W",
    "Linear Acceleration X",
    "Linear Acceleration Y",
    "Linear Acceleration Z",
    "Temperature IMU"
]

start = time.time()

while True:
    # Read current time.
    current = time.time() - start

    # Read BMP390 sensor.
    temperature_alt = sensors.ALTIMETER.temperature()
    pressure = sensors.ALTIMETER.pressure()
    altitude = sensors.ALTIMETER.altitude()

   # Read BNO055 sensor.
   acceleration = sensors.IMU.acceleration()
   acceleration_x = acceleration[0]
   acceleration_y = acceleration[1]
   acceleration_z = acceleration[2]
   gravity = sensors.IMU.gravity()
   gravity_x = gravity[0]
   gravity_y = gravity[1]
   gravity_z = gravity[2]
   gyro = sensors.IMU.gyro()
   gyro_x = gyro[0]
   gyro_y = gyro[1]
   gyro_z = gyro[2]
   magnetic = sensors.IMU.magnetic()
   magnetic_x = magnetic[0]
   magnetic_y = magnetic[1]
   magnetic_z = magnetic[2]



