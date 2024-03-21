from acs2024.control import State, determine_state, predict_apogee, calculate_drag, ActuationController

readline = lambda f: f.readline().strip().split(",")

data = open("../data/Fullscale 2/fullscale_2_cut.csv")
headers = readline(data)

time_i = headers.index("Time")
state_i = headers.index("State")
altitude_i = headers.index("Altitude Filtered")
acceleration_i = headers.index("Acceleration Filtered")
velocity_i = headers.index("Velocity Filtered")

test_state = State.GROUND
test_prediction = 5800
test_actuator = ActuationController()
while True:
    line = readline(data)
    if line == [""]:
        break


    time = float(line[time_i])
    state = State[line[state_i][6:]]
    altitude = float(line[altitude_i])
    acceleration = float(line[acceleration_i])
    velocity = float(line[velocity_i])

    test_state = determine_state(test_state, altitude, acceleration, velocity)
    test_prediction = predict_apogee(altitude, acceleration, velocity, calculate_drag(0, velocity))
    test_actuation = test_actuator.calculate_actuation(test_state, altitude, acceleration, velocity, time, 0)
    print(test_actuation)
