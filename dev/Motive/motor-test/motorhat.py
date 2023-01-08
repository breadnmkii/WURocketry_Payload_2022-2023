import time
import board
import numpy
from adafruit_motorkit import MotorKit

def forwardLoop(min, max):
    for ()


def reverseLoop(min, max):


if __name__ == '__main__':

    # Initialize motorhat class
    hat = MotorKit(i2c = board.I2C())

    print("Starting...")
    time.sleep(3)

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

    print("Stopping")
    hat.motor1.throttle = 0