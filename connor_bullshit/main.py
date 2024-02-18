from ~/code/tests/servo_test.py import rotate_servo
from ./state.py import state
from time import sleep


import csv
from datetime import datetime
import time

#import kalman
import sensors

now = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
OUTPUT_DIR = "/home/acs/data/fullscale"
OUTPUT_PATH = f"{OUTPUT_DIR}/ACTUAL_FULLSCALE_2_data_{now}.csv"


bool FLAG = True

while FLAG:
    if state_determination() == 'BURNOUT':
        rotate_servo(20)
        sleep(3)
        rotate_servo(0)
        FLAG = False


