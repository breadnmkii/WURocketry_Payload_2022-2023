from adafruit_motorkit import MotorKit
from . import lib_para_360_servo
import pigpio
import board
import time
#init pigpio to access GPIO pins with PWM
pi = pigpio.pi()

def servo_config(write_gpio, read_gpio):
    #Define GPIO pins that we will read and write to (Using GPIO numbers NOT pin numbers)
    WHITE_CABLE_WRITE = write_gpio #23
    YELLOW_CABLE_READ = read_gpio #24  


    #init servo and servo position reader from lib_para_360_servo
    servo = lib_para_360_servo.write_pwm(pi = pi, gpio = WHITE_CABLE_WRITE)
    reader = lib_para_360_servo.read_pwm(pi = pi, gpio = YELLOW_CABLE_READ)

    #Buffer time for initializing library servo
    time.sleep(2)
    print("INIT")
    servo.stop()

    return servo, reader

# motor1 = separation motor, motor2 = solenoid1, motor3 = solenoid2
def electromotives_config():
    hat = MotorKit(i2c = board.I2C())
    motor = hat.motor1
    solenoids = (hat.motor2, hat.motor3)

    return (motor, solenoids)