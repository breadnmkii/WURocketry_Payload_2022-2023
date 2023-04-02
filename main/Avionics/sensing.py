from . import config
import time
import board
import math 
#import numpy as np
#import adafruit_bno055 as a_bno

"""
Constants
"""
BMP_BUFFER_LEN = 200     # Length of sensor reading buffer
BNO_BUFFER_LEN = 50  # length 50 for testing


"""
Main components
"""
bno = config.init_bno()
bmp = config.init_bmp()
# delete any values from the front??? -- TODO: pointer none stuffs
bno_buf = []
bmp_buf = []
acceleration_buffer = [[None, None, None] for _ in range(BNO_BUFFER_LEN)]
euler_buffer = [[None, None, None] for _ in range(BNO_BUFFER_LEN)]
seqeuntial_euler = [[None, None, None]]
altitude_buffer = [None]*BMP_BUFFER_LEN
pressure_buffer = [None]*BMP_BUFFER_LEN
temperature_buffer = [None]*BMP_BUFFER_LEN
#global bmp_pointer
bmp_pointer = 0 # pointer for a ring buffer for altitudes and pressures from BMP
#global bno_pointer
bno_pointer = 0 # pointer for a ring buffer for euler orientations and linear accelerations from BNO
euler_orient_pointer = 0
linear_acc_pointer = 0

def read_bno():
    quat = bno.quaternion
    global bno_pointer
    global euler_orient_pointer
    global linear_acc_pointer
    global seqeuntial_euler
    euler_orient_pointer = euler_orient_pointer % BNO_BUFFER_LEN
    linear_acc_pointer = linear_acc_pointer % BNO_BUFFER_LEN

    if None not in quat:
        [x, y, z, w] = quat
        yy = y * y # 2 Uses below
        # convert to euler, then tell from vertical -- roll and pitch
        yaw = math.atan2(2 * (w* x + y * z), 1 - 2*(x * x + yy))
        # clamping asin values
        pitch = math.asin(max(-1, min(2 * w * y - x * z, 1)))
        roll= math.atan2(2 * (w* z + x * y), 1 - 2*(yy+z * z))
        three_ele = [roll, pitch, yaw]
        euler_buffer[euler_orient_pointer] = [roll, pitch, yaw]
        euler_orient_pointer = euler_orient_pointer+1
        seqeuntial_euler.insert(0, three_ele)
        seqeuntial_euler = seqeuntial_euler[:BNO_BUFFER_LEN]

        
    # thinking about splitting into two functions not sure how to deal with the pointer though 
    acceleration = bno.linear_acceleration
    if None not in acceleration:
        # acceleration_buffer.append(acceleration) trying ring buffer right now
        #acceleration_buffer[bno_pointer] = acceleration
        acceleration_buffer[linear_acc_pointer] = acceleration
        linear_acc_pointer = linear_acc_pointer+1
    
    # write data to file 
    # if bno_pointer == BNO_BUFFER_LEN-1:
    if linear_acc_pointer == BNO_BUFFER_LEN-1:
        with open('accelerations.txt', 'a') as the_file:
            the_file.write(str(acceleration_buffer))
    if euler_orient_pointer == BNO_BUFFER_LEN-1:
        with open('eulers.txt', 'a') as the_file:
            '''
            # may need to format txt files
            data_f.write(f"{time_thisSample-time_launchStart}")
            data_f.write(f"{acc[0]}\t{acc[1]}\t{acc[2]}\t")
            data_f.write(f"{qua[0]}\t{qua[1]}\t{qua[2]}\t{qua[3]}\n")
            '''
            the_file.write(str(euler_buffer))
    
    #bno_pointer = bno_pointer+1
        
    return (bno.magnetic, bno.gyro)

