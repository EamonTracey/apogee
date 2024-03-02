# Physical constants.
G = 32.17405              # feet / second^2

# State determination constants.
LAUNCH_ALTITUDE = 150     # feet
LAUNCH_ACCELERATION = 200 # feet / second^2
BURNOUT_ACCELERATION = 8  # feet / second^2
BURNOUT_ALTITUDE = 1000   # feet
APOGEE_ALTITUDE = 5200    # altitude

# Launch vehicle constants.
VEHICLE_MASS = 1.1902231  # slugs

OUTPUT_DIRECTORY = "/home/acs/data/fullscale"
HEADERS = [
    "Time",
    "State",
    "Servo Percentage",
    "Apogee Prediction",
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
