import config

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
    pass


if __name__ == '__main__':
    print(read_bmp())
    print(read_bno())

