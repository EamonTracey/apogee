import time

import board

from acs2024.control import State, determine_state, predict_apogee, calculate_drag, ActuationController
from acs2024.devices.servo_motor import ServoMotor

s = ServoMotor(board.D12)
s.rotate(0)
time.sleep(1)

readline = lambda f: f.readline().strip().split(",")

data = open("../data/Fullscale 2/fullscale_2_cut.csv")
headers = readline(data)

time_i = headers.index("Time")
state_i = headers.index("State")
altitude_i = headers.index("Altitude Filtered")
acceleration_i = headers.index("Acceleration Filtered")
velocity_i = headers.index("Velocity Filtered")
flap_i = headers.index("Servo Percentage")

test_state = State.GROUND
test_prediction = 5800
last_test_actuation = 0
test_actuation = 0
actuator = ActuationController()
last_time = 0
c = 0
while True:
    line = readline(data)
    if line == [""]:
        break

    time_ = float(line[time_i])
    state = State[line[state_i][6:]]
    altitude = float(line[altitude_i])
    acceleration = float(line[acceleration_i])
    velocity = float(line[velocity_i])
    flap_angle = float(line[flap_i])
    dt = time_ - last_time

    test_state = determine_state(test_state, altitude, velocity, acceleration)
    test_prediction = predict_apogee(test_actuation or 0, altitude, velocity)
    test_actuation = actuator.calculate_actuation(time_, test_state, test_actuation or 0, altitude, velocity)
    if test_actuation is not None:
        c += 1
        s.rotate(test_actuation)
        print(f"{c}   Time: {time.time()}     Altitude: {altitude}     Projection: {test_prediction}")
        time.sleep(dt)

    last_time = time_
