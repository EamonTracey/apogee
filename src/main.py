#!/usr/bin/python3

import csv
from datetime import datetime
import time

time.sleep(3)

#import kalman
import sensors
from state import State

now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
OUTPUT_DIR = "/home/acs/data/subscale"
OUTPUT_PATH = f"{OUTPUT_DIR}/ACTUAL_SUBSCALE_2_data_{now}.csv"

HEADERS = [
    "Time",
    "State",
#    "Temperature BMP",
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
    "Temperature BNO"
]

writer = csv.writer(open(OUTPUT_PATH, "w"))
writer.writerow(HEADERS)

#try:
#    sensors.ALTIMETER.zero()
#except Exception as e:
#    print(f"{e}: failed to zero BMP390.")

#state = State.GROUND

start = time.time()
while True:
    try:
        # Read current time.
        current = time.time() - start

#        # Read BMP390 sensor.
#        temperature_bmp = sensors.ALTIMETER.temperature()
        # Read MPRLS sensor.
        try:
            pressure = sensors.ALTIMETER.pressure()
        except Exception as e:
            pressure = "FAIL"
            print(e)

        altitude = sensors.AlTIMETER.pressure()
        state = state(altitude, acceleration_y)
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
        euler = sensors.IMU.euler()
        euler_x = euler[0]
        euler_y = euler[1]
        euler_z = euler[2]
        quaternion = sensors.IMU.quaternion()
        quaternion_x = quaternion[0]
        quaternion_y = quaternion[1]
        quaternion_z = quaternion[2]
        quaternion_w = quaternion[3]
        linear_acceleration = sensors.IMU.linear_acceleration()
        linear_acceleration_x = linear_acceleration[0]
        linear_acceleration_y = linear_acceleration[1]
        linear_acceleration_z = linear_acceleration[2]
        temperature_bno = sensors.IMU.temperature()
        writer.writerow([
            current,
            state,
#            temperature_bmp,
            pressure,
            altitude,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            gravity_x,
            gravity_y,
            gravity_z,
            gyro_x,
            gyro_y,
            gyro_z,
            magnetic_x,
            magnetic_y,
            magnetic_z,
            euler_x,
            euler_y,
            euler_z,
            quaternion_x,
            quaternion_y,
            quaternion_z,
            quaternion_w,
            linear_acceleration_x,
            linear_acceleration_y,
            linear_acceleration_z,
            temperature_bno
        ])
    except Exception as e:
        print(e)
    if state == 'BURNOUT':
        rotate_servo(20)
        sleep(3)
        rotate_servo(0)
        break


