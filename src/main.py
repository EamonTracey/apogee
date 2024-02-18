#!/usr/bin/python3

import csv
from datetime import datetime
import time

from kalman import DataFilter
import sensors
from state import State

# Initialize data logging constants.
now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
OUTPUT_DIR = "/home/acs/data/fullscale"
OUTPUT_PATH = f"{OUTPUT_DIR}/fullscale_data_{now}.csv"
HEADERS = [
    "Time",
    "State",
    "Altitude Filtered",
    "Acceleration Filtered",
    "Velocity Filtered",
    "Altitude",
    "Acceleration X",
    "Acceleration Y",
    "Acceleration Z",
    "Euler Angle 0",
    "Euler Angle 1",
    "Euler Angle 2",
    "Temperature"
]

# Create csv writer (logger).
writer = csv.writer(open(OUTPUT_PATH, "w"))
writer.writerow(HEADERS)

# Make the data filter.
data_filter = DataFilter()
for _ in range(100):
    data_filter.filter_data(0, 0)
    time.sleep(0.05)

# Zero the altimeter.
try:
    sensors.ALTIMETER.zero()
except Exception as e:
    print(f"{e}: failed to zero BMP390.")

# Begin the control loop.
start = time.time()
while True:
    try:
        # Read current time.
        current = time.time() - start

         # Read BMP390 sensor.
        altitude = sensors.ALTIMETER.altitude()
        temperature = sensors.ALTIMETER.temperature()

        # Read BNO055 sensor.
        acceleration = sensors.IMU.linear_acceleration()
        acceleration_x = acceleration[0]
        acceleration_y = acceleration[1]
        acceleration_z = acceleration[2]
        euler_angle = sensors.IMU.euler()
        euler_angle_0 = euler_angle[0]
        euler_angle_1 = euler_angle[1]
        euler_angle_2 = euler_angle[2]

        # Filter the data.
        data_filter.filter_data(altitude, acceleration_z)
        altitude_filtered = data_filter.kalman_altitude
        acceleration_filtered = data_filter.kalman_acceleration
        velocity_filtered = data_filter.kalman_velocity

        # TODO: Update the state of the launch vehicle.
        state = "NA"

        print("acc",acceleration_filtered)
        print("vel",velocity_filtered)

        # Log the data
        writer.writerow([
            current,
            state,
            altitude_filtered,
            acceleration_filtered,
            velocity_filtered,
            altitude,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            euler_angle_0,
            euler_angle_1,
            euler_angle_2,
            temperature
        ])
    except Exception as e:
        print(e)
