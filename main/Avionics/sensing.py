import config
import time
import mathlib
import board
import math 

import adafruit_bno055 as a_bno

"""
Constants
"""
BUFFER_LEN = 25     # Length of sensor reading buffer


"""
Main components
"""
(bno, bmp) = config.init_avionics()
bno_buf = []
bmp_buf = []
acceleration_buffer = []
quaternion_buffer = []


"""
Function returning raw bno data
functionality: 
    push linear acceleration values into acceleration_buffer
    push displacement from vertical orientation values into quaternion_buffer
return: (accel(3), mag(3), gyro(3))
"""
def read_bno():
    quat = bno.getQuat()
    yy = quat.y() * quat.y() # 2 Uses below
    roll = math.atan2(2 * (quat.w() * quat.x() + quat.y() * quat.z()), 1 - 2*(quat.x() * quat.x() + yy))
    pitch = math.asin(2 * quat.w() * quat.y() - quat.x() * quat.z())
    yaw = math.atan2(2 * (quat.w() * quat.z() + quat.x() * quat.y()), 1 - 2*(yy+quat.z() * quat.z()))
    three_ele = [roll, pitch, yaw]
    quaternion_buffer.append(three_ele)
    
    acceleration_buffer.append(bno.linear_acceleration)
    return (bno.acceleration, bno.magnetic, bno.gyro)


"""
Function returning raw bmp data 
return: (temp, pres, alt)
"""
def read_bmp():
    return (bmp.temperature, bmp.pressure, bmp.altitude)


""" 
Function to determine if payload is moving,
with sensitivity of 'window' readings mean
"""
def isMoving(window):
    if(bno.linear_acceleration == 0.0): #Assuming it returns in m/s based from documentation
        print("Not moving")
    else:
        print("Moving")

def average_window(list, window):
    if(not list):
        return 0
    return sum(map(lambda acc: abs(acc), list[-window:]))/window

'''
from previous year's code
functionality: detect whether the payload has launched or not
input: 
    acc_accumulator: array of acceleration values
    gps: gps object from adafruit_gps
return:
    True if rocket has launched and is moving
    False if payload is relatively static right now
'''
def detectLaunch(acc_accumulator):
    MOTION_SENSITIVITY = 3           # Amount of 3-axis acceleration needed to be read to trigger "movement" detection
    MOTION_LAUNCH_SENSITIVITY = 13   # Amount of accel added to offset for stronger initial launch accel
    hasLaunched = False
    ACC_WINDOW = 50                  # Range of values to apply rolling average in 'acc_accumulator'
    if(average_window(acc_accumulator, ACC_WINDOW) > MOTION_SENSITIVITY + MOTION_LAUNCH_SENSITIVITY):
        print("Launch detected!")
        hasLaunched = True
    return hasLaunched
    
'''
functionality: detect whether the camera has reached vertical position or not
'''
def vertical(quaternion_accumulator):
    is_vertical = False
    quarternion_window = 50
    threshold = 2 # NEED TESTING
    if (average_window(quaternion_accumulator, quarternion_window) > threshold):
        print("Camera is vertical from horizontal")
        is_vertical = True
    return is_vertical

def isUpright():
    if(bno.calibrated):
        print("Euler angle: {}".format(bno.euler))



def isAboveAltitude(altitude):
    if(altitude > bmp388.altitude):
        return True
    else:
        return False




if __name__ == '__main__':
    
    SECOND_NS = 1_000_000_000
    NUM_READINGS = 25
    SAMPLE_FREQUENCY = 100   # in Hz
    DELTA_T = SECOND_NS/SAMPLE_FREQUENCY
    last_sample_t = time.monotonic_ns()

    # start_sample_T = time.monotonic_ns()
    isUpright()

    # Test loop
    while True:
        this_sample_t = time.monotonic_ns()
        if (this_sample_t - last_sample_t >= DELTA_T):

            # Sample BMP388
            if (isAboveAltitude(0)):
                print("BMP is above!")
                print(bmp.pressure)
            

            last_sample_t = this_sample_t


if __name__ == '__main__':
    print(read_bmp())
    print(read_bno())

