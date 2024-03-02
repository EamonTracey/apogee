#!/usr/bin/python3

import csv
from datetime import datetime
import logging
import time

from actuation_controller import ActuationController
from constants import HEADERS, OUTPUT_DIRECTORY
from piezo_buzzer import BUZZER
from kalman import DataFilter
from sensors import ALTIMETER, IMU
from servo_motor import SERVO
from state import State, determine_state

# Initialize various logging parameters.
now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
OUTPUT_DATA_PATH = f"{OUTPUT_DIRECTORY}/fullscale_data_{now}.csv"
OUTPUT_LOG_PATH = f"{OUTPUT_DIRECTORY}/fullscale_log_{now}.log"
logging.basicConfig(filename=OUTPUT_LOG_PATH, level=logging.DEBUG, filemode="w")

logging.debug("Knock knock. Who's there? ACS. ACS who? ACS.")

# Create csv writer (logger).
logging.debug(f"Opening output data file @ {OUTPUT_DATA_PATH}.")
writer = csv.writer(open(OUTPUT_DATA_PATH, "w+"))
writer.writerow(HEADERS)
logging.debug(f"Output data file is open @ {OUTPUT_DATA_PATH}.")

# Make the data filter.
logging.debug("Initializing the data filter.")
data_filter = DataFilter()
for _ in range(100):
    data_filter.filter_data(0, 0)
    time.sleep(0.05)
logging.debug("The data filter is initialized.")

# Zero the altimeter.
logging.debug("Zeroing the altimeter.")
try:
    ALTIMETER.zero()
except Exception as e:
    logging.exception("The altimeter failed to zero. This is fatal.")
    exit(1)
logging.debug(f"The altimeter is zeroed. Reading @ {ALTIMETER.altitude()} feet.")

logging.debug("Initializing the actuator.")
actuator = ActuationController(SERVO)
logging.debug("The actuator is initialized.")
start = time.time()
state = State.GROUND
logging.debug("Beginning the ACS control loop.")
while True:
    try:
        # Read current time.
        current = time.time() - start

         # Read BMP390 sensor.
        try:
            altitude = ALTIMETER.altitude()
            temperature = ALTIMETER.temperature()
        except Exception as e:
            logging.exception(f"Error reading the BMP390 altimeter: {e}.")
            logging.info(f"BMP390 last altitude: {altitude}.")
            logging.info(f"BMP390 last temperature: {temperature}.")
            continue

        # Read BNO055 sensor.
        try:
            acceleration = IMU.acceleration()
            acceleration_x = acceleration[0]
            acceleration_y = acceleration[1]
            acceleration_z = acceleration[2] - 31.0537
            euler_angle = IMU.euler()
            euler_angle_0 = euler_angle[0]
            euler_angle_1 = euler_angle[1]
            euler_angle_2 = euler_angle[2]
        except Exception as e:
            logging.exception(f"Error reading the BNO055 inertial measurement unit: {e}.")
            logging.info(f"BNO055 last acceleration: {acceleration}.")
            logging.info(f"BNO055 last euler angle: {euler_angle}.")
            continue

        # Filter the data.
        try:
            data_filter.filter_data(altitude, acceleration_z)
            altitude_filtered = data_filter.kalman_altitude
            acceleration_filtered = data_filter.kalman_acceleration
            velocity_filtered = data_filter.kalman_velocity
        except Exception as e:
            logging.exception(f"Error filtering the data: {e}.")
            logging.info(f"Filter last altitude: {altitude_filtered}.")
            logging.info(f"Filter last acceleration: {acceleration_filtered}.")
            logging.info(f"Filter last velocity: {velocity_filtered}.")
            continue


        # Determine the state of the ACS.
        try:
            state = determine_state(state, altitude_filtered, acceleration_filtered, velocity_filtered)
        except Exception as e:
            logging.exception(f"Error within state determination: {e}.")
            logging.info(f"Determinator last state: {state}.")
            continue

        # Log the data
        writer.writerow([
            current,
            state,
            SERVO.percentage,
            actuator.apogee_prediction,
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

        # Run actuation control algorithm.
        try:
            actuator.actuate(state, altitude_filtered, acceleration_filtered, velocity_filtered, current)
        except Exception as e:
            logging.exception(f"Error within actuation control: {e}.")
    except BaseException as e:
        logging.error(f"BaseException caught (this is bad): {e}")
