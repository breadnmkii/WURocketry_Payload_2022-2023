import config
import time
import mathlib
import board

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



"""
Function returning raw bno data
return: (accel(3), mag(3), gyro(3))
"""
def read_bno():
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

def isUpright():
    if(bno.calibrated):
        print("Upright")




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

