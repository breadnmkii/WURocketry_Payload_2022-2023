import config
import time
import mathlib
import board
import math 

#import adafruit_bno055 as a_bno

"""
Constants
"""
BMP_BUFFER_LEN = 200     # Length of sensor reading buffer
BNO_BUFFER_LEN = 200 


"""
Main components
"""
#(bno, bmp) = config.init_avionics()
bno = config.init_bno()
#bmp = config.init_bmp()
# delete any values from the front??? -- TODO: pointer none stuffs
bno_buf = []
bmp_buf = []
acceleration_buffer = [None]*BNO_BUFFER_LEN
#euler_buffer = [None, None, None]*BNO_BUFFER_LEN
euler_buffer = [[None, None, None] for _ in range(BNO_BUFFER_LEN)]
altitude_buffer = [None]*BMP_BUFFER_LEN
pressure_buffer = [None]*BMP_BUFFER_LEN
temperature_buffer = [None]*BMP_BUFFER_LEN
#global bmp_pointer
bmp_pointer = 0 # pointer for a ring buffer for altitudes and pressures from BMP
#global bno_pointer
bno_pointer = 0 # pointer for a ring buffer for euler orientations and linear accelerations from BNO
euler_orient_pointer = 0
linear_acc_pointer = 0

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
    quat = bno.quaternion
    global bno_pointer
    global euler_orient_pointer
    #bno_pointer = bno_pointer % BNO_BUFFER_LEN
    euler_orient_pointer = euler_orient_pointer % BNO_BUFFER_LEN
    linear_acc_pointer = linear_acc_pointer % BNO_BUFFER_LEN

    if None not in quat:
        [x, y, z, w] = quat
        yy = y * y # 2 Uses below
        # convert to euler, then tell from vertical -- roll and pitch
        roll = math.atan2(2 * (w* x + y * z), 1 - 2*(x * x + yy))
        # clamping asin values
        yaw = math.asin(max(-1, min(2 * w * y - x * z, 1)))
        pitch = math.atan2(2 * (w* z + x * y), 1 - 2*(yy+z * z))
        print('pitch: ', pitch)
        print('roll: ', roll)
        three_ele = [roll, pitch, yaw]
        # euler_buffer.append(three_ele) trying ring buffer right now
        #euler_buffer[bno_pointer] = [roll, pitch, yaw]
        euler_buffer[euler_orient_pointer] = [roll, pitch, yaw]
        euler_orient_pointer = euler_orient_pointer+1

        
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
            the_file.write(acceleration_buffer)
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

def read_euler_buffer():
    quat = bno.quaternion
    global euler_orient_pointer
    euler_orient_pointer = euler_orient_pointer % BNO_BUFFER_LEN

    if None not in quat:
        [x, y, z, w] = quat 
        yy = y * y # 2 Uses below
        # convert to euler, then tell from vertical -- roll and pitch
        roll = math.atan2(2 * (w* x + y * z), 1 - 2*(x * x + yy))
        # clamping asin values
        yaw = math.asin(max(-1, min(2 * w * y - x * z, 1)))
        pitch = math.atan2(2 * (w* z + x * y), 1 - 2*(yy+z * z))
        print('pitch: ', pitch)
        print('roll: ', roll)
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
    if None not in altitude and None not in pressure and None not in temperature:
        altitude_buffer[bmp_pointer] = altitude
        pressure_buffer[bmp_pointer] = pressure
        temperature_buffer[bmp_pointer] = temperature
        bmp_pointer = bmp_pointer+1
    
    if bmp_pointer == BMP_BUFFER_LEN-1:
        with open('altitudes.txt', 'a') as the_file:
            #the_file.write(altitude)
            the_file.write(str(altitude_buffer))
        with open('pressures.txt', 'a') as the_file:
            #the_file.write(pressure)
             the_file.write(str(pressure_buffer))

    return (temperature_buffer, pressure_buffer, altitude_buffer)


""" 
Function to determine if payload is moving,
with sensitivity of 'window' readings mean
"""
def isMoving(window):
    if(bno.linear_acceleration == 0.0): #Assuming it returns in m/s based from documentation
        print("Not moving")
    else:
        print("Moving")

def average_window(list, window, pointer):
    if(not list):
        return 0
    summing = 0
    most_recent = pointer
    least_recent = pointer-window
    if least_recent < 0:
        buf_len = len(list)
        least_recent = buf_len-1-abs(least_recent)
        (sum_left, total_left) = average_sum_abs_range(list, 0, most_recent)
        (sum_right, total_right) = average_sum_abs_range(list, least_recent, buf_len)
        summing = sum_left+sum_right
        window = total_left+total_right
    else:
        # when least_recent >= 0
        (summing, window) =  average_sum_abs_range(list, least_recent, most_recent)
    return summing/window

def average_sum_abs_range(list, least_recent, most_recent):
    start_idx = next((i for i, x in enumerate(list[least_recent:most_recent+1]) if x is not None), None)
    end_idx = next((i for i, x in enumerate(reversed(list[most_recent:least_recent+1])) if x is not None), None)
    if start_idx is None or end_idx is None:
        return (0, 1)
    start_idx += most_recent
    end_idx = least_recent - end_idx
    summing = sum(abs(x) for x in list[start_idx:end_idx])
    return (summing, end_idx-start_idx)

# for BMP readings only 
def differential_window(list, window):
    if (not list):
        return 0
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
    global linear_acc_pointer
    MOTION_SENSITIVITY = 3           # Amount of 3-axis acceleration needed to be read to trigger "movement" detection
    MOTION_LAUNCH_SENSITIVITY = 13   # Amount of accel added to offset for stronger initial launch accel
    hasLaunched = False
    ACC_WINDOW = 50                  # Range of values to apply rolling average in 'acc_accumulator'
    if(average_window(acc_accumulator, ACC_WINDOW, linear_acc_pointer) > MOTION_SENSITIVITY + MOTION_LAUNCH_SENSITIVITY):
        print("Launch detected!")
        hasLaunched = True
    return hasLaunched
    
'''
functionality: detect whether the camera has reached vertical position or not
'''
def vertical(euler_accumulator):
    global euler_orient_pointer
    is_vertical = False
    rolling_window = 50
    threshold = 0.15 # NEED TESTING -- tested 3/6
    rolls = [item[0] for item in euler_accumulator]
    pitches = [item[1] for item in euler_accumulator]
    if (abs(average_window(rolls, rolling_window, euler_orient_pointer)) < threshold and abs(average_window(pitches, rolling_window, euler_orient_pointer)) < threshold):
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
    if (abs(average_window(acc_accumulator, rolling_window, linear_acc_pointer), 0) < acceleration_sensitivity):
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
    #print(read_bmp())
    euler_acc = read_euler_buffer()
    read_acceleration_buffer()
    print('is it vertical?', vertical(euler_acc))
    print('exiting avionics testing for read_bno')

    while True:
        euler_acc = read_euler_buffer()
        read_acceleration_buffer()
        print('is it vertical?', vertical(euler_acc))