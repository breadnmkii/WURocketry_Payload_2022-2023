import config
import time
import mathlib
import board
import math 

import adafruit_bno055 as a_bno

"""
Constants
"""
BMP_BUFFER_LEN = 200     # Length of sensor reading buffer
BNO_BUFFER_LEN = 200 


"""
Main components
"""
(bno, bmp) = config.init_avionics()
# delete any values from the front???
bno_buf = []
bmp_buf = []
acceleration_buffer = [None]*BNO_BUFFER_LEN
euler_buffer = [None]*BNO_BUFFER_LEN
altitude_buffer = [None]*BMP_BUFFER_LEN
pressure_buffer = [None]*BMP_BUFFER_LEN
bmp_pointer = 0 # pointer for a ring buffer for altitudes and pressures from BMP
bno_pointer = 0 # pointer for a ring buffer for euler orientations and linear accelerations from BNO

'''
TODO manage array size
    100 samples per second --> definitely overflow 
solution
    write file to disk
    ring buffer -- manage pointer, slice list itself
    
'''

"""
Function returning raw bno data
functionality: 
    push linear acceleration values into acceleration_buffer
    push displacement from vertical orientation values into quaternion_buffer
return: (accel(3), mag(3), gyro(3))
"""
def read_bno():
    quat = bno.getQuat()
    bno_pointer = bno_pointer % BNO_BUFFER_LEN
    if None not in quat:
        yy = quat.y() * quat.y() # 2 Uses below
        # convert to euler, then tell from vertical -- roll and pitch
        roll = math.atan2(2 * (quat.w() * quat.x() + quat.y() * quat.z()), 1 - 2*(quat.x() * quat.x() + yy))
        pitch = math.asin(2 * quat.w() * quat.y() - quat.x() * quat.z())
        yaw = math.atan2(2 * (quat.w() * quat.z() + quat.x() * quat.y()), 1 - 2*(yy+quat.z() * quat.z()))
        print('pitch: ', pitch)
        print('roll: ', roll)
        three_ele = [roll, pitch, yaw]
        # euler_buffer.append(three_ele) trying ring buffer right now
        euler_buffer[bno_pointer] = [roll, pitch, yaw]
        if bno_pointer % BNO_BUFFER_LEN == 0:
            with open('eulers.txt', 'a') as the_file:
                the_file.write(euler_buffer)
        
       
    acceleration = bno.linear_acceleration
    if None not in acceleration:
        # acceleration_buffer.append(acceleration) trying ring buffer right now
        acceleration_buffer[bno_pointer] = acceleration
        if bno_pointer == BNO_BUFFER_LEN-1:
            with open('accelerations.txt', 'a') as the_file:
                the_file.write(acceleration_buffer)
    bno_pointer = bno_pointer+1
    return (bno.acceleration, bno.magnetic, bno.gyro)


"""
Function returning raw bmp data 
return: (temp, pres, alt)
"""
def read_bmp():
    bmp_pointer = bmp_pointer % BMP_BUFFER_LEN
    altitude = bmp.altitude
    pressure = bmp.pressure
    '''
    transfering to ring buffer idea
    altitude_buffer.append(altitude)
    pressure_buffer.append(pressure)
    '''
    altitude_buffer[bmp_pointer] = altitude
    pressure_buffer[bmp_pointer] = pressure
    if bmp_pointer == BMP_BUFFER_LEN-1:
        with open('altitudes.txt', 'a') as the_file:
            #the_file.write(altitude)
            the_file.write(altitude_buffer)
        with open('pressures.txt', 'a') as the_file:
            #the_file.write(pressure)
             the_file.write(pressure_buffer)
    bmp_pointer = bmp_pointer+1
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

# for BMP readings only 
def differential_window(list, window):
    if (not list):
        return 0
    most_recent = bmp_pointer
    least_recent = bmp_pointer-window
    diff = 0 # will be turned into a ternary if
    diff = []
    if least_recent < 0:
        least_recent = BMP_BUFFER_LEN-1-abs(least_recent)
        diff = [list[i+1] - list[i] for i in range(0, most_recent)]
        diff.append([list[i+1] - list[i] for i in range(least_recent, BMP_BUFFER_LEN-1)])
    else:
        # when least_recent >= 0
        diff = [list[i+1] - list[i] for i in range(least_recent, most_recent)]
    
    return sum(diff)/window


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
def detectMovement(acc_accumulator):
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
def vertical(euler_accumulator):
    is_vertical = False
    rolling_window = 50
    threshold = 0.5 # NEED TESTING
    rolls = [item[0] for item in euler_accumulator]
    pitches = [item[1] for item in euler_accumulator]
    if (abs(average_window(rolls, rolling_window)) < threshold and abs(average_window(pitches, rolling_window)) < threshold):
        print("Camera is vertical from horizontal")
        is_vertical = True
    return is_vertical

'''
functionality: detect whether the payload is moving up, or moving down or 
'''
def altitude_status(altitude_accumulator, pressure_accumulator):
    rolling_window = 50
    descent_altitude = -2
    ascent_altitude =  2
    descent_pressure = 2
    ascent_pressure =  -2
    if (differential_window(altitude_accumulator, rolling_window) < descent_altitude and differential_window(pressure_accumulator, rolling_window) > descent_pressure):
        print('BMP -- payload is moving up')
        return 'up'
    elif (differential_window(altitude_accumulator, rolling_window) > ascent_altitude and differential_window(pressure_accumulator, rolling_window) < ascent_pressure):
        print('BMP -- payload is moving down')
        return 'down'
    else:
        print('BMP -- indeterminant')  
        return 'not_sure'      

def isUpright():
    if(bno.calibrated):
        print("Euler angle: {}".format(bno.euler))



def isAboveAltitude(altitude):
    if(altitude > bmp388.altitude):
        return True
    else:
        return False

def ground_level(altitude_accumulator, pressure_accumulator, groud_presure, ground_altitude):
    rolling_window = 50
    ground_altitude_sensitivity = 0.5 # NEED TESTING 
    ground_pressure_sensitivity = 0.5 # NEED TESTING 
    if ((abs(average_window(altitude_accumulator, rolling_window), ground_altitude) < ground_altitude_sensitivity) and
        (abs(average_window(pressure_accumulator, rolling_window), groud_presure)) < ground_pressure_sensitivity):
        return True
    else:
        return False

def remain_still(acc_accumulator):
    rolling_window = 50
    acceleration_sensitivity = 0.5 # NEED TESTING 
    if (abs(average_window(acc_accumulator, rolling_window), 0) < acceleration_sensitivity):
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
    print('entering main')
    read_bmp()
    read_bno()
    isUpright()
    print('exiting testing for read_bmp, read_bno, isUpright')

    # Test loop
    while True:
        this_sample_t = time.monotonic_ns()
        if (this_sample_t - last_sample_t >= DELTA_T):

            # Sample BMP388
            if (isAboveAltitude(0)):
                print("BMP is above!")
                print(bmp.pressure)
            

            last_sample_t = this_sample_t

