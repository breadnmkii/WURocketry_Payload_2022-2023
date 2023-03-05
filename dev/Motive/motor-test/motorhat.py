import time
import board
# import numpy as np
from adafruit_motorkit import MotorKit

# def throttleLoop(hat, min, max, step, reverse=False):
#     for val in np.arange(min, max, step):
#         if reverse:
#             val *= -1
#         print("Throttle @", val)
#         hat.motor1.throttle = val
#         time.sleep(3)


if __name__ == '__main__':

    # Initialize motorhat class
    hat = MotorKit(i2c = board.I2C())

    print("Starting...")
    time.sleep(5)
    print("Running")
    #throttleLoop(hat, 0, 1.1, 0.1)
    hat.motor1.throttle = 1 #Forward
    #hat.motor1.throttle = -1: reverse
    time.sleep(5)
    print("Done!")
    hat.motor1.throttle = 0
    """

    print("25% Speed")
    hat.motor1.throttle = 0.25
    time.sleep(3)

    print("50% Speed")
    hat.motor1.throttle = 0.5
    time.sleep(3)

    print("75% Speed")
    hat.motor1.throttle = 0.75
    time.sleep(2)

    print("100% Speed")
    hat.motor1.throttle = 1.0
    time.sleep(2)

    print("75% Speed reverse")
    hat.motor1.throttle = -0.75
    time.sleep(2)

    print("50% Speed reverse")
    hat.motor1.throttle = -0.5
    time.sleep(3)

    print("25% Speed reverse")
    hat.motor1.throttle = -0.25
    time.sleep(3)

    """

    print("Stopping")
    hat.motor1.throttle = 0