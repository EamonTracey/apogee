#!/usr/bin/python3

import board
import csv
from datetime import datetime
import logging
import time

from acs2024.control import ActuationController, State, determine_state, servo_percentage_to_flap_angle
from acs2024.devices.piezo_buzzer import PiezoBuzzer
from acs2024.devices.sensors import BMP390, BNO055
from acs2024.devices.servo_motor import ServoMotor
from acs2024.filter import DataFilter

# Output data constants.
OUTPUT_DIRECTORY = "/home/acs/data/fullscale"
HEADERS = [
    "Time",
    "State",
    "Flap Angle",
    "Apogee Prediction",
    "Altitude Filtered",
    "Velocity Filtered",
    "Acceleration Filtered",
    "Altitude",
    "Acceleration X",
    "Acceleration Y",
    "Acceleration Z",
    "Magnetic X",
    "Magnetic Y",
    "Magnetic Z",
    "Gyro X",
    "Gyro Y",
    "Gyro Z",
    "Temperature"
]

# Initialize various logging parameters.
now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
OUTPUT_DATA_PATH = f"{OUTPUT_DIRECTORY}/fullscale_data_{now}.csv"
OUTPUT_LOG_PATH = f"{OUTPUT_DIRECTORY}/fullscale_log_{now}.log"
logging.basicConfig(filename=OUTPUT_LOG_PATH, level=logging.DEBUG, filemode="w")
logging.getLogger().addHandler(logging.StreamHandler())

# Jokes.
logging.debug("Knock knock. Who's there? ACS. ACS who? ACS.")
logging.debug("ACS is the all-American air brake system ... not a metric unit in sight.")
logging.debug("Disabling independent flap actuation to abide by federal missile laws.")

# Create CSV writer.
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

# Create the devices.
logging.debug("Creating the device drivers.")
i2c = board.I2C()
altimeter = BMP390(i2c)
imu = BNO055(i2c)
servo = ServoMotor(board.D12)
buzzer = PiezoBuzzer(board.D13)
logging.debug("The device drivers are up and running.")

# Zero the altimeter.
logging.debug("Zeroing the altimeter.")
try:
    altimeter.zero()
except Exception as e:
    logging.exception("The altimeter failed to zero. This is fatal.")
    exit(1)
logging.debug(f"The altimeter is zeroed. Reading @ {altimeter.altitude()} feet.")

# Run the actuation sequence.
logging.debug("Beginning the initial actuation sequence.")
buzzer.beep(1)
servo.rotate(0)
time.sleep(2)
servo.rotate(35)
time.sleep(2)
servo.rotate(0)
buzzer.beep(1)
logging.debug("Initial actuation sequence complete.")

logging.debug("Initializing the actuator.")
actuator = ActuationController()
logging.debug("The actuator is initialized.")

logging.debug("The launch vehicle is currently on the ground.")
state = State.GROUND

start = time.time()
logging.debug(f"Start time (Unix epoch): {start}.")

logging.debug("Beginning the ACS control loop.")
while True:
    try:
        # Read current time.
        time_current = time.time() - start

         # Read BMP390 sensor.
        try:
            altitude = altimeter.altitude()
            temperature = altimeter.temperature()
        except Exception as e:
            logging.exception(f"Error reading the BMP390 altimeter: {e}.")
            logging.info(f"BMP390 last altitude: {altitude}.")
            logging.info(f"BMP390 last temperature: {temperature}.")
            continue

        # Read BNO055 sensor.
        try:
            acceleration = imu.acceleration()
            acceleration_x = acceleration[0]
            acceleration_y = acceleration[1]
            acceleration_z = acceleration[2] - 32.15
            magnetic = imu.magnetic()
            magnetic_x = magnetic[0]
            magnetic_y = magnetic[1]
            magnetic_z = magnetic[2]
            gyro = imu.gyro()
            gyro_x = gyro[0]
            gyro_y = gyro[1]
            gyro_z = gyro[2]
        except Exception as e:
            logging.exception(f"Error reading the BNO055 inertial measurement unit: {e}.")
            logging.info(f"BNO055 last acceleration: ({acceleration_x}, {acceleration_y}, {acceleration_z}).")
            logging.info(f"BNO055 last magnetic: ({magnetic_x}, {magnetic_y}, {magnetic_z}).")
            logging.info(f"BNO055 last gyro: ({gyro_x}, {gyro_y}, {gyro_z}).")
            continue

        # Filter the data.
        try:
            data_filter.filter_data(altitude, acceleration_z)
            altitude_filtered = data_filter.kalman_altitude
            velocity_filtered = data_filter.kalman_velocity
            acceleration_filtered = data_filter.kalman_acceleration
        except Exception as e:
            logging.exception(f"Error filtering the data: {e}.")
            logging.info(f"Filter last altitude: {altitude_filtered}.")
            logging.info(f"Filter last acceleration: {acceleration_filtered}.")
            logging.info(f"Filter last velocity: {velocity_filtered}.")
            continue


        # Determine the state of the ACS.
        try:
            state = determine_state(state, altitude_filtered, velocity_filtered, acceleration_filtered)
        except Exception as e:
            logging.exception(f"Error within state determination: {e}.")
            logging.info(f"Determinator last state: {state}.")
            continue

        # Determine the current flap angle.
        flap_angle = servo_percentage_to_flap_angle(servo.percentage)

        # Log the data
        writer.writerow([
            time_current,
            state,
            flap_angle,
            actuator.apogee_prediction,
            altitude_filtered,
            velocity_filtered,
            acceleration_filtered,
            altitude,
            acceleration_x,
            acceleration_y,
            acceleration_z,
            magnetic_x,
            magnetic_y,
            magnetic_z,
            gyro_x,
            gyro_y,
            gyro_z,
            temperature
        ])

        # Run actuation control algorithm.
        try:
            actuation_degree = actuator.calculate_actuation(
                time_current,
                state,
                flap_angle,
                altitude_filtered,
                velocity_filtered
            )
            if actuation_degree is not None:
                servo.rotate(actuation_degree)
        except Exception as e:
            logging.exception(f"Error within actuation control: {e}.")
    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt detected; exiting gracefully.")
        break
    except BaseException as e:
        logging.error(f"BaseException caught (this is bad): {e}")
