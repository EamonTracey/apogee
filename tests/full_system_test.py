import time
import board
import adafruit_bmp3xx
import adafruit_bno055
import pwmio

# I2C setup
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bno = adafruit_bno055.BNO055_I2C(i2c)
buzzer = pwmio.PWMOut(board.D13, variable_frequency=False)
motor = pwmio.PWMOut(board.D12, variable_frequency=False)

# SPI setup
# from digitalio import DigitalInOut, Direction
# spi = board.SPI()
# cs = DigitalInOut(board.D5)
# bmp = adafruit_bmp3xx.BMP3XX_SPI(spi, cs)
sample_count = 0
bmp.pressure_oversampling = 1
buzzer.frequency = 1000
motor.frequency = 330
OFF = 0
ON = 2**16
MOTOR_MIN_PERCENT_D = 0.20
MOTOR_MAX_PERCENT_D = 0.50
buzzer.duty_cycle = ON/2
print("BEEP!")
time.sleep(2)
buzzer.duty_cycle = OFF
motor.duty_cycle = (MOTOR_MIN_PERCENT_D*ON)
time.sleep(2)
print("Motor Duty Cycle = {}".format(motor.duty_cycle/ON))
motor.duty_cycle = (MOTOR_MAX_PERCENT_D*ON)
time.sleep(2)
print("Motor Duty Cycle = {}".format(motor.duty_cycle/ON))
motor.duty_cycle = (MOTOR_MIN_PERCENT_D*ON)
time.sleep(2)
print("Motor Duty Cycle = {}".format(motor.duty_cycle/ON))

start_time = time.time()

while True:
    print("BMP390 Data")
    print(
        "Pressure (Pa): {:6.4f}  Altitude (m): {:6.4f}".format(bmp.pressure, bmp.altitude)
    )
    # time.sleep(1)
    print()
    print("BNO055 Data")
    print("Accelerometer (m/s^2): {}".format(bno.acceleration))
    print("Magnetometer (microteslas): {}".format(bno.magnetic))
    print("Gyroscope (rad/sec): {}".format(bno.gyro))
    print("Euler angle: {}".format(bno.euler))
    #print("Quaternion: {}".format(bno.quaternion))
    #print("Linear acceleration (m/s^2): {}".format(bno.linear_acceleration))
    #print("Gravity (m/s^2): {}".format(bno.gravity))
    print()




    sample_count+=1
    print("Sample Rate (Hz) = {}".format((sample_count)/(time.time()-start_time)))

