#!/usr/bin/python3

import csv
from datetime import datetime
import time

from actuation_controller import ActuationController
from constants import HEADERS, OUTPUT_DIR
from piezo_buzzer import BUZZER
from kalman import DataFilter
from sensors import ALTIMETER, IMU
from servo_motor import SERVO
from state import State, determine_state
from units import meters_to_feet
import sys

# Initialize data logging constants.
now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
OUTPUT_PATH = f"{~/data/testDataOUT}/test-{now}.csv"

# Create csv writer (logger).
writer = csv.writer(open(~/acs/data/testDataOUT, "w+"))
writer.writerow(HEADERS)

# Make the data filter.
data_filter = DataFilter()
for _ in range(100):
    data_filter.filter_data(0, 0)
    time.sleep(0.05)

print(f'{sys.argv[0]} and {sys.argv[1]}')

state = State.GROUND

if len(sys.argv) == 2:
    #READING FILES AND TESTING WITH TEST DATA
    try:
        with open(sys.argv[1], 'r') as file:
            for row in csv.DictReader(file):
                try:
                    # Read current time.
                    current = row['Time']
                    
                    # Reading BMP390 sensor.
                    altitude = meters_to_feet(float(row['Altitude']))
                    #temperature = row[-1] not in sheet

                    # Read BNO055 sensor.
                    #acceleration_x = meters_to_feet(float(row["ADXL_Acceleration_X"]))
                    acceleration_y = meters_to_feet(float(row["Acceleration Y"]))
                    #acceleration_z = meters_to_feet(float(row["ADXL_Acceleration_Y"]))
                    
                    #euler_angle = row[5] we dont have flat euler angle
                    # euler_angle_0 = row["Euler_Angle_X"]
                    # euler_angle_1 = row["Euler_Angle_Z"]
                    # euler_angle_2 = row["Euler_Angle_Y"]

                    # Filter the data.
                    data_filter.filter_data(altitude, acceleration_y)
                    altitude_filtered = data_filter.kalman_altitude
                    acceleration_filtered = data_filter.kalman_acceleration
                    velocity_filtered = data_filter.kalman_velocity

                    # Determine the state of the ACS.
                    state = determine_state(state, altitude_filtered, acceleration_filtered, velocity_filtered)

                    # Run actuation control algorithm.
                    actuator.actuate(state, altitude_filtered, acceleration_filtered, velocity_filtered)

                    # Log the data
                    writer.writerow([
                        current,
                        state,
                        altitude_filtered,
                        acceleration_filtered,
                        velocity_filtered,
                        altitude,
                        #acceleration_x,
                        acceleration_y,
                        # acceleration_z,
                        # euler_angle_0,
                        # euler_angle_1,
                        # euler_angle_2,
                        #temperature
                    ])
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
else:
    print('improper usage')


