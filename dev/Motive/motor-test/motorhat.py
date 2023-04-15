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


### TEST: separation: 80s
### TEST: retract: 

## NOTE: left Mport is GND, right Mport is POS
# throttle = 1 is outwards, -1 is backwards (into body tube)

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
    print("Running")
    # hat.motor1.throttle = 1
    # time.sleep(2)
    # hat.motor1.throttle = 0
    print("Move")
    hat.motor2.throttle = 1
    
    # busy loop to ensure we can ctrl+c process
    while True:
        pass

    # print("Starting...")
    # # time.sleep(1)

    # print("Running")
    # MOTOR.throttle = -1 #Forward

    # time.sleep(TIME_SEPARATE)

    # print("Done!")
    # MOTOR.throttle = 0

