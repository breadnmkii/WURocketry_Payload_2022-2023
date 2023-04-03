import time
import board
import signal
import sys

from adafruit_motorkit import MotorKit

# def throttleLoop(hat, min, max, step, reverse=False):
#     for val in np.arange(min, max, step):
#         if reverse:
#             val *= -1
#         print("Throttle @", val)
#         hat.motor1.throttle = val
#         time.sleep(3)


## NOTE: left Mport is GND, right Mport is POS

TIME_SEPARATE = 60 # in seconds
TIME_RETRACT = 30

hat = MotorKit(i2c = board.I2C())
MOTOR = hat.motor2

# SIGINT abort
def abort_motor(sig, frame):
    print("Caught SIGINT")
    hat.motor1.throttle = 0
    hat.motor2.throttle = 0
    hat.motor3.throttle = 0
    sys.exit(0)
signal.signal(signal.SIGINT, abort_motor)

if __name__ == '__main__':
    hat.motor1.throttle = 0
    hat.motor2.throttle = -1
    time.sleep(100000)

    # print("Starting...")
    # # time.sleep(1)

    # print("Running")
    # MOTOR.throttle = -1 #Forward

    # time.sleep(TIME_SEPARATE)

    # print("Done!")
    # MOTOR.throttle = 0