'''
testing status:
    tested, needed in final version
'''
def read_euler_buffer():
    quat = bno.quaternion
    global euler_orient_pointer
    euler_orient_pointer = euler_orient_pointer % BNO_BUFFER_LEN

    if None not in quat:
        [x, y, z, w] = quat 
        yy = y * y # 2 Uses below
        # convert to euler, then tell from vertical -- roll and pitch
        yaw = math.atan2(2 * (w* x + y * z), 1 - 2*(x * x + yy))
        # clamping asin values
        pitch = math.asin(max(-1, min(2 * w * y - x * z, 1)))
        roll= math.atan2(2 * (w* z + x * y), 1 - 2*(yy+z * z))
        three_ele = [roll, pitch, yaw]
        #print("r,p,y:\t", three_ele)
        euler_buffer[euler_orient_pointer] = [roll, pitch, yaw]
        euler_orient_pointer = euler_orient_pointer+1
    
    if euler_orient_pointer == BNO_BUFFER_LEN-1:
        with open('eulers.txt', 'a') as the_file:
            '''
            # may need to format txt files
            data_f.write(f"{time_thisSample-time_launchStart}")
            data_f.write(f"{acc[0]}\t{acc[1]}\t{acc[2]}\t")
            data_f.write(f"{qua[0]}\t{qua[1]}\t{qua[2]}\t{qua[3]}\n")
            '''
            the_file.write(str(euler_buffer))
    
    return euler_buffer

'''
testing status:
    tested, needed in final version
'''
def read_acceleration_buffer():
    global linear_acc_pointer
    linear_acc_pointer = linear_acc_pointer % BNO_BUFFER_LEN
    acceleration = bno.linear_acceleration
    if None not in acceleration:
        acceleration_buffer[linear_acc_pointer] = acceleration
        linear_acc_pointer = linear_acc_pointer+1
    
    # write data to file 
    # if bno_pointer == BNO_BUFFER_LEN-1:
    if linear_acc_pointer == BNO_BUFFER_LEN-1:
        with open('accelerations.txt', 'a') as the_file:
            the_file.write(str(acceleration_buffer))
    
    return acceleration_buffer


"""
Function returning raw bmp data 
return: (temp, pres, alt)
testing status:
    tested, needed in final version
"""
def read_bmp():
    global bmp_pointer
    bmp_pointer = bmp_pointer % BMP_BUFFER_LEN
    altitude = bmp.altitude
    pressure = bmp.pressure
    temperature = bmp.temperature
    '''
    transfering to ring buffer idea
    altitude_buffer.append(altitude)
    pressure_buffer.append(pressure)
    '''
    if altitude and pressure and temperature:
        altitude_buffer[bmp_pointer] = altitude
        pressure_buffer[bmp_pointer] = pressure
        temperature_buffer[bmp_pointer] = temperature
        bmp_pointer = bmp_pointer+1
    
    if bmp_pointer == BMP_BUFFER_LEN-1:
        with open('altitudes.txt', 'a') as the_file:
            the_file.write(str(altitude_buffer))
        with open('pressures.txt', 'a') as the_file:
             the_file.write(str(pressure_buffer))

    return (temperature_buffer, pressure_buffer, altitude_buffer)


def average_window(list, window, pointer):
    if(not list):
        return 0
    
    buf_len = len(list)
    start = (pointer - window + 1) % buf_len
    end = (pointer + 1) % buf_len
    window_list = None
    if start <= end:
        window_list = list[start:end]
    else:
        window_list = list[start:] + list[:end]

    window_list = [abs(x) for x in window_list if x is not None]
    if len(window_list) == 0:
        return 0

    return sum(window_list) / len(window_list)
    
'''
testing status:
    tested, needed in final version
'''
def average_sum_abs_range(list, least_recent, most_recent):
    of_interest = list[least_recent:most_recent+1]
    print('averaging window:', of_interest)
    values = [abs(x) for x in of_interest if x is not None]
    if len(values) == 0:
        return 0
    print('average:', sum(values) / len(values))
    return sum(values) / len(values)

