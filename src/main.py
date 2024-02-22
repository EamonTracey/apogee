#!/usr/bin/python3

import csv
from datetime import datetime
import time

from piezo_buzzer import BUZZER
from kalman import DataFilter
from sensors import ALTIMETER, IMU
from servo_motor import SERVO
from state import State
from constants import LAUNCH_ALTITUDE, LAUNCH_ACCELERATION, BURNOUT_ACCELERATION, APOGEE_ALTITUDE

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
    ALTIMETER.zero()
except Exception as e:
    print(f"{e}: failed to zero BMP390.")

# Begin the control loop.
state = State.GROUND
start = time.time()
burnt = None
actuation_complete = False
ap = None
second_actuation_complete = False
SERVO.rotate(0)
time.sleep(2)
SERVO.rotate(30)
time.sleep(2)
SERVO.rotate(0)
print("starting loop!")
while True:
    try:
        # Read current time.
        current = time.time() - start

         # Read BMP390 sensor.
        altitude = ALTIMETER.altitude()
        temperature = ALTIMETER.temperature()

        # Read BNO055 sensor.
        acceleration = IMU.linear_acceleration()
        acceleration_x = acceleration[0]
        acceleration_y = acceleration[1]
        acceleration_z = acceleration[2]
        euler_angle = IMU.euler()
        euler_angle_0 = euler_angle[0]
        euler_angle_1 = euler_angle[1]
        euler_angle_2 = euler_angle[2]

        # Filter the data.
        data_filter.filter_data(altitude, acceleration_z)
        altitude_kalman = data_filter.kalman_altitude
        acceleration_kalman = data_filter.kalman_acceleration
        velocity_kalman = data_filter.kalman_velocity

        data_filter.filter_data(altitude, acceleration_y)
        altitude_kalman = data_filter.kalman_altitude
        acceleration_kalman = data_filter.kalman_acceleration
        velocity_kalman = data_filter.kalman_velocity

        # Determine the state of the ACS.
        # Ground -> Launched.
        if (state == State.GROUND and
            altitude_kalman > LAUNCH_ALTITUDE and
            acceleration_kalman > LAUNCH_ACCELERATION):
            state = State.LAUNCHED
        # Launched -> Burnout.
        elif (state == State.LAUNCHED and
              altitude_kalman < APOGEE_ALTITUDE and
              acceleration_kalman < BURNOUT_ACCELERATION):
            state = State.BURNOUT
        # Burnout -> Overshoot.
        elif (state == State.BURNOUT and
              altitude_kalman > APOGEE_ALTITUDE and
              acceleration_kalman < BURNOUT_ACCELERATION):
            state = State.OVERSHOOT
        # Burnout -> Apogee.
        elif (state == State.BURNOUT and
              altitude_kalman < APOGEE_ALTITUDE and
              velocity_kalman < APOGEE_VELOCITY):
            state = State.APOGEE
        # Overshoot -> Apogee.
        elif (state == State.OVERSHOOT and
              altitude_kalman > APOGEE_ALTITUDE and
              velocity_kalman < APOGEE_VELOCITY):
            state = State.APOGEE

        # Actuate.
        if state == State.BURNOUT and not actuation_complete:
            if burnt is None:
                print("actuating!!!")
                burnt = time.time()
                SERVO.rotate(30)
            elif time.time() - burnt > 3:
                SERVO.rotate(0)
                actuation_complete = True
        elif state == State.APOGEE and not second_actuation_complete:
            if ap is None:
                print("actuating again!!!")
                ap = time.time()
                SERVO.rotate(30)
            elif time.time() - ap > 3:
                SERVO.rotate(0)
                second_actuation_complete = True

        # Log the data
        writer.writerow([
            current,
            state,
            altitude_kalman,
            acceleration_kalman,
            velocity_kalman,
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
