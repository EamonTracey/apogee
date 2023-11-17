import csv
import time

import kalman
import sensors

OUTPUT_PATH = "/home/acs/data/subscale/subscale_0.csv"

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
    "Temperature IMU",
]

writer = csv.writer(open(OUTPUT_PATH, "w"))
writer.writerow(HEADERS)



count = 0
start = time.time()
for _ in range(200):
    count += 1
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
    temperature_imu = sensors.IMU.temperature()

    # TODO: Compute state.
    state = 0

    print([
        current,
        state,
        temperature_alt,
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
        temperature_imu,
    ])

print(f"sample rate: {count / (time.time() - start)}")