# for BMP readings only 
def differential_window(list, window):
    if (not list):
        return 0
    
    '''
    most_recent = bmp_pointer
    least_recent = bmp_pointer-window
    diff = []
    if least_recent < 0:
        least_recent = BMP_BUFFER_LEN-1-abs(least_recent)
        diff = [list[i+1] - list[i] for i in range(0, most_recent)]
        diff.append([list[i+1] - list[i] for i in range(least_recent, BMP_BUFFER_LEN-1)])
    else:
        # when least_recent >= 0
        diff = [list[i+1] - list[i] for i in range(least_recent, most_recent)]
    '''
    buf_len = len(list)
    start = (bmp_pointer - window + 1) % buf_len
    end = (bmp_pointer + 1) % buf_len
    window_list = []
    if start <= end:
        window_list = list[start:end]
    else:
        window_list = list[start:] + list[:end]
    # need to take care of none initializations
    filtered_list = [x for x in window_list if x is not None]
    print('erroring:', filtered_list)
    #window_list = list(filter(lambda item: item is not None, window_list))
    # for the first value ever written to the list
    if len(filtered_list) < 2:
        return filtered_list[0]
    diff = [filtered_list[i+1] - filtered_list[i] for i in filtered_list 
            #if window_list[i] is not None and window_list[i+1] is not None
            ]

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
testing status:
    tested, needed in final version
'''
def detectMovement(acc_accumulator):
    global linear_acc_pointer
    MOTION_SENSITIVITY = 2           # Amount of 3-axis acceleration needed to be read to trigger "movement" detection
    isMoving = False
    ACC_WINDOW = 20                  # Range of values to apply rolling average in 'acc_accumulator'

    x = [item[0] for item in acc_accumulator]
    y = [item[1] for item in acc_accumulator]
    z = [item[2] for item in acc_accumulator]

    if(average_window(x, ACC_WINDOW, linear_acc_pointer) > MOTION_SENSITIVITY 
       or average_window(y, ACC_WINDOW, linear_acc_pointer) > MOTION_SENSITIVITY 
       or average_window(z, ACC_WINDOW, linear_acc_pointer) > MOTION_SENSITIVITY
       ):
        print("Motion detected!")
        isMoving = True
    return isMoving

def detectLaunch(acc_accumulator):
    global linear_acc_pointer
    MOTION_SENSITIVITY = 1           # Amount of 3-axis acceleration needed to be read to trigger "movement" detection
    MOTION_LAUNCH_SENSITIVITY = 10   # Amount of accel added to offset for stronger initial launch accel
    hasLaunched = False
    ACC_WINDOW = 20                  # Range of values to apply rolling average in 'acc_accumulator'

    x = [item[0] for item in acc_accumulator]
    y = [item[1] for item in acc_accumulator]
    z = [item[2] for item in acc_accumulator]

    if(average_window(x, ACC_WINDOW, linear_acc_pointer) > MOTION_SENSITIVITY + MOTION_LAUNCH_SENSITIVITY 
       or average_window(y, ACC_WINDOW, linear_acc_pointer) > MOTION_SENSITIVITY + MOTION_LAUNCH_SENSITIVITY
       or average_window(z, ACC_WINDOW, linear_acc_pointer) > MOTION_SENSITIVITY + MOTION_LAUNCH_SENSITIVITY
       ):
        print("Launch detected!")
        hasLaunched = True
    return hasLaunched
    
    
'''
functionality: detect whether the camera has reached vertical position or not
testing status:
    tested, needed in final version
'''
def vertical(euler_accumulator):
    global euler_orient_pointer
    is_vertical = False
    rolling_window = 15
    threshold = 0.4 # NEED TESTING -- tested 0.15 on 3/6 by itself -- tested again 3/24 on motor hat not stable enough -> changed to 0.2
    rolls = [item[0] for item in euler_accumulator]
    pitches = [item[1] for item in euler_accumulator]
    pitch= abs(average_window(pitches, rolling_window, euler_orient_pointer))
    roll = abs(average_window(rolls, rolling_window, euler_orient_pointer))

    filtered_rolls = [abs(x) for x in rolls if x is not None]
    averaged_roll = sum(filtered_rolls) / len(filtered_rolls)

    filtered_pitches = [abs(x) for x in pitches if x is not None]
    averaged_pitch = sum(filtered_pitches) / len(filtered_pitches)

    #print('inspecting rolls:', rolls)
    if (averaged_roll < threshold and averaged_pitch < threshold):
        print("Camera is vertical from horizontal: row pitch", averaged_roll, averaged_pitch)
        
        is_vertical = True
    else:
        print('not vertical:', averaged_roll, averaged_pitch)
    return is_vertical

'''
functionality: detect whether the payload is moving up, or moving down or 
'''
def altitude_status(altitude_accumulator, pressure_accumulator):
    rolling_window = 50
    descent_altitude = -2 # HOW TO TEST THRESHOLD
    ascent_altitude =  2 # HOW TO TEST THRESHOLD 
    descent_pressure = 0.5 # HOW TO TEST THRESHOLD from sea level to apogee
    ascent_pressure =  -0.5 # HOW TO TEST THRESHOLD 1000-755 = 245 in range
    if (differential_window(altitude_accumulator, rolling_window) < descent_altitude and differential_window(pressure_accumulator, rolling_window) > descent_pressure):
        print('BMP -- payload is moving up')
        return 'up'
    elif (differential_window(altitude_accumulator, rolling_window) > ascent_altitude and differential_window(pressure_accumulator, rolling_window) < ascent_pressure):
        print('BMP -- payload is moving down')
        return 'down'
    else:
        print('BMP -- indeterminant')  
        return 'not_sure'      
'''
not needed for final version 
'''
def isUpright():
    if(bno.calibrated):
        print("Euler angle: {}".format(bno.euler))


'''
not needed for final version 
'''
def isAboveAltitude(altitude):
    if(altitude > bmp388.altitude):
        return True
    else:
        return False

'''
TODO: testing
'''
def ground_level(altitude_accumulator, pressure_accumulator):
    rolling_window = 50
    ground_altitude_sensitivity = 0.5 # NEED TESTING 
    ground_pressure_sensitivity = 0.5 # NEED TESTING 
    if ((abs(average_window(altitude_accumulator, rolling_window, bmp_pointer), bmp.sea_level_altitude) < ground_altitude_sensitivity) and
        (abs(average_window(pressure_accumulator, rolling_window, bmp_pointer), bmp.sea_level_pressure)) < ground_pressure_sensitivity):
        return True
    else:
        return False

def remain_still(acc_accumulator):
    rolling_window = 50
    acceleration_sensitivity = 0.5 # NEED TESTING 
    if (abs(average_window(acc_accumulator, rolling_window, linear_acc_pointer)) < acceleration_sensitivity):
        return True
    else:
        return False

# for heat warning
def check_heat(temperature_accumulator):
    rolling_window = 50
    # if averaged temperature exceeds 83 Celcius, raspberry Pi may die
    if (average_window(temperature_accumulator, rolling_window, bmp_pointer) > 83):
        return True
    else:
        return False

if __name__ == '__main__':
    
    SECOND_NS = 1_000_000_000
    NUM_READINGS = 25
    SAMPLE_FREQUENCY = 100   # in Hz
    DELTA_T = SECOND_NS/SAMPLE_FREQUENCY
    last_sample_t = time.monotonic_ns() # TODO reminder: need to time everything right now
    
    # start_sample_T = time.monotonic_ns()
    print('entering main')


    while True:
        read_bno()
        read_acceleration_buffer()
        read_bmp()
        #print('sequential:',seqeuntial_euler )
        print(detectMovement(acceleration_buffer))
        # print('is it vertical?', vertical(euler_buffer))
        #print('is it vertical?', vertical(seqeuntial_euler))
        # print('flight status?', altitude_status(altitude_buffer, pressure_buffer))